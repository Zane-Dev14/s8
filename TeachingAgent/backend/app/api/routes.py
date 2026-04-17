from __future__ import annotations

import asyncio
import copy
import json
import shutil
import time
from pathlib import Path
from typing import Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.core.settings import settings
from app.models.db import Concept, ContentChunk, IngestionJob, LearnerProfile, SourceFile
from app.models.schemas import (
    HealthResponse,
    IngestResponse,
    JobStatusResponse,
    ComprehensionCheckRequest,
    ComprehensionCheckResponse,
    InteractiveTeachResponse,
    QuizQuestionResponse,
    TTSRequest,
    TTSResponse,
    TutorAnswerRequest,
    TutorAnswerResponse,
    TutorStartResponse,
    VoiceProfileResponse,
    WeakArea,
    WeakAreaResponse,
)
from app.services.ingestion_service import IngestionService
from app.services.chunking_service import ChunkingService
from app.services.interactive_teacher_service import InteractiveTeacherService
from app.services.learning_service import LearningService
from app.services.ollama_router import OllamaRouter
from app.services.pipeline_service import PipelineService
from app.services.quiz_service import QuizService
from app.services.tts_service import TTSService
from app.services.tutor_service import TutorService
from app.services.visual_asset_service import VisualAssetService
from app.services.voice_profile_service import VoiceProfileService

router = APIRouter()

_CACHE_TTL_SEC = 15 * 60
_AUDIO_FAIL_COOLDOWN_SEC = 90
_INTERACTIVE_TEACH_TIMEOUT_SEC = 18.0
_DIAGRAM_TIMEOUT_SEC = 8.0
_AUDIO_RESPONSE_WAIT_SEC = 3.5
_teach_cache: dict[str, tuple[float, dict[str, object]]] = {}
_audio_cache: dict[str, tuple[float, dict[str, object]]] = {}
_audio_jobs: dict[str, asyncio.Task[dict[str, object] | None]] = {}
_audio_fail_until: dict[str, float] = {}


def _cache_get(cache: dict[str, tuple[float, dict[str, object]]], key: str) -> dict[str, object] | None:
    item = cache.get(key)
    if not item:
        return None
    expires_at, value = item
    if time.monotonic() >= expires_at:
        cache.pop(key, None)
        return None
    return copy.deepcopy(value)


def _cache_set(cache: dict[str, tuple[float, dict[str, object]]], key: str, value: dict[str, object]) -> None:
    cache[key] = (time.monotonic() + _CACHE_TTL_SEC, copy.deepcopy(value))


def _normalize_chunk_text(chunk_type: str, text: str) -> str:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return ""

    if chunk_type == "concept_bundle":
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            parts = [
                str(parsed.get("explanation", "")).strip(),
                str(parsed.get("example", "")).strip(),
                str(parsed.get("mistake", "")).strip(),
            ]
            cleaned = " ".join(part for part in parts if part)

    if len(cleaned) > 420:
        cleaned = cleaned[:420].rsplit(" ", 1)[0] + "..."
    return cleaned


def _grounded_source_chunks(db: Session, concept: Concept, limit: int = 8) -> list[str]:
    chunking = ChunkingService(db, OllamaRouter())
    query = " ".join(
        part
        for part in [
            concept.name,
            concept.explanation,
            concept.why_it_matters,
            concept.example,
            concept.source_reference,
        ]
        if part
    )
    retrieved = chunking.retrieve_relevant_chunks_with_scores(query, limit=limit)

    lines: list[str] = []
    seen: set[str] = set()
    for item in retrieved:
        normalized = _normalize_chunk_text(item.chunk.chunk_type, item.chunk.text)
        if not normalized:
            continue
        source_ref = item.chunk.source_reference or concept.source_reference or "bootcamp"
        row = f"{source_ref}: {normalized}"
        if row in seen:
            continue
        seen.add(row)
        lines.append(row)

    if lines:
        return lines[:limit]

    fallback = [
        f"{concept.source_reference}: {concept.explanation}" if concept.explanation else "",
        concept.example or "",
        concept.why_it_matters or "",
    ]
    return [line for line in fallback if line]


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name)


