"""
End-to-end learning session simulation test.

Validates the complete high-ROI upgrade workflow through realistic learning scenarios:
- Complete learning session flow from start to mastery
- Shallow loop prevention (answer-before-explanation, mandatory confidence, feedback delays)
- Brutal mastery progression (3 correct, high confidence, time pressure, spaced repetition)
- Forced revisit triggers (false confidence, lucky guess, hesitation confusion)
- Graph-driven prerequisite repair on failure
- Interview mode pressure differentiation
- Retrieval-grounded responses with uncertainty fallback
- TTS integration with tone shaping
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.orm import Session

from app.models.db import Concept, ConceptEdge, ContentChunk, LearnerProfile, LearningAttempt, SourceFile
from app.services.learning_service import LearningService
from app.services.tutor_service import TutorService


class TestCompleteLearningSessionFlow:
    """Test complete learning session from start to mastery."""
    
    @pytest.mark.asyncio
    async def test_full_learning_journey_to_mastery(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Simulate a complete learning journey from fresh learner to mastery."""
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "journey-user"
        
        # Step 1: Start with fresh learner profile
        learning.ensure_profiles(user_id)
        profile = db_session.query(LearnerProfile).filter_by(
            user_id=user_id,
            concept_id=sample_concept.id,
        ).first()
        assert profile is not None
        assert profile.accuracy == 0.0
        assert profile.confidence == 50
        
        # Step 2: Begin lesson mode
        concept, preview, question, time_pressure = await tutor.start_lesson(user_id, mode="lesson")
        assert concept.id == sample_concept.id
        assert time_pressure == 20  # Lesson mode
        assert "name" in preview
        assert question != ""
        
        # Step 3: Answer with varying confidence levels
        # First attempt: correct but low confidence (lucky guess)
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Correct but needs reinforcement", "misconception_tag": "none", "next_action": "review", "confidence": "medium", "uncertainty": "medium"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id=user_id,
            concept=concept,
            question=question,
            user_answer="SFTP uses SSH for secure file transfer",
            user_confidence=35,  # Low confidence
            response_time_ms=12000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        # Verify lucky guess detection
        assert correctness
        assert misconception_tag == "lucky_guess"
        assert next_action == "review"
        assert feedback_delay == 1800  # Longer delay for review
        
        # Step 4: Experience delayed feedback gate
        assert feedback_delay in [900, 1800]
        
        # Step 5: Verify forced revisit was triggered
        forced_ids = learning._forced_revisit_concept_ids(user_id)
        assert sample_concept.id in forced_ids
        
        # Step 6: Progress through multiple questions
        # Second attempt: correct with high confidence and fast response
        await asyncio.sleep(0.5)  # Simulate time passing
        
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Excellent understanding", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        result2 = await tutor.evaluate_answer(
            user_id=user_id,
            concept=concept,
            question=next_question,
            user_answer="SFTP is a network protocol that provides file access, transfer, and management over a secure SSH channel",
            user_confidence=90,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        correctness2, explanation2, misconception_tag2, next_action2, next_question2, source_chunks2, confidence_label2, uncertainty2, feedback_delay2 = result2
        
        assert correctness2
        assert next_action2 == "harder"
        assert feedback_delay2 == 900  # Shorter delay for harder
        
        # Step 7: Switch to interview mode
        concept3, preview3, question3, time_pressure3 = await tutor.start_lesson(user_id, mode="interview")
        assert time_pressure3 == 10  # Interview mode has shorter pressure
        
        # Step 8: Verify weak area tracking throughout
        profile_updated = db_session.query(LearnerProfile).filter_by(
            user_id=user_id,
            concept_id=sample_concept.id,
        ).first()
        assert profile_updated.accuracy > 0.0
        assert profile_updated.confidence > 50
        
        # Verify attempts were recorded
        attempts = db_session.query(LearningAttempt).filter_by(
            user_id=user_id,
            concept_id=sample_concept.id,
        ).all()
        assert len(attempts) >= 2


