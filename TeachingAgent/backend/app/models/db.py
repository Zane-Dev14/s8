from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Subject(Base):
    """A subject/course that can be taught (e.g., 'Networking', 'Blockchain', 'Soft Computing')"""
    __tablename__ = "subjects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="pending")  # pending, processing, ready, failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingestion_jobs: Mapped[list[IngestionJob]] = relationship(back_populates="subject", cascade="all, delete-orphan")
    concepts: Mapped[list[Concept]] = relationship(back_populates="subject", cascade="all, delete-orphan")


class IngestionJob(Base):
    """Tracks ingestion of files for a subject"""
    __tablename__ = "ingestion_jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    subject_id: Mapped[str] = mapped_column(ForeignKey("subjects.id"), index=True)
    zip_name: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    stage: Mapped[str] = mapped_column(String(64), default="queued")
    message: Mapped[str] = mapped_column(String(1024), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject: Mapped[Subject] = relationship(back_populates="ingestion_jobs")
    files: Mapped[list[SourceFile]] = relationship(back_populates="job", cascade="all, delete-orphan")


class SourceFile(Base):
    """Individual files ingested for a subject"""
    __tablename__ = "source_files"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    job_id: Mapped[str] = mapped_column(ForeignKey("ingestion_jobs.id"), index=True)

    path: Mapped[str] = mapped_column(String(2048), index=True)
    folder: Mapped[str] = mapped_column(String(512), index=True)
    extension: Mapped[str] = mapped_column(String(16), index=True)
    file_type: Mapped[str] = mapped_column(String(32), index=True)  # pdf, video, audio, image, text
    is_video: Mapped[bool] = mapped_column(Boolean, default=False)
    recording_day: Mapped[str] = mapped_column(String(16), default="")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)

    job: Mapped[IngestionJob] = relationship(back_populates="files")
    transcript_segments: Mapped[list[TranscriptSegment]] = relationship(back_populates="source_file", cascade="all, delete-orphan")
    chunks: Mapped[list[ContentChunk]] = relationship(back_populates="source_file", cascade="all, delete-orphan")


class TranscriptSegment(Base):
    """Transcribed segments from video/audio files"""
    __tablename__ = "transcript_segments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    source_file_id: Mapped[str] = mapped_column(ForeignKey("source_files.id"), index=True)

    start_sec: Mapped[float] = mapped_column(Float)
    end_sec: Mapped[float] = mapped_column(Float)
    text: Mapped[str] = mapped_column(Text)
    topic: Mapped[str] = mapped_column(String(256), default="")
    importance: Mapped[int] = mapped_column(Integer, default=3)
    keyframe_path: Mapped[str] = mapped_column(String(2048), default="")

    source_file: Mapped[SourceFile] = relationship(back_populates="transcript_segments")


class ParsedDocument(Base):
    """Full text extracted from documents"""
    __tablename__ = "parsed_documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    source_file_id: Mapped[str] = mapped_column(ForeignKey("source_files.id"), index=True)
    full_text: Mapped[str] = mapped_column(Text)


class ContentChunk(Base):
    """Semantic chunks for RAG retrieval"""
    __tablename__ = "content_chunks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    source_file_id: Mapped[str] = mapped_column(ForeignKey("source_files.id"), index=True)
    transcript_segment_id: Mapped[Optional[str]] = mapped_column(ForeignKey("transcript_segments.id"), nullable=True)

    chunk_type: Mapped[str] = mapped_column(String(32), default="document")
    text: Mapped[str] = mapped_column(Text)
    source_reference: Mapped[str] = mapped_column(String(1024))
    embedding_json: Mapped[str] = mapped_column(Text, default="[]")  # Deprecated - use ChromaDB

    source_file: Mapped[SourceFile] = relationship(back_populates="chunks")