@router.post("/api/ingest/upload", response_model=IngestResponse)
def upload_zip(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> IngestResponse:
    filename = file.filename or ""
    if not filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are supported")

    ingestion = IngestionService(db)
    job = ingestion.create_job(filename)

    upload_dir = settings.data_root / "cache" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    zip_path = upload_dir / f"{job.id}_{Path(filename).name}"

    with open(zip_path, "wb") as output:
        shutil.copyfileobj(file.file, output)

    pipeline = PipelineService()
    background_tasks.add_task(pipeline.run, job.id, str(zip_path))

    return IngestResponse(job_id=job.id, status=job.status, stage=job.stage)


@router.get("/api/ingest/{job_id}", response_model=JobStatusResponse)
def job_status(job_id: str, db: Session = Depends(get_db_session)) -> JobStatusResponse:
    job = db.get(IngestionJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    files_indexed = int(
        db.scalar(select(func.count()).select_from(SourceFile).where(SourceFile.job_id == job_id)) or 0
    )
    concepts_count = int(db.scalar(select(func.count()).select_from(Concept)) or 0)

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        stage=job.stage,
        message=job.message,
        created_at=job.created_at,
        updated_at=job.updated_at,
        files_indexed=files_indexed,
        concepts_count=concepts_count,
    )


@router.get("/api/timeline/{job_id}")
def timeline(job_id: str, db: Session = Depends(get_db_session)) -> dict[str, list[dict[str, object]]]:
    return PipelineService.timeline(db, job_id)


@router.get("/api/course-map")
def course_map(db: Session = Depends(get_db_session)) -> dict[str, list[dict[str, str]]]:
    return PipelineService.course_map(db)


@router.get("/api/tutor/start", response_model=TutorStartResponse)
async def tutor_start(
    user_id: str = "local-user",
    mode: Literal["lesson", "interview"] = "lesson",
    concept_id: Optional[str] = None,
    db: Session = Depends(get_db_session),
) -> TutorStartResponse:
    tutor = TutorService(db, OllamaRouter())
    if concept_id:
        concept, lesson_preview, question, time_pressure_seconds = await tutor.start_lesson_for_concept(concept_id, mode)
    else:
        concept, lesson_preview, question, time_pressure_seconds = await tutor.start_lesson(user_id, mode)
    if not concept:
        raise HTTPException(status_code=404, detail="No concept available. Run ingestion first.")
    return TutorStartResponse(
        concept_id=concept.id,
        mode=mode,
        lesson_preview=lesson_preview,
        question=question,
        answer_before_explanation=True,
        time_pressure_seconds=time_pressure_seconds,
    )

@router.get("/api/tutor/interactive-teach", response_model=InteractiveTeachResponse)
async def interactive_teach(
    concept_id: str,
    user_id: str = "local-user",
    voice_profile: Optional[str] = None,
    generate_audio: bool = True,
    db: Session = Depends(get_db_session),
) -> InteractiveTeachResponse:
    """
    Generate an interactive teaching session with model-generated explanations,
    auto-generated diagrams, and full-session audio/subtitles.
    """
    concept = db.get(Concept, concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    teach_key = f"teach:{concept.id}"
    selected_voice_profile = voice_profile or settings.default_voice_profile
    teacher = InteractiveTeacherService()

    cached_teaching = _cache_get(_teach_cache, teach_key)
    if cached_teaching is not None:
        teaching_session = cached_teaching
    else:
        source_chunks = _grounded_source_chunks(db, concept, limit=8)
        try:
            teaching_session = await asyncio.wait_for(
                teacher.generate_teaching_session(
                    concept_name=concept.name,
                    concept_explanation=concept.explanation,
                    source_chunks=source_chunks,
                    learner_level="beginner",
                ),
                timeout=_INTERACTIVE_TEACH_TIMEOUT_SEC,
            )
        except Exception:
            teaching_session = teacher._fallback_teaching_content(
                concept_name=concept.name,
                concept_explanation=concept.explanation,
                raw_response="",
            )

        visuals = VisualAssetService(db).find_diagrams_for_concept(concept.name)
        try:
            generated_diagram = await asyncio.wait_for(
                teacher.generate_mermaid_diagram(
                    concept_name=concept.name,
                    sections=teaching_session.get("sections", {}),
                ),
                timeout=_DIAGRAM_TIMEOUT_SEC,
            )
        except Exception:
            generated_diagram = None

        if not generated_diagram:
            generated_diagram = teacher._fallback_mermaid_diagram(
                concept_name=concept.name,
                sections=teaching_session.get("sections", {}),
            )

        if generated_diagram:
            visuals = [generated_diagram, *visuals]

        teaching_session["diagrams"] = visuals
        teaching_session["has_audio"] = False
        teaching_session["audio"] = None
        _cache_set(_teach_cache, teach_key, teaching_session)

    audio_key = f"audio:{concept.id}:{selected_voice_profile}"
    cached_audio = _cache_get(_audio_cache, audio_key)
    existing_task = _audio_jobs.get(audio_key)
    now = time.monotonic()
    if existing_task is not None and existing_task.done():
        _audio_jobs.pop(audio_key, None)
        existing_task = None

    fail_until = _audio_fail_until.get(audio_key, 0.0)
    in_fail_cooldown = fail_until > now
    if not in_fail_cooldown:
        _audio_fail_until.pop(audio_key, None)

    if cached_audio is not None:
        teaching_session["has_audio"] = True
        teaching_session["audio"] = cached_audio
    else:
        tts = TTSService()

        async def _build_audio_payload() -> dict[str, object] | None:
            try:
                audio_payload = await teacher.generate_audio_teaching(
                    teaching_content=teaching_session,
                    voice_style="energetic_teacher",
                    voice_profile=selected_voice_profile,
                )
            except Exception:
                return None

            filtered_segments: list[dict[str, object]] = []
            for segment in audio_payload.get("segments", []):
                audio_url = tts.to_public_url(segment.get("audio_path", ""))
                if not audio_url:
                    continue
                normalized_segment = dict(segment)
                normalized_segment["audio_url"] = audio_url
                filtered_segments.append(normalized_segment)

            if not filtered_segments:
                return None

            return {
                "total_duration_seconds": sum(float(seg.get("duration_seconds", 0.0)) for seg in filtered_segments),
                "segments": filtered_segments,
                "voice_style": audio_payload.get("voice_style", "energetic_teacher"),
                "voice_profile": selected_voice_profile,
            }

        # Always warm audio in the background so users never need a button click.
        if existing_task is None and not in_fail_cooldown:
            existing_task = asyncio.create_task(_build_audio_payload())
            _audio_jobs[audio_key] = existing_task

        def _store_audio(done_task: asyncio.Task[dict[str, object] | None], key: str = audio_key) -> None:
            try:
                payload = done_task.result()
                if payload is not None:
                    _cache_set(_audio_cache, key, payload)
                    _audio_fail_until.pop(key, None)
                else:
                    _audio_fail_until[key] = time.monotonic() + _AUDIO_FAIL_COOLDOWN_SEC
            except Exception:
                _audio_fail_until[key] = time.monotonic() + _AUDIO_FAIL_COOLDOWN_SEC
            finally:
                _audio_jobs.pop(key, None)

        if not existing_task.done():
            existing_task.add_done_callback(_store_audio)

        if generate_audio:
            if existing_task is None:
                teaching_session["has_audio"] = False
                teaching_session["audio"] = None
                return InteractiveTeachResponse(**teaching_session)
            try:
                generated_audio = await asyncio.wait_for(asyncio.shield(existing_task), timeout=_AUDIO_RESPONSE_WAIT_SEC)
                if generated_audio is not None:
                    _cache_set(_audio_cache, audio_key, generated_audio)
                    teaching_session["has_audio"] = True
                    teaching_session["audio"] = generated_audio
                else:
                    teaching_session["has_audio"] = False
                    teaching_session["audio"] = None
            except asyncio.TimeoutError:
                teaching_session["has_audio"] = False
                teaching_session["audio"] = None
        else:
            teaching_session["has_audio"] = False
            teaching_session["audio"] = None

    return InteractiveTeachResponse(**teaching_session)


@router.post("/api/tutor/comprehension-check", response_model=ComprehensionCheckResponse)
async def comprehension_check(
    payload: ComprehensionCheckRequest,
    db: Session = Depends(get_db_session),
) -> ComprehensionCheckResponse:
    concept = db.get(Concept, payload.concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    source_chunks = _grounded_source_chunks(db, concept, limit=5)

    teacher = InteractiveTeacherService()
    result = await teacher.assess_comprehension(
        concept_name=concept.name,
        learner_summary=payload.summary_in_own_words,
        learner_example=payload.real_world_example,
        learner_failure_mode=payload.failure_mode,
        source_chunks=source_chunks,
    )
    return ComprehensionCheckResponse(**result)



@router.post("/api/tutor/answer", response_model=TutorAnswerResponse)
async def tutor_answer(payload: TutorAnswerRequest, db: Session = Depends(get_db_session)) -> TutorAnswerResponse:
    concept = db.get(Concept, payload.concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    tutor = TutorService(db, OllamaRouter())
    (
        correctness,
        explanation,
        misconception_tag,
        next_action,
        next_question,
        source_chunks,
        confidence_label,
        uncertainty,
        feedback_delay_ms,
    ) = await tutor.evaluate_answer(
        user_id=payload.user_id,
        concept=concept,
        question=payload.question,
        user_answer=payload.user_answer,
        user_confidence=payload.user_confidence,
        response_time_ms=payload.response_time_ms,
        mode=payload.mode,
    )
    action_literal: Literal["harder", "retry", "review", "rebuild", "interview"] = next_action

    return TutorAnswerResponse(
        question=payload.question,
        user_answer=payload.user_answer,
        user_confidence=payload.user_confidence,
        correctness=correctness,
        answer=explanation,
        explanation=explanation,
        misconception_tag=misconception_tag,
        next_action=action_literal,
        source_chunks=source_chunks,
        confidence=confidence_label,
        uncertainty=uncertainty,
        next_question=next_question,
        feedback_delay_ms=feedback_delay_ms,
    )


@router.get("/api/quiz/next", response_model=QuizQuestionResponse)
async def quiz_next(db: Session = Depends(get_db_session)) -> QuizQuestionResponse:
    quiz = QuizService(db, OllamaRouter())
    await quiz.ensure_questions()
    question, options = quiz.get_next_question()
    if not question:
        raise HTTPException(status_code=404, detail="No quiz questions available")

    return QuizQuestionResponse(
        question_id=question.id,
        concept_id=question.concept_id,
        question=question.question,
        options=options,
        correct_answer=question.correct_answer,
        difficulty=question.difficulty,
    )


@router.get("/api/analytics/weak-areas", response_model=WeakAreaResponse)
def weak_areas(user_id: str = "local-user", db: Session = Depends(get_db_session)) -> WeakAreaResponse:
    learning = LearningService(db)
    rows = list(
        db.scalars(
            select(LearnerProfile).where(LearnerProfile.user_id == user_id).order_by(LearnerProfile.accuracy.asc())
        ).all()
    )

    weak: list[WeakArea] = []
    for profile in rows[:10]:
        concept = db.get(Concept, profile.concept_id)
        if not concept:
            continue
        weak.append(
            WeakArea(
                concept_id=concept.id,
                concept_name=concept.name,
                accuracy=profile.accuracy,
                retries=profile.retries,
                response_time_ms=profile.response_time_ms,
                mastered=learning.is_mastered(user_id, concept.id),
                pressure_failures=learning.pressure_failures(user_id, concept.id),
            )
        )

    return WeakAreaResponse(user_id=user_id, weak_areas=weak)


@router.get("/api/assets/visual/{job_id}/{source_file_id}")
def visual_asset(job_id: str, source_file_id: str, db: Session = Depends(get_db_session)) -> FileResponse:
    source_file = db.get(SourceFile, source_file_id)
    if not source_file or source_file.job_id != job_id or source_file.file_type != "visual":
        raise HTTPException(status_code=404, detail="Visual asset not found")

    root = (settings.data_root / "ingested" / job_id).resolve()
    asset = (root / source_file.path).resolve()
    if root != asset and root not in asset.parents:
        raise HTTPException(status_code=400, detail="Invalid asset path")
    if not asset.exists():
        raise HTTPException(status_code=404, detail="Visual file missing on disk")
    return FileResponse(str(asset))


@router.get("/api/assets/tts/{file_name}")
def tts_asset(file_name: str) -> FileResponse:
    if Path(file_name).name != file_name:
        raise HTTPException(status_code=400, detail="Invalid file name")

    asset = settings.data_root / "tts" / file_name
    if not asset.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(str(asset))


@router.post("/api/voice/train-profile", response_model=VoiceProfileResponse)
def train_voice_profile(profile_name: str = Form(...), clip: UploadFile = File(...)) -> VoiceProfileResponse:
    clip_name = clip.filename or "voice-sample"
    upload_dir = settings.data_root / "cache" / "voice_uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    temp_path = upload_dir / f"{uuid4()}_{Path(clip_name).name}"
    with open(temp_path, "wb") as handle:
        shutil.copyfileobj(clip.file, handle)

    service = VoiceProfileService()
    try:
        profile = service.create_profile_from_clip(profile_name, temp_path)
        return VoiceProfileResponse(**profile)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        temp_path.unlink(missing_ok=True)


@router.get("/api/voice/profiles", response_model=list[VoiceProfileResponse])
def list_voice_profiles() -> list[VoiceProfileResponse]:
    service = VoiceProfileService()
    return [VoiceProfileResponse(**item) for item in service.list_profiles()]


@router.post("/api/tts/speak", response_model=TTSResponse)
def speak(payload: TTSRequest) -> TTSResponse:
    tts = TTSService()
    audio_path = tts.synthesize(
        payload.text,
        payload.speed,
        payload.tone,
        payload.emphasis_words,
        payload.voice_profile,
    )
    return TTSResponse(audio_path=audio_path, audio_url=tts.to_public_url(audio_path))


# ============================================================================
# Subject and Concept Management Endpoints
# ============================================================================

@router.get("/api/subjects")
def get_all_subjects(db: Session = Depends(get_db_session)):
    """Get all subjects"""
    from app.models.db import Subject
    subjects = db.query(Subject).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "status": s.status,
            "created_at": s.created_at.isoformat(),
        }
        for s in subjects
    ]


@router.get("/api/subjects/{subject_id}")
def get_subject(subject_id: str, db: Session = Depends(get_db_session)):
    """Get subject details"""
    from app.models.db import Subject
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    concept_count = db.query(Concept).filter(Concept.subject_id == subject_id).count()
    
    return {
        "id": subject.id,
        "name": subject.name,
        "description": subject.description,
        "status": subject.status,
        "concept_count": concept_count,
        "created_at": subject.created_at.isoformat(),
    }


@router.get("/api/subjects/{subject_id}/concepts")
def get_subject_concepts(subject_id: str, db: Session = Depends(get_db_session)):
    """Get all concepts for a subject"""
    concepts = db.query(Concept).filter(Concept.subject_id == subject_id).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "plain_name": c.plain_name,
            "difficulty": c.difficulty,
            "explanation": c.explanation,
            "module": c.module or "Other",
            "metadata_json": c.metadata_json or "{}",
            "prerequisites_json": c.prerequisites_json or "[]",
        }
        for c in concepts
    ]


