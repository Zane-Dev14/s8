"""Shared fixtures for test suite."""
from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.db import Base, Concept, ConceptEdge, ContentChunk, LearnerProfile, LearningAttempt, SourceFile


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def mock_ollama_router():
    """Mock OllamaRouter for testing."""
    router = MagicMock()
    router.chat = AsyncMock(return_value='{"correctness": true, "explanation": "Good answer", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}')
    router.embeddings = AsyncMock(return_value=[0.1] * 384)
    return router


@pytest.fixture
def sample_concept(db_session: Session):
    """Create a sample concept for testing."""
    concept = Concept(
        id="concept-1",
        name="SFTP Protocol",
        explanation="Secure File Transfer Protocol for encrypted file transfers",
        intuition="Think of SFTP as a secure tunnel for moving files",
        example="Using SFTP to transfer EDI documents between trading partners",
        common_mistake="Confusing SFTP with FTPS - they use different security mechanisms",
        why_it_matters="Critical for secure B2B data exchange",
        checkpoint_question="What makes SFTP different from regular FTP?",
        hard_follow_up="Under what conditions would SFTP authentication fail and how would you diagnose it?",
        source_reference="Day1-Recording.mp4",
    )
    db_session.add(concept)
    db_session.commit()
    return concept


@pytest.fixture
def sample_concept_with_dependencies(db_session: Session):
    """Create concepts with dependency relationships."""
    prerequisite = Concept(
        id="concept-prereq",
        name="SSH Keys",
        explanation="Public-private key pairs for authentication",
        intuition="SSH keys are like a lock and key system",
        example="Generating SSH key pair for SFTP authentication",
        common_mistake="Not protecting private keys properly",
        why_it_matters="Foundation for secure authentication",
        checkpoint_question="How do SSH keys enable passwordless authentication?",
        source_reference="Day1-Recording.mp4",
    )
    
    dependent = Concept(
        id="concept-dependent",
        name="SFTP Authentication",
        explanation="Using SSH keys to authenticate SFTP connections",
        intuition="SFTP authentication builds on SSH key infrastructure",
        example="Configuring SFTP server to accept key-based auth",
        common_mistake="Using weak key algorithms",
        why_it_matters="Enables automated secure file transfers",
        checkpoint_question="What are the steps in SFTP key-based authentication?",
        source_reference="Day2-Recording.mp4",
    )
    
    db_session.add(prerequisite)
    db_session.add(dependent)
    db_session.commit()
    
    edge = ConceptEdge(
        source_concept_id=prerequisite.id,
        target_concept_id=dependent.id,
        edge_type="depends_on",
    )
    db_session.add(edge)
    db_session.commit()
    
    return prerequisite, dependent


@pytest.fixture
def sample_learner_profile(db_session: Session, sample_concept: Concept):
    """Create a sample learner profile."""
    profile = LearnerProfile(
        user_id="test-user",
        concept_id=sample_concept.id,
        accuracy=0.5,
        response_time_ms=10000.0,
        retries=2,
        confidence=60,
        next_review_at=datetime.utcnow(),
    )
    db_session.add(profile)
    db_session.commit()
    return profile


@pytest.fixture
def sample_learning_attempts(db_session: Session, sample_concept: Concept):
    """Create sample learning attempts with various patterns."""
    attempts = []
    
    # Correct answer with high confidence and fast response
    attempts.append(LearningAttempt(
        user_id="test-user",
        concept_id=sample_concept.id,
        answer="SFTP uses SSH for encryption and authentication",
        is_correct=True,
        feedback="Excellent understanding",
        response_time_ms=8000.0,
        confidence=90,
        created_at=datetime.utcnow() - timedelta(minutes=30),
    ))
    
    # Correct answer with low confidence (lucky guess)
    attempts.append(LearningAttempt(
        user_id="test-user",
        concept_id=sample_concept.id,
        answer="SFTP is secure",
        is_correct=True,
        feedback="Correct but lacks detail",
        response_time_ms=15000.0,
        confidence=35,
        created_at=datetime.utcnow() - timedelta(minutes=20),
    ))
    
    # Incorrect answer with high confidence (false confidence)
    attempts.append(LearningAttempt(
        user_id="test-user",
        concept_id=sample_concept.id,
        answer="SFTP is the same as FTPS",
        is_correct=False,
        feedback="Common misconception",
        response_time_ms=5000.0,
        confidence=85,
        created_at=datetime.utcnow() - timedelta(minutes=10),
    ))
    
    for attempt in attempts:
        db_session.add(attempt)
    db_session.commit()
    return attempts


@pytest.fixture
def sample_source_file(db_session: Session):
    """Create a sample source file."""
    source_file = SourceFile(
        id="file-1",
        job_id="job-1",
        path="Day1-Recording.mp4",
        folder="Webex Recordings/Day1",
        extension=".mp4",
        file_type="video",
        is_video=True,
        recording_day="Day1",
        size_bytes=1024000,
    )
    db_session.add(source_file)
    db_session.commit()
    return source_file


@pytest.fixture
def sample_content_chunks(db_session: Session, sample_source_file: SourceFile):
    """Create sample content chunks with various types."""
    chunks = []
    
    # Concept definition chunk
    chunks.append(ContentChunk(
        source_file_id=sample_source_file.id,
        chunk_type="concept_definition",
        text="SFTP is a network protocol that provides file access, transfer, and management over a secure channel.",
        source_reference="Day1-Recording.mp4@120-180s",
        embedding_json="[0.1, 0.2, 0.3]",
    ))
    
    # Concept example chunk
    chunks.append(ContentChunk(
        source_file_id=sample_source_file.id,
        chunk_type="concept_example",
        text="For example, when transferring EDI 850 purchase orders, SFTP ensures the data is encrypted in transit.",
        source_reference="Day1-Recording.mp4@180-240s",
        embedding_json="[0.2, 0.3, 0.4]",
    ))
    
    # Edge case chunk
    chunks.append(ContentChunk(
        source_file_id=sample_source_file.id,
        chunk_type="edge_case",
        text="If the SSH key permissions are too open (e.g., 644), SFTP authentication will fail for security reasons.",
        source_reference="Day1-Recording.mp4@240-300s",
        embedding_json="[0.3, 0.4, 0.5]",
    ))
    
    # Concept bundle chunk
    chunks.append(ContentChunk(
        source_file_id=sample_source_file.id,
        chunk_type="concept_bundle",
        text='{"explanation": "SFTP provides secure file transfer", "example": "EDI document exchange", "mistake": "Confusing with FTPS"}',
        source_reference="Day1-Recording.mp4@300-360s",
        embedding_json="[0.4, 0.5, 0.6]",
    ))
    
    # Checkpoint question chunk
    chunks.append(ContentChunk(
        source_file_id=sample_source_file.id,
        chunk_type="checkpoint_question",
        text="What security mechanisms does SFTP use and how do they differ from FTPS?",
        source_reference="Day1-Recording.mp4@360-420s",
        embedding_json="[0.5, 0.6, 0.7]",
    ))
    
    for chunk in chunks:
        db_session.add(chunk)
    db_session.commit()
    return chunks

# Made with Bob
