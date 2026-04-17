from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str


class IngestionMetadata(BaseModel):
    path: str
    folder: str
    extension: str
    type: str
    is_video: bool
    recording_day: str
    size: int


class IngestResponse(BaseModel):
    job_id: str
    status: str
    stage: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    stage: str
    message: str
    created_at: datetime
    updated_at: datetime
    files_indexed: int
    concepts_count: int


class TranscriptSegmentPayload(BaseModel):
    timestamp_start: float
    timestamp_end: float
    text: str
    topic: str
    importance: int = Field(ge=1, le=5)
    keyframe_path: str = ""


class TutorStartResponse(BaseModel):
    concept_id: str
    mode: Literal["lesson", "interview"]
    lesson_preview: dict[str, str]
    question: str
    answer_before_explanation: bool = True
    time_pressure_seconds: int


class TutorAnswerRequest(BaseModel):
    user_id: str = "local-user"
    concept_id: str
    question: str
    user_answer: str
    user_confidence: int = Field(default=50, ge=0, le=100)
    response_time_ms: float = 0.0
    mode: Literal["lesson", "interview"] = "lesson"


class TutorAnswerResponse(BaseModel):
    question: str
    user_answer: str
    user_confidence: int
    correctness: bool
    answer: str
    explanation: str
    misconception_tag: str
    next_action: Literal["harder", "retry", "review", "rebuild", "interview"]
    source_chunks: list[str]
    confidence: str
    uncertainty: str
    next_question: str
    feedback_delay_ms: int


class QuizQuestionResponse(BaseModel):
    question_id: str
    concept_id: str
    question: str
    options: list[str]
    correct_answer: str
    difficulty: int


class WeakArea(BaseModel):
    concept_id: str
    concept_name: str
    accuracy: float
    retries: int
    response_time_ms: float
    mastered: bool
    pressure_failures: int


class WeakAreaResponse(BaseModel):
    user_id: str
    weak_areas: list[WeakArea]


class TTSRequest(BaseModel):
    text: str
    speed: float = Field(default=1.2, ge=0.75, le=1.5)
    tone: Literal["teaching", "challenge"] = "teaching"
    emphasis_words: list[str] = Field(default_factory=list)
    voice_profile: Optional[str] = None


class TTSResponse(BaseModel):
    audio_path: str
    audio_url: str = ""


class InteractiveTeachDiagram(BaseModel):
    title: str
    description: str
    image_url: str
    source_path: str = ""
    mermaid_code: str = ""


class InteractiveTeachFlashcard(BaseModel):
    id: str
    front: str
    back: str
    cue: str = ""


class InteractiveTeachAudioSegment(BaseModel):
    section: str
    audio_path: str
    audio_url: str = ""
    duration_seconds: float
    text: str


class InteractiveTeachAudio(BaseModel):
    total_duration_seconds: float
    segments: list[InteractiveTeachAudioSegment]
    voice_style: str
    voice_profile: str = ""


class InteractiveTeachResponse(BaseModel):
    concept_name: str
    teaching_style: str
    learner_level: str
    sections: dict[str, str]
    flashcards: list[InteractiveTeachFlashcard] = Field(default_factory=list)
    has_audio: bool = False
    diagrams: list[InteractiveTeachDiagram] = Field(default_factory=list)
    interactive_elements: list[dict[str, object]] = Field(default_factory=list)
    audio: Optional[InteractiveTeachAudio] = None


class ComprehensionCheckRequest(BaseModel):
    user_id: str = "local-user"
    concept_id: str
    summary_in_own_words: str = Field(min_length=8)
    real_world_example: str = Field(min_length=8)
    failure_mode: str = Field(min_length=8)


class ComprehensionCheckResponse(BaseModel):
    understood: bool
    score: int = Field(ge=0, le=100)
    feedback: str
    next_step: Literal["ready_for_question", "needs_reteach"]


class VoiceProfileResponse(BaseModel):
    profile_name: str
    created_at: str = ""
    source_clip: str = ""
    sample_count: int
    samples: list[str] = Field(default_factory=list)