@router.get("/api/concepts/{concept_id}")
def get_concept(concept_id: str, db: Session = Depends(get_db_session)):
    """Get concept details"""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    return {
        "id": concept.id,
        "subject_id": concept.subject_id,
        "name": concept.name,
        "plain_name": concept.plain_name,
        "difficulty": concept.difficulty,
        "explanation": concept.explanation,
        "why_it_matters": concept.why_it_matters,
        "intuition": concept.intuition,
        "example": concept.example,
        "common_mistake": concept.common_mistake,
    }


# ============================================================================
# Flashcard Endpoints
# ============================================================================

@router.post("/api/flashcards/generate")
async def generate_flashcards(
    payload: dict,
    db: Session = Depends(get_db_session)
):
    """Generate flashcards for a concept"""
    from app.services.flashcard_service import FlashcardService
    
    concept_id = payload.get("concept_id")
    min_cards = payload.get("count", 5)
    
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    # Get context chunks from the concept's subject source files
    from app.models.db import SourceFile, IngestionJob
    jobs = db.query(IngestionJob).filter(IngestionJob.subject_id == concept.subject_id).all()
    
    context_chunks = []
    for job in jobs:
        for sf in job.files[:2]:  # First 2 files per job
            for chunk in sf.chunks[:5]:  # First 5 chunks per file
                context_chunks.append(chunk.text)
                if len(context_chunks) >= 10:  # Max 10 chunks total
                    break
            if len(context_chunks) >= 10:
                break
        if len(context_chunks) >= 10:
            break
    
    if not context_chunks:
        context_chunks = [f"Concept: {concept.name}\nThis is a concept in {concept.subject.name}"]
    
    service = FlashcardService(db)
    cards = await service.generate_flashcards_for_concept(concept, context_chunks, min_cards)
    
    return {
        "concept_id": concept_id,
        "cards_generated": len(cards),
        "cards": [
            {
                "id": card.id,
                "card_type": card.card_type,
                "front": card.front,
                "back": card.back,
            }
            for card in cards
        ]
    }