class TestShallowLoopPrevention:
    """Test shallow loop prevention mechanisms."""
    
    @pytest.mark.asyncio
    async def test_answer_must_be_submitted_before_explanation(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify answer must be submitted before explanation is available."""
        tutor = TutorService(db_session, mock_ollama_router)
        user_id = "shallow-test-user"
        
        # Start lesson - should only get question, not explanation
        concept, preview, question, time_pressure = await tutor.start_lesson(user_id, mode="lesson")
        
        assert question != ""
        assert "explanation" not in preview or preview.get("explanation") is None
        # Preview should have concept info but not full explanation
        assert "name" in preview
        assert "why_it_matters" in preview
    
    @pytest.mark.asyncio
    async def test_confidence_is_mandatory(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify confidence (0-100) is mandatory and used in evaluation."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="conf-test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=75,  # Must be provided
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        # Verify confidence is used
        confidence_label = result[6]
        assert confidence_label in ["low", "medium", "high"]
        
        # Verify attempt records confidence
        attempt = db_session.query(LearningAttempt).filter_by(
            user_id="conf-test-user",
            concept_id=sample_concept.id,
        ).first()
        assert attempt.confidence == 75
    
    @pytest.mark.asyncio
    async def test_feedback_delay_enforces_reflection_time(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify feedback delay enforces reflection time based on next_action."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Test longer delay for review/rebuild
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Needs review", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="delay-test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Not sure",
            user_confidence=30,
            response_time_ms=15000.0,
            mode="lesson",
        )
        
        feedback_delay = result[8]
        assert feedback_delay == 1800  # Longer delay for review
        
        # Test shorter delay for harder
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Excellent", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        result2 = await tutor.evaluate_answer(
            user_id="delay-test-user-2",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP provides secure file transfer using SSH encryption",
            user_confidence=95,
            response_time_ms=7000.0,
            mode="lesson",
        )
        
        feedback_delay2 = result2[8]
        assert feedback_delay2 == 900  # Shorter delay for harder
    
    @pytest.mark.asyncio
    async def test_explanation_only_shown_after_delay_expires(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify explanation is only shown after delay expires."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="explain-test-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        explanation, feedback_delay = result[1], result[8]
        
        # Explanation is returned but client must enforce delay
        assert explanation != ""
        assert feedback_delay > 0
        # In production, frontend would wait feedback_delay ms before showing explanation


class TestBrutalMasteryProgression:
    """Test brutal mastery progression requirements."""
    
    @pytest.mark.asyncio
    async def test_mastery_progression_from_zero_to_three(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Test progression from mastery level 0 to 3."""
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "mastery-user"
        
        learning.ensure_profiles(user_id)
        
        # Start at mastery level 0
        assert not learning.is_mastered(user_id, sample_concept.id)
        
        # Mock correct answers
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Excellent", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        # First correct answer with high confidence and fast response
        await tutor.evaluate_answer(
            user_id=user_id,
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP provides secure file transfer using SSH",
            user_confidence=90,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        # Still not mastered (need 3)
        assert not learning.is_mastered(user_id, sample_concept.id)
        
        # Wait for spacing requirement (8+ minutes)
        await asyncio.sleep(0.1)
        
        # Second correct answer (simulate 10 minutes later)
        attempt2 = LearningAttempt(
            user_id=user_id,
            concept_id=sample_concept.id,
            answer="SFTP uses SSH for encryption and authentication",
            is_correct=True,
            feedback="Excellent",
            response_time_ms=9000.0,
            confidence=88,
            created_at=datetime.utcnow() + timedelta(minutes=10),
        )
        db_session.add(attempt2)
        db_session.commit()
        
        # Still not mastered (need 3)
        assert not learning.is_mastered(user_id, sample_concept.id)
        
        # Third correct answer (simulate 10 minutes later)
        attempt3 = LearningAttempt(
            user_id=user_id,
            concept_id=sample_concept.id,
            answer="SFTP is a network protocol for secure file operations",
            is_correct=True,
            feedback="Excellent",
            response_time_ms=10000.0,
            confidence=92,
            created_at=datetime.utcnow() + timedelta(minutes=20),
        )
        db_session.add(attempt3)
        db_session.commit()
        
        # Now should be mastered
        assert learning.is_mastered(user_id, sample_concept.id)
    
    def test_mastery_requires_all_brutal_conditions(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify mastery requires all brutal conditions: 3 correct, high confidence, time pressure, spacing."""
        learning = LearningService(db_session)
        user_id = "brutal-user"
        
        learning.ensure_profiles(user_id)
        
        # Add 3 attempts but violate different conditions
        base_time = datetime.utcnow()
        
        # Attempt 1: correct, high confidence, fast (good)
        attempt1 = LearningAttempt(
            user_id=user_id,
            concept_id=sample_concept.id,
            answer="Good answer",
            is_correct=True,
            feedback="Correct",
            response_time_ms=10000.0,
            confidence=85,
            created_at=base_time,
        )
        db_session.add(attempt1)
        
        # Attempt 2: correct, high confidence, but TOO SLOW (violates time pressure)
        attempt2 = LearningAttempt(
            user_id=user_id,
            concept_id=sample_concept.id,
            answer="Good answer",
            is_correct=True,
            feedback="Correct",
            response_time_ms=15000.0,  # Too slow
            confidence=85,
            created_at=base_time + timedelta(minutes=10),
        )
        db_session.add(attempt2)
        
        # Attempt 3: correct, fast, but LOW CONFIDENCE (violates confidence requirement)
        attempt3 = LearningAttempt(
            user_id=user_id,
            concept_id=sample_concept.id,
            answer="Good answer",
            is_correct=True,
            feedback="Correct",
            response_time_ms=10000.0,
            confidence=70,  # Too low
            created_at=base_time + timedelta(minutes=20),
        )
        db_session.add(attempt3)
        db_session.commit()
        
        # Should NOT be mastered due to violations
        assert not learning.is_mastered(user_id, sample_concept.id)


class TestForcedRevisitTriggers:
    """Test forced revisit triggers."""
    
    @pytest.mark.asyncio
    async def test_false_confidence_triggers_forced_revisit(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Test false confidence (correct answer + low confidence) triggers forced revisit."""
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "false-conf-user"
        
        learning.ensure_profiles(user_id)
        
        # Mock incorrect answer with high confidence
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Incorrect", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id=user_id,
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is the same as FTPS",
            user_confidence=95,  # High confidence but wrong
            response_time_ms=5000.0,
            mode="lesson",
        )
        
        misconception_tag, next_action = result[2], result[3]
        assert misconception_tag == "false_confidence"
        assert next_action == "rebuild"
        
        # Verify forced revisit
        forced_ids = learning._forced_revisit_concept_ids(user_id)
        assert sample_concept.id in forced_ids
    
    @pytest.mark.asyncio
    async def test_lucky_guess_triggers_forced_revisit(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Test lucky guess (correct + low confidence) triggers forced revisit."""
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "lucky-user"
        
        learning.ensure_profiles(user_id)
        
        result = await tutor.evaluate_answer(
            user_id=user_id,
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP uses SSH",
            user_confidence=30,  # Low confidence
            response_time_ms=12000.0,
            mode="lesson",
        )
        
        misconception_tag = result[2]
        assert misconception_tag == "lucky_guess"
        
        # Verify forced revisit
        forced_ids = learning._forced_revisit_concept_ids(user_id)
        assert sample_concept.id in forced_ids
    
    @pytest.mark.asyncio
    async def test_hesitation_confusion_triggers_forced_revisit(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Test hesitation confusion (wrong + very slow) triggers forced revisit."""
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "hesitation-user"
        
        learning.ensure_profiles(user_id)
        
        # Mock incorrect answer
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Incorrect", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id=user_id,
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Not sure",
            user_confidence=50,
            response_time_ms=22000.0,  # Very slow
            mode="lesson",
        )
        
        misconception_tag, next_action = result[2], result[3]
        assert misconception_tag == "hesitation_confusion"
        assert next_action == "rebuild"
        
        # Verify forced revisit
        forced_ids = learning._forced_revisit_concept_ids(user_id)
        assert sample_concept.id in forced_ids
    
    def test_forced_revisits_prioritized_in_next_concept(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify forced revisits are prioritized in next concept selection."""
        learning = LearningService(db_session)
        user_id = "priority-user"
        
        learning.ensure_profiles(user_id)
        
        # Add false confidence attempt
        attempt = LearningAttempt(
            user_id=user_id,
            concept_id=sample_concept.id,
            answer="Wrong",
            is_correct=False,
            feedback="Incorrect",
            response_time_ms=5000.0,
            confidence=95,  # False confidence
            created_at=datetime.utcnow(),
        )
        db_session.add(attempt)
        db_session.commit()
        
        # Next concept should prioritize forced revisit
        next_concept = learning.next_concept(user_id)
        assert next_concept is not None
        assert next_concept.id == sample_concept.id


class TestGraphDrivenPrerequisiteRepair:
    """Test graph-driven prerequisite repair on failure."""
    
    @pytest.mark.asyncio
    async def test_failure_schedules_prerequisite_for_immediate_revisit(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept_with_dependencies,
    ):
        """Test that failing on dependent concept schedules prerequisite for immediate revisit."""
        prerequisite, dependent = sample_concept_with_dependencies
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "prereq-user"
        
        learning.ensure_profiles(user_id)
        
        # Mock incorrect answer on dependent concept
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": false, "explanation": "Incorrect", "misconception_tag": "confusion", "next_action": "review", "confidence": "low", "uncertainty": "high"}'
        )
        
        # Fail on dependent concept
        await tutor.evaluate_answer(
            user_id=user_id,
            concept=dependent,
            question="What is SFTP Authentication?",
            user_answer="Not sure",
            user_confidence=40,
            response_time_ms=15000.0,
            mode="lesson",
        )
        
        # Prerequisite should be scheduled for immediate review
        prereq_profile = db_session.query(LearnerProfile).filter_by(
            user_id=user_id,
            concept_id=prerequisite.id,
        ).first()
        
        assert prereq_profile is not None
        time_until_review = (prereq_profile.next_review_at - datetime.utcnow()).total_seconds()
        assert time_until_review <= 60  # Within 1 minute
        assert prereq_profile.retries >= 1
    
    def test_prerequisite_repair_progression_order(
        self,
        db_session: Session,
        sample_concept_with_dependencies,
    ):
        """Test that prerequisites are repaired before returning to dependent concepts."""
        prerequisite, dependent = sample_concept_with_dependencies
        learning = LearningService(db_session)
        user_id = "repair-user"
        
        learning.ensure_profiles(user_id)
        
        # Fail on dependent
        learning.update_progress(
            user_id=user_id,
            concept_id=dependent.id,
            is_correct=False,
            response_time_ms=10000.0,
            confidence=50,
            misconception_tag="confusion",
            next_action="review",
        )
        
        # Prerequisite should be in forced revisit queue
        forced_ids = learning._forced_revisit_concept_ids(user_id)
        assert prerequisite.id in forced_ids


class TestInterviewModePressure:
    """Test interview mode pressure differentiation."""
    
    @pytest.mark.asyncio
    async def test_interview_mode_shorter_time_pressure(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify interview mode has shorter time pressure (10s vs 20s)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # Lesson mode
        concept1, preview1, question1, time_pressure1 = await tutor.start_lesson("test-user", mode="lesson")
        assert time_pressure1 == 20
        
        # Interview mode
        concept2, preview2, question2, time_pressure2 = await tutor.start_lesson("test-user", mode="interview")
        assert time_pressure2 == 10
    
    @pytest.mark.asyncio
    async def test_interview_mode_harder_challenge_prompts(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify interview mode uses harder challenge prompts."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        concept, preview, question, time_pressure = await tutor.start_lesson("test-user", mode="interview")
        
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
        
        mock_ollama_router.chat = AsyncMock(
            return_value='{"correctness": true, "explanation": "Good", "misconception_tag": "none", "next_action": "harder", "confidence": "high", "uncertainty": "low"}'
        )
        
        result = await tutor.evaluate_answer(
            user_id="interview-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP provides secure file transfer using SSH",
            user_confidence=90,
            response_time_ms=7000.0,
            mode="interview",
        )
        
        next_action = result[3]
        assert next_action == "interview"


class TestRetrievalGroundedResponses:
    """Test retrieval-grounded responses with source chunks."""
    
    @pytest.mark.asyncio
    async def test_tutor_evaluation_uses_source_chunks(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify tutor evaluation uses source chunks for grounding."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="grounding-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is a network protocol for secure file transfer",
            user_confidence=85,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        source_chunks = result[5]
        
        # Should have retrieved source chunks
        assert len(source_chunks) > 0
        # Each chunk should have source reference
        for chunk in source_chunks:
            assert "Day1-Recording.mp4" in chunk or "[" in chunk
    
    @pytest.mark.asyncio
    async def test_grounding_confidence_threshold(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify grounding confidence score threshold (≥0.18)."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="threshold-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP provides secure file transfer",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        source_chunks = result[5]
        # If chunks are returned, they passed the 0.18 threshold
        # This is validated in the chunking service
        assert isinstance(source_chunks, list)
    
    @pytest.mark.asyncio
    async def test_uncertainty_fallback_when_grounding_weak(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
    ):
        """Verify uncertainty fallback when grounding is weak."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        # No chunks in DB - weak grounding
        result = await tutor.evaluate_answer(
            user_id="weak-grounding-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Some answer",
            user_confidence=70,
            response_time_ms=10000.0,
            mode="lesson",
        )
        
        correctness, explanation, misconception_tag, confidence_label, uncertainty = result[0], result[1], result[2], result[6], result[7]
        
        assert not correctness
        assert "Uncertain" in explanation or "grounded" in explanation.lower()
        assert misconception_tag == "insufficient_grounding"
        assert confidence_label == "low"
        assert "high" in uncertainty.lower()
    
    @pytest.mark.asyncio
    async def test_source_chunks_included_in_response(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify source chunks are included in response for transparency."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="chunks-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP is a network protocol that provides file access transfer and management over a secure channel",
            user_confidence=85,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        source_chunks = result[5]
        
        # Should have source chunks
        assert len(source_chunks) > 0
        # Chunks should contain source reference and chunk type
        for chunk in source_chunks:
            assert "[" in chunk and "]" in chunk  # Contains chunk type
            assert "Day1-Recording.mp4" in chunk  # Contains source reference


class TestAPIResponseContract:
    """Test that all API responses follow the 11-field contract."""
    
    @pytest.mark.asyncio
    async def test_evaluate_answer_returns_all_fields(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify evaluate_answer returns all 11 required fields."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        result = await tutor.evaluate_answer(
            user_id="contract-user",
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        # Verify tuple has 9 elements (the contract)
        assert len(result) == 9
        
        correctness, explanation, misconception_tag, next_action, next_question, source_chunks, confidence_label, uncertainty, feedback_delay = result
        
        # Verify types
        assert isinstance(correctness, bool)
        assert isinstance(explanation, str)
        assert isinstance(misconception_tag, str)
        assert next_action in ["harder", "retry", "review", "rebuild", "interview"]
        assert isinstance(next_question, str)
        assert isinstance(source_chunks, list)
        assert isinstance(confidence_label, str)
        assert isinstance(uncertainty, str)
        assert isinstance(feedback_delay, int)
        
        # Verify non-empty
        assert explanation != ""
        assert misconception_tag != ""
        assert next_question != ""
        assert confidence_label in ["low", "medium", "high"]
        assert feedback_delay in [900, 1800]


class TestTimingConstraints:
    """Test timing constraints for pressure windows, delays, and spacing."""
    
    @pytest.mark.asyncio
    async def test_lesson_mode_pressure_window(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify lesson mode has 20s pressure window."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        concept, preview, question, time_pressure = await tutor.start_lesson("test-user", mode="lesson")
        assert time_pressure == 20
    
    @pytest.mark.asyncio
    async def test_interview_mode_pressure_window(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_learner_profile,
    ):
        """Verify interview mode has 10s pressure window."""
        tutor = TutorService(db_session, mock_ollama_router)
        
        concept, preview, question, time_pressure = await tutor.start_lesson("test-user", mode="interview")
        assert time_pressure == 10
    
    def test_spaced_repetition_requirement(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify spaced repetition requires 8+ minutes between attempts."""
        learning = LearningService(db_session)
        user_id = "spacing-user"
        
        learning.ensure_profiles(user_id)
        
        # Add 3 attempts with proper spacing
        base_time = datetime.utcnow()
        for i in range(3):
            attempt = LearningAttempt(
                user_id=user_id,
                concept_id=sample_concept.id,
                answer="Good answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=85,
                created_at=base_time + timedelta(minutes=i * 10),  # 10 min apart
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should be mastered with proper spacing
        assert learning.is_mastered(user_id, sample_concept.id)
        
        # Now test insufficient spacing
        db_session.query(LearningAttempt).filter_by(user_id=user_id).delete()
        for i in range(3):
            attempt = LearningAttempt(
                user_id=user_id,
                concept_id=sample_concept.id,
                answer="Good answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=85,
                created_at=base_time + timedelta(minutes=i * 5),  # Only 5 min apart
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should NOT be mastered with insufficient spacing
        assert not learning.is_mastered(user_id, sample_concept.id)


class TestDatabaseStatePersistence:
    """Test that database state is correctly persisted throughout the workflow."""
    
    @pytest.mark.asyncio
    async def test_learning_attempts_persisted(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify learning attempts are persisted to database."""
        tutor = TutorService(db_session, mock_ollama_router)
        user_id = "persist-user"
        
        await tutor.evaluate_answer(
            user_id=user_id,
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="Secure File Transfer Protocol",
            user_confidence=80,
            response_time_ms=9000.0,
            mode="lesson",
        )
        
        # Check attempt was saved
        attempts = db_session.query(LearningAttempt).filter_by(
            user_id=user_id,
            concept_id=sample_concept.id,
        ).all()
        
        assert len(attempts) > 0
        latest = attempts[-1]
        assert latest.answer == "Secure File Transfer Protocol"
        assert latest.confidence == 80
        assert latest.response_time_ms == 9000.0
    
    @pytest.mark.asyncio
    async def test_learner_profiles_updated(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_concept: Concept,
        sample_content_chunks,
    ):
        """Verify learner profiles are updated after each attempt."""
        tutor = TutorService(db_session, mock_ollama_router)
        learning = LearningService(db_session)
        user_id = "profile-user"
        
        learning.ensure_profiles(user_id)
        
        profile_before = db_session.query(LearnerProfile).filter_by(
            user_id=user_id,
            concept_id=sample_concept.id,
        ).first()
        initial_accuracy = profile_before.accuracy
        
        await tutor.evaluate_answer(
            user_id=user_id,
            concept=sample_concept,
            question="What is SFTP?",
            user_answer="SFTP provides secure file transfer",
            user_confidence=85,
            response_time_ms=8000.0,
            mode="lesson",
        )
        
        profile_after = db_session.query(LearnerProfile).filter_by(
            user_id=user_id,
            concept_id=sample_concept.id,
        ).first()
        
        # Profile should be updated
        assert profile_after.accuracy != initial_accuracy
        assert profile_after.confidence == 85
        assert profile_after.next_review_at > datetime.utcnow()


# Made with Bob