"""
Test suite for TutorService - validates high-ROI tutor upgrades.

Tests cover:
1. Answer-before-explanation contract enforcement
2. Mandatory 0-100 confidence scoring
3. Delayed feedback gate behavior
4. New tutor response contract fields
5. Retrieval-first guardrails and uncertainty fallback
6. Tutor refuses freestyling without strong source evidence
7. Interview mode differentiation
"""
from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.orm import Session

from app.models.db import Concept, ContentChunk, LearningAttempt
from app.services.tutor_service import TutorService


class TestAnswerBeforeExplanation:
    """Test that tutor enforces answer-before-explanation contract."""
    
    @pytest.mark.asyncio
    async def test_start_lesson_returns_question_first(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify start_lesson returns question before any explanation."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        concept, preview, question, time_pressure = await tutor.start_lesson("test-user", mode="lesson")
        
        assert concept is not None
        assert concept.id == sample_concept.id
        assert question != ""
        assert "?" in question or "Explain" in question
        assert time_pressure == 20  # Lesson mode has 20s pressure
        
        # Preview should contain concept info but not full explanation yet
        assert "name" in preview
        assert preview["name"] == sample_concept.name
    
    @pytest.mark.asyncio
    async def test_interview_mode_has_shorter_pressure_window(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify interview mode has shorter time pressure (10s vs 20s)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        concept, preview, question, time_pressure = await tutor.start_lesson("test-user", mode="interview")
        
        assert time_pressure == 10  # Interview mode has 10s pressure
        assert "interview" in question.lower() or "defend" in question.lower()


class TestMandatoryConfidenceScoring:
    """Test that confidence scoring is mandatory and validated."""
    
    @pytest.mark.asyncio
    async def test_confidence_must_be_0_to_100(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify confidence is enforced in 0-100 range."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Test with valid confidence
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=75,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        # Verify confidence is used in evaluation
        assert confidence_label in ["low", "medium", "high"]
        assert uncertainty in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_false_confidence_detection(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify false confidence is detected (wrong answer + high confidence)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock incorrect answer evaluation
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Incorrect", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is the same as FTPS",
            user_confidence=90,  # High confidence but wrong
            response_time_ms=5000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        assert not correctness
        assert misconception_tag == "false_confidence"
        assert next_action == "rebuild"
    
    @pytest.mark.asyncio
    async def test_lucky_guess_detection(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify lucky guess is detected (correct answer + low confidence)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol using SSH",
            user_confidence=30,  # Low confidence but correct
            response_time_ms=12000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        assert correctness
        assert misconception_tag == "lucky_guess"
        assert next_action == "review"


class TestDelayedFeedbackGate:
    """Test delayed feedback behavior based on next_action."""
    
    @pytest.mark.asyncio
    async def test_longer_delay_for_retry_review_rebuild(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify longer feedback delay (1800ms) for retry/review/rebuild."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock review action
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Needs review", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Not sure",
            user_confidence=20,
            response_time_ms=15000.0,
            mode="lesson",
        )
        
        feedback_delay = result[8]
        assert feedback_delay == 1800
    
    @pytest.mark.asyncio
    async def test_shorter_delay_for_harder_interview(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify shorter feedback delay (900ms) for harder/interview actions."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock harder action
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Excellent", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol using SSH for encryption and authentication",
            user_confidence=95,
            response_time_ms=7000.0,
            mode="lesson",
        )
        
        feedback_delay = result[8]
        assert feedback_delay == 900


class TestTutorResponseContract:
    """Test new tutor response contract fields."""
    
    @pytest.mark.asyncio
    async def test_response_includes_all_required_fields(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify response includes all contract fields."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        # Verify all fields are present
        assert isinstance(correctness, bool)
        assert isinstance(explanation, str)
        assert isinstance(misconception_tag, str)
        assert next_action in ["harder", "retry", "review", "rebuild", "interview"]
        assert isinstance(next_question, str)
        assert isinstance(source_chunks, list)
        assert isinstance(confidence_label, str)
        assert isinstance(uncertainty, str)
        assert isinstance(feedback_delay, int)
    
    @pytest.mark.asyncio
    async def test_source_chunks_included_in_response(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify source chunks are included in response for grounding."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is a network protocol for secure file transfer",
            user_confidence=85,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        source_chunks = result[5]
        
        # Should have retrieved relevant chunks
        assert len(source_chunks) > 0
        # Each chunk should have source reference
        for chunk in source_chunks:
            assert "Day1-Recording.mp4" in chunk or "[" in chunk


class TestRetrievalFirstGuardrails:
    """Test retrieval-first guardrails and uncertainty fallback."""
    
    @pytest.mark.asyncio
    async def test_weak_grounding_triggers_uncertainty(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
    ):
        """Verify weak source grounding triggers uncertainty response."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # No chunks in DB - weak grounding
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Some answer",
            user_confidence=70,
            response_time_ms=10000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        assert not correctness
        assert "Uncertain" in explanation or "grounded" in explanation.lower()
        assert misconception_tag == "insufficient_grounding"
        assert next_action == "review"
        assert confidence_label == "low"
        assert "high" in uncertainty.lower()
    
    @pytest.mark.asyncio
    async def test_strong_grounding_enables_evaluation(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify strong source grounding enables proper evaluation."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is a network protocol that provides file access transfer and management over a secure channel",
            user_confidence=85,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, source_chunks, confidence_label, uncertainty, feedback_delay = result[0], result[1], result[2], result[3], result[5], result[6], result[7], result[8]
        
        # Should have strong grounding
        assert len(source_chunks) > 0
        # Should not be insufficient_grounding
        assert misconception_tag != "insufficient_grounding"


class TestTutorRefusesFreestyling:
    """Test that tutor refuses to freestyle without strong source evidence."""
    
    @pytest.mark.asyncio
    async def test_heuristic_eval_requires_source_overlap(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify heuristic evaluation requires source token overlap."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock model failure to trigger heuristic
        mock_ollama_router.chat = AsyncMock(side_effect=Exception("Model error"))
        
        # Answer with no source overlap
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="xyz abc def",
            user_confidence=50,
            response_time_ms=10000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag = result[0], result[1], result[2]
        
        assert not correctness
        assert misconception_tag == "insufficient_grounding"
        assert "grounded" in explanation.lower() or "source" in explanation.lower()
    
    @pytest.mark.asyncio
    async def test_model_eval_enforces_source_chunks(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify model evaluation system prompt enforces source chunk usage."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        # Verify chat was called with source chunks in prompt
        mock_ollama_router.chat.assert_called_once()
        call_args = mock_ollama_router.chat.call_args
        system_prompt = call_args[0][1]
        user_prompt = call_args[0][2]
        
        assert "source chunks" in system_prompt.lower()
        assert "MUST use only provided source chunks" in system_prompt
        assert "Grounding source chunks:" in user_prompt


class TestInterviewMode:
    """Test interview mode differentiation."""
    
    @pytest.mark.asyncio
    async def test_interview_mode_uses_hard_follow_up(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify interview mode uses hard_follow_up questions."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        concept, preview, question, time_pressure = await tutor.start_lesson("test-user", mode="interview")
        
        assert time_pressure == 10
        # Should use hard_follow_up or interview-style question
        assert (
            question == sample_concept.hard_follow_up
            or "interview" in question.lower()
            or "defend" in question.lower()
            or "failure" in question.lower()
        )
    
    @pytest.mark.asyncio
    async def test_interview_mode_converts_harder_to_interview_action(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify interview mode converts 'harder' action to 'interview'."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock harder action
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Good", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol using SSH",
            user_confidence=90,
            response_time_ms=7000.0,
            mode="interview",
        )
        
        next_action = result[3]
        assert next_action == "interview"


class TestConfusionDetection:
    """Test confusion detection logic."""
    
    @pytest.mark.asyncio
    async def test_fragile_understanding_detection(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify fragile understanding is detected (correct but low confidence or slow)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Correct but low confidence
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP uses SSH for secure file transfer",
            user_confidence=60,
            response_time_ms=15000.0,
            mode="lesson",
        )
        
        misconception_tag = result[2]
        assert misconception_tag == "fragile_understanding"
    
    @pytest.mark.asyncio
    async def test_hesitation_confusion_detection(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify hesitation confusion is detected (wrong + very slow)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock incorrect answer
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Incorrect", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Not sure about this",
            user_confidence=40,
            response_time_ms=22000.0,  # Very slow
            mode="lesson",
        )
        
        misconception_tag, next_action = result[2], result[3]
        assert misconception_tag == "hesitation_confusion"
        assert next_action == "rebuild"
    
    @pytest.mark.asyncio
    async def test_guessing_pattern_detection(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify guessing pattern is detected (wrong + very low confidence)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock incorrect answer
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Incorrect", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Maybe it's something with files",
            user_confidence=25,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        misconception_tag = result[2]
        assert misconception_tag == "guessing_pattern"


class TestNextActionAdjustments:
    """Test next action adjustments based on misconceptions."""
    
    @pytest.mark.asyncio
    async def test_rebuild_action_for_false_confidence(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify rebuild action is triggered for false confidence."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock incorrect answer
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Wrong", "misconception_tag": "confusion", "next_action": "retry", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is the same as FTPS",
            user_confidence=95,  # False confidence
            response_time_ms=5000.0,
            mode="lesson",
        )
        
        next_action, next_question = result[3], result[4]
        assert next_action == "rebuild"
        assert "thought you knew" in next_question.lower() or "rebuild" in next_question.lower()
    
    @pytest.mark.asyncio
    async def test_review_action_for_lucky_guess(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify review action is triggered for lucky guess."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP uses SSH",
            user_confidence=35,  # Lucky guess
            response_time_ms=10000.0,
            mode="lesson",
        )
        
        next_action = result[3]
        assert next_action == "review"
    
    @pytest.mark.asyncio
    async def test_harder_action_generates_stress_test_question(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify harder action generates stress-test question."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Mock correct answer with high confidence
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Excellent", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is a network protocol providing secure file transfer using SSH encryption",
            user_confidence=95,
            response_time_ms=7000.0,
            mode="lesson",
        )
        
        next_action, next_question = result[3], result[4]
        assert next_action == "harder"
        assert (
            next_question == sample_concept.hard_follow_up
            or "stress" in next_question.lower()
            or "fail" in next_question.lower()
        )


class TestLearningAttemptPersistence:
    """Test that learning attempts are persisted correctly."""
    
    @pytest.mark.asyncio
    async def test_attempt_saved_to_database(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify learning attempt is saved to database."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        await tutor.evaluate_answer(
            user_id="test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        # Check attempt was saved
        attempts = db_session.query(LearningAttempt).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).all()
        
        assert len(attempts) > 0
        latest = attempts[-1]
        assert latest.answer == "Secure File Transfer Protocol"
        assert latest.confidence == 80
        assert latest.response_time_ms == 9000.0

# Made with Bob