@router.get("/api/concepts/{concept_id}/flashcards")
def get_flashcards(concept_id: str, db: Session = Depends(get_db_session)):
    """Get all flashcards for a concept"""
    from app.models.db import Flashcard
    
    cards = db.query(Flashcard).filter(Flashcard.concept_id == concept_id).all()
    return [
        {
            "id": card.id,
            "card_type": card.card_type,
            "front": card.front,
            "back": card.back,
            "ease_factor": card.ease_factor,
            "interval_days": card.interval_days,
            "repetitions": card.repetitions,
        }
        for card in cards
    ]


# ============================================================================
# Quiz Endpoints
# ============================================================================

@router.post("/api/quiz/generate")
async def generate_quiz_question(
    payload: dict,
    db: Session = Depends(get_db_session)
):
    """Generate quiz questions for a concept"""
    from app.services.quiz_service import QuizService
    
    concept_id = payload.get("concept_id")
    count = payload.get("count", 5)
    
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    # Get context chunks from the concept's subject source files
    from app.models.db import SourceFile, IngestionJob
    jobs = db.query(IngestionJob).filter(IngestionJob.subject_id == concept.subject_id).all()
    
    context_chunks = []
    for job in jobs:
        for sf in job.files[:2]:  # First 2 files per job
            for chunk in sf.chunks[:5]:  # First 5 chunks per file
                context_chunks.append(chunk.text)
                if len(context_chunks) >= 10:  # Max 10 chunks total
                    break
            if len(context_chunks) >= 10:
                break
        if len(context_chunks) >= 10:
            break
    
    if not context_chunks:
        context_chunks = [f"Concept: {concept.name}\nThis is a concept in {concept.subject.name}"]
    
    service = QuizService(db)
    questions = await service.generate_questions_for_concept(concept, context_chunks, count)
    
    return {
        "concept_id": concept_id,
        "questions_generated": len(questions),
        "questions": [
            {
                "id": q.id,
                "question_type": q.question_type,
                "question": q.question,
                "correct_answer": q.correct_answer,
                "distractors": json.loads(q.distractors_json) if q.distractors_json else []
            }
            for q in questions
        ]
    }


