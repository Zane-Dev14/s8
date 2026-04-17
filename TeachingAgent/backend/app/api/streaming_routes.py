"""
Streaming API Routes - Server-Sent Events for Real-Time Teaching
All teaching and quiz interactions use SSE for instant feedback
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
import json

from app.core.database import get_db_session
from app.models.db import Concept, Subject, ContentChunk
from app.services.teaching_session_service import TeachingSessionService
from app.services.streaming_service import StreamingService
from app.services.quiz_service import QuizService


router = APIRouter(prefix="/api/stream", tags=["streaming"])


@router.get("/teach/{concept_id}")
async def stream_teaching_session(
    concept_id: str,
    user_level: str = "beginner",
    db: Session = Depends(get_db_session),
):
    """
    Stream complete teaching session section by section.
    Returns SSE stream with tokens and section completions.
    """
    # Get concept
    concept = db.get(Concept, concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    # Create teaching service
    teaching_service = TeachingSessionService(db)
    
    async def event_generator():
        """Generate SSE events"""
        try:
            async for event in teaching_service.stream_teaching_session(
                concept=concept,
                user_level=user_level,
            ):
                # Format as SSE
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            error_event = {
                "type": "error",
                "error": str(e),
                "done": True,
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/quiz/evaluate")
async def stream_quiz_evaluation(
    question_id: str,
    user_answer: str,
    confidence: int,
    response_time_ms: float,
    db: Session = Depends(get_db_session),
):
    """
    Stream quiz answer evaluation with real-time feedback.
    Returns SSE stream with evaluation tokens.
    """
    from app.models.db import QuizQuestion
    
    # Get question
    question = db.get(QuizQuestion, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Get concept for context
    concept = db.get(Concept, question.concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    # Get context chunks
    try:
        context_chunks = json.loads(question.source_chunks)
    except json.JSONDecodeError:
        context_chunks = []
    
    streaming_service = StreamingService()
    
    async def event_generator():
        """Generate SSE events for evaluation"""
        try:
            # Stream evaluation feedback
            async for chunk in streaming_service.stream_quiz_evaluation(
                concept_name=concept.name,
                question=question.question,
                user_answer=user_answer,
                correct_answer=question.correct_answer,
                context_chunks=context_chunks,
            ):
                yield f"data: {chunk}\n\n"
            
            # Send final evaluation
            quiz_service = QuizService(db)
            evaluation = await quiz_service.evaluate_answer(
                question=question,
                user_answer=user_answer,
                confidence=confidence,
                response_time_ms=response_time_ms,
            )
            
            final_event = {
                "type": "evaluation_complete",
                "evaluation": evaluation,
                "done": True,
            }
            yield f"data: {json.dumps(final_event)}\n\n"
            
        except Exception as e:
            error_event = {
                "type": "error",
                "error": str(e),
                "done": True,
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/concept/extract/{subject_id}")
async def stream_concept_extraction(
    subject_id: str,
    db: Session = Depends(get_db_session),
):
    """
    Stream concept extraction progress for a subject.
    Shows real-time progress as concepts are discovered.
    """
    # Get subject
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Get content chunks
    chunks = list(
        db.scalars(
            select(ContentChunk)
            .join(ContentChunk.source_file)
            .where(ContentChunk.source_file.has(job_id=subject.ingestion_jobs[0].id))
            .limit(100)
        ).all()
    )
    
    if not chunks:
        raise HTTPException(status_code=400, detail="No content chunks found for subject")
    
    from app.services.concept_extraction_service import ConceptExtractionService
    extractor = ConceptExtractionService()
    
    async def event_generator():
        """Generate SSE events for extraction progress"""
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'total_chunks': len(chunks)})}\n\n"
            
            # Extract concepts
            content_texts = [chunk.text for chunk in chunks if chunk.text]
            concepts = await extractor.extract_concepts(
                subject_name=subject.name,
                content_chunks=content_texts,
                max_concepts=20,
            )
            
            # Send progress for each concept
            for idx, concept_data in enumerate(concepts, 1):
                event = {
                    "type": "concept_found",
                    "concept": concept_data,
                    "progress": f"{idx}/{len(concepts)}",
                }
                yield f"data: {json.dumps(event)}\n\n"
            
            # Send completion
            final_event = {
                "type": "extraction_complete",
                "total_concepts": len(concepts),
                "done": True,
            }
            yield f"data: {json.dumps(final_event)}\n\n"
            
        except Exception as e:
            error_event = {
                "type": "error",
                "error": str(e),
                "done": True,
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )

# Made with Bob