class Concept(Base):
    """Learning concepts extracted from subject materials"""
    __tablename__ = "concepts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    subject_id: Mapped[str] = mapped_column(ForeignKey("subjects.id"), index=True)
    
    name: Mapped[str] = mapped_column(String(256), index=True)
    plain_name: Mapped[str] = mapped_column(String(256), default="")  # Jargon-free name
    difficulty: Mapped[str] = mapped_column(String(32), default="beginner")  # beginner, intermediate, advanced
    
    # Teaching content (cached from generation)
    why_it_matters: Mapped[str] = mapped_column(Text, default="")
    intuition: Mapped[str] = mapped_column(Text, default="")
    explanation: Mapped[str] = mapped_column(Text, default="")
    example: Mapped[str] = mapped_column(Text, default="")
    common_mistake: Mapped[str] = mapped_column(Text, default="")
    
    # Quiz content (pre-generated)
    checkpoint_question: Mapped[str] = mapped_column(Text, default="")
    hard_follow_up: Mapped[str] = mapped_column(Text, default="")
    
    source_reference: Mapped[str] = mapped_column(String(1024), default="")

    subject: Mapped[Subject] = relationship(back_populates="concepts")
    edges_out: Mapped[list[ConceptEdge]] = relationship(
        foreign_keys="ConceptEdge.source_concept_id",
        back_populates="source_concept",
        cascade="all, delete-orphan"
    )
    edges_in: Mapped[list[ConceptEdge]] = relationship(
        foreign_keys="ConceptEdge.target_concept_id",
        back_populates="target_concept",
        cascade="all, delete-orphan"
    )
    flashcards: Mapped[list[Flashcard]] = relationship(back_populates="concept", cascade="all, delete-orphan")
    quiz_questions: Mapped[list[QuizQuestion]] = relationship(back_populates="concept", cascade="all, delete-orphan")


class ConceptEdge(Base):
    """Relationships between concepts (dependency graph)"""
    __tablename__ = "concept_edges"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    source_concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)
    target_concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)
    edge_type: Mapped[str] = mapped_column(String(32), index=True)  # depends_on, part_of, related_to

    source_concept: Mapped[Concept] = relationship(foreign_keys=[source_concept_id], back_populates="edges_out")
    target_concept: Mapped[Concept] = relationship(foreign_keys=[target_concept_id], back_populates="edges_in")


class Flashcard(Base):
    """Spaced repetition flashcards for concepts"""
    __tablename__ = "flashcards"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)
    
    card_type: Mapped[str] = mapped_column(String(32), default="definition")  # definition, analogy, application, mistake
    front: Mapped[str] = mapped_column(Text)
    back: Mapped[str] = mapped_column(Text)
    cue: Mapped[str] = mapped_column(String(256), default="")  # Hint for answering
    
    # SM-2 Algorithm fields
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=1)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    concept: Mapped[Concept] = relationship(back_populates="flashcards")


class LearnerProfile(Base):
    """Per-user, per-concept learning progress"""
    __tablename__ = "learner_profiles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(128), index=True)
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)

    # Performance metrics
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    response_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    confidence: Mapped[int] = mapped_column(Integer, default=50)  # 0-100
    
    # Spaced repetition
    next_review_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Mastery tracking
    mastered: Mapped[bool] = mapped_column(Boolean, default=False)
    mastered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class LearningAttempt(Base):
    """Individual quiz/practice attempts"""
    __tablename__ = "learning_attempts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(128), index=True)
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)

    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    feedback: Mapped[str] = mapped_column(Text)
    
    response_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[int] = mapped_column(Integer, default=50)
    
    misconception_tag: Mapped[str] = mapped_column(String(64), default="")  # false_confidence, lucky_guess, fragile, confused
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class QuizQuestion(Base):
    """Pre-generated quiz questions for concepts"""
    __tablename__ = "quiz_questions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)
    
    question_type: Mapped[str] = mapped_column(String(32), default="multiple_choice")  # multiple_choice, free_answer, scenario, fill_blank
    question: Mapped[str] = mapped_column(Text)
    correct_answer: Mapped[str] = mapped_column(Text)
    distractors_json: Mapped[str] = mapped_column(Text, default="[]")  # For multiple choice
    difficulty: Mapped[int] = mapped_column(Integer, default=3)  # 1-5
    
    # RAG grounding
    source_chunks: Mapped[str] = mapped_column(Text, default="[]")  # JSON array of chunk IDs
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    concept: Mapped[Concept] = relationship(back_populates="quiz_questions")

# Made with Bob