@router.post("/api/quiz/evaluate")
async def evaluate_answer(
    payload: dict,
    db: Session = Depends(get_db_session)
):
    """Evaluate a quiz answer"""
    from app.services.quiz_service import QuizService
    from app.models.db import QuizQuestion
    
    question_id = payload.get("question_id")
    answer = payload.get("answer", "")
    confidence = payload.get("confidence", 50)
    response_time_ms = payload.get("response_time_ms", 5000)
    
    if not answer:
        raise HTTPException(status_code=400, detail="Answer is required")
    
    question = db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    service = QuizService(db)
    result = await service.evaluate_answer(
        question=question,
        user_answer=answer,
        confidence=confidence,
        response_time_ms=response_time_ms
    )
    
    return result


# ============================================================================
# TTS Synthesis Endpoint
# ============================================================================

@router.post("/api/tts/synthesize")
async def synthesize_speech(payload: dict):
    """Synthesize speech from text using Goku voice"""
    from app.services.goku_tts_service import GokuTTSService
    from pathlib import Path
    
    text = payload.get("text", "")
    voice_profile = payload.get("voice_profile", "goku")
    
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    service = GokuTTSService()
    audio_path_str = await service.speak(text)
    audio_path = Path(audio_path_str)
    
    return {
        "audio_path": str(audio_path),
        "audio_url": f"/api/audio/{audio_path.name}",
        "text": text,
        "voice_profile": voice_profile,
        "cached": service._get_cached_audio(text) is not None
    }


@router.get("/api/audio/{file_name}")
def serve_audio(file_name: str):
    """Serve generated audio files"""
    audio_path = settings.data_root / "tts" / file_name
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/wav")
