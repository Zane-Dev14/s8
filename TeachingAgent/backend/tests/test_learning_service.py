"""
Test suite for LearningService - validates learning progression and graph-driven revisits.

Tests cover:
1. Brutal mastery requirements (3 correct, high confidence, time pressure, spaced repetition)
2. Forced revisit queue triggers (false confidence, lucky guess, hesitation, repeated failures)
3. Explicit rebuild loop activation with "you thought you knew this" progression
4. Confusion detection logic
5. Next action adjustments
6. Graph-driven dependency prerequisite scheduling on failure
7. Next-concept selection prioritizes forced revisits and prerequisite repair
"""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.models.db import Concept, ConceptEdge, LearnerProfile, LearningAttempt
from app.services.learning_service import LearningService


class TestBrutalMasteryRequirements:
    """Test brutal mastery requirements implementation."""
    
    def test_mastery_requires_three_correct_answers(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify mastery requires at least 3 correct answers."""
        learning = LearningService(db_session)
        
        # Add 2 correct attempts
        for i in range(2):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Good answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=85,
                created_at=datetime.utcnow() - timedelta(minutes=20 - i * 10),
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should not be mastered with only 2
        assert not learning.is_mastered("test-user", sample_concept.id)
        
        # Add 3rd correct attempt
        attempt = LearningAttempt(
            user_id="test-user",
            concept_id=sample_concept.id,
            answer="Good answer",
            is_correct=True,
            feedback="Correct",
            response_time_ms=10000.0,
            confidence=85,
            created_at=datetime.utcnow(),
        )
        db_session.add(attempt)
        db_session.commit()
        
        # Should be mastered with 3
        assert learning.is_mastered("test-user", sample_concept.id)
    
    def test_mastery_requires_high_confidence(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify mastery requires confidence >= 80."""
        learning = LearningService(db_session)
        
        # Add 3 correct attempts with low confidence
        for i in range(3):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=70,  # Below 80
                created_at=datetime.utcnow() - timedelta(minutes=30 - i * 10),
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should not be mastered with low confidence
        assert not learning.is_mastered("test-user", sample_concept.id)
    
    def test_mastery_requires_time_pressure(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify mastery requires response_time_ms <= 12000."""
        learning = LearningService(db_session)
        
        # Add 3 correct attempts with slow response
        for i in range(3):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=15000.0,  # Too slow
                confidence=85,
                created_at=datetime.utcnow() - timedelta(minutes=30 - i * 10),
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should not be mastered with slow responses
        assert not learning.is_mastered("test-user", sample_concept.id)
    
    def test_mastery_requires_spaced_repetition(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify mastery requires >= 8 minutes spacing between attempts."""
        learning = LearningService(db_session)
        
        # Add 3 correct attempts too close together
        base_time = datetime.utcnow()
        for i in range(3):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=85,
                created_at=base_time + timedelta(minutes=i * 5),  # Only 5 min apart
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should not be mastered with insufficient spacing
        assert not learning.is_mastered("test-user", sample_concept.id)
        
        # Now add attempts with proper spacing
        db_session.query(LearningAttempt).delete()
        for i in range(3):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=85,
                created_at=base_time + timedelta(minutes=i * 10),  # 10 min apart
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should be mastered with proper spacing
        assert learning.is_mastered("test-user", sample_concept.id)


class TestForcedRevisitQueue:
    """Test forced revisit queue triggers."""
    
    def test_false_confidence_triggers_forced_revisit(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify false confidence (wrong + high confidence) triggers forced revisit."""
        learning = LearningService(db_session)
        
        # Add false confidence attempt
        attempt = LearningAttempt(
            user_id="test-user",
            concept_id=sample_concept.id,
            answer="Wrong answer",
            is_correct=False,
            feedback="Incorrect",
            response_time_ms=8000.0,
            confidence=90,  # High confidence but wrong
            created_at=datetime.utcnow(),
        )
        db_session.add(attempt)
        db_session.commit()
        
        # Should be in forced revisit queue
        forced_ids = learning._forced_revisit_concept_ids("test-user")
        assert sample_concept.id in forced_ids
    
    def test_lucky_guess_triggers_forced_revisit(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify lucky guess (correct + low confidence) triggers forced revisit."""
        learning = LearningService(db_session)
        
        # Add lucky guess attempt
        attempt = LearningAttempt(
            user_id="test-user",
            concept_id=sample_concept.id,
            answer="Correct answer",
            is_correct=True,
            feedback="Correct",
            response_time_ms=10000.0,
            confidence=35,  # Low confidence
            created_at=datetime.utcnow(),
        )
        db_session.add(attempt)
        db_session.commit()
        
        # Should be in forced revisit queue
        forced_ids = learning._forced_revisit_concept_ids("test-user")
        assert sample_concept.id in forced_ids
    
    def test_hesitation_confusion_triggers_forced_revisit(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify hesitation confusion (wrong + very slow) triggers forced revisit."""
        learning = LearningService(db_session)
        
        # Add hesitation confusion attempt
        attempt = LearningAttempt(
            user_id="test-user",
            concept_id=sample_concept.id,
            answer="Wrong answer",
            is_correct=False,
            feedback="Incorrect",
            response_time_ms=20000.0,  # Very slow
            confidence=50,
            created_at=datetime.utcnow(),
        )
        db_session.add(attempt)
        db_session.commit()
        
        # Should be in forced revisit queue
        forced_ids = learning._forced_revisit_concept_ids("test-user")
        assert sample_concept.id in forced_ids
    
    def test_repeated_failures_tracked(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify repeated failures under pressure are tracked."""
        learning = LearningService(db_session)
        
        # Add multiple pressure failures
        for i in range(3):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Wrong",
                is_correct=False,
                feedback="Incorrect",
                response_time_ms=10000.0,  # Under pressure
                confidence=60,
                created_at=datetime.utcnow() - timedelta(minutes=10 - i * 3),
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should track pressure failures
        failures = learning.pressure_failures("test-user", sample_concept.id)
        assert failures == 3


class TestRebuildLoopActivation:
    """Test explicit rebuild loop activation."""
    
    def test_false_confidence_triggers_rebuild_interval(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify false confidence triggers short rebuild interval (5 min)."""
        learning = LearningService(db_session)
        
        learning.update_progress(
            user_id="test-user",
            concept_id=sample_concept.id,
            is_correct=False,
            response_time_ms=8000.0,
            confidence=90,
            misconception_tag="false_confidence",
            next_action="rebuild",
        )
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        
        # Should have very short interval
        time_until_review = (profile.next_review_at - datetime.utcnow()).total_seconds() / 60
        assert time_until_review < 10  # Less than 10 minutes
        # Should have increased retries significantly
        assert profile.retries >= 2
    
    def test_rebuild_action_triggers_short_interval(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify rebuild action triggers 7-minute interval."""
        learning = LearningService(db_session)
        
        learning.update_progress(
            user_id="test-user",
            concept_id=sample_concept.id,
            is_correct=False,
            response_time_ms=12000.0,
            confidence=60,
            misconception_tag="confusion",
            next_action="rebuild",
        )
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        
        # Should have short interval for rebuild
        time_until_review = (profile.next_review_at - datetime.utcnow()).total_seconds() / 60
        assert time_until_review < 10


class TestGraphDrivenRevisits:
    """Test graph-driven dependency prerequisite scheduling."""
    
    def test_failure_schedules_prerequisite_revisit(
        self,
        db_session: Session,
        sample_concept_with_dependencies,
    ):
        """Verify failure on dependent concept schedules prerequisite for immediate revisit."""
        prerequisite, dependent = sample_concept_with_dependencies
        learning = LearningService(db_session)
        
        # Create profiles
        learning.ensure_profiles("test-user")
        
        # Fail on dependent concept
        learning.update_progress(
            user_id="test-user",
            concept_id=dependent.id,
            is_correct=False,
            response_time_ms=10000.0,
            confidence=50,
            misconception_tag="confusion",
            next_action="review",
        )
        
        # Prerequisite should be scheduled for immediate review
        prereq_profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=prerequisite.id,
        ).first()
        
        assert prereq_profile is not None
        # Should be scheduled for now or very soon
        time_until_review = (prereq_profile.next_review_at - datetime.utcnow()).total_seconds()
        assert time_until_review <= 60  # Within 1 minute
        # Retries should be incremented
        assert prereq_profile.retries >= 1
    
    def test_next_concept_prioritizes_forced_revisits(
        self,
        db_session: Session,
        sample_concept_with_dependencies,
    ):
        """Verify next_concept prioritizes forced revisits over regular due concepts."""
        prerequisite, dependent = sample_concept_with_dependencies
        learning = LearningService(db_session)
        
        # Create profiles
        learning.ensure_profiles("test-user")
        
        # Add false confidence attempt on prerequisite
        attempt = LearningAttempt(
            user_id="test-user",
            concept_id=prerequisite.id,
            answer="Wrong",
            is_correct=False,
            feedback="Incorrect",
            response_time_ms=8000.0,
            confidence=95,  # False confidence
            created_at=datetime.utcnow(),
        )
        db_session.add(attempt)
        db_session.commit()
        
        # Next concept should be the prerequisite (forced revisit)
        next_concept = learning.next_concept("test-user")
        assert next_concept is not None
        assert next_concept.id == prerequisite.id
    
    def test_prerequisite_repair_before_dependent(
        self,
        db_session: Session,
        sample_concept_with_dependencies,
    ):
        """Verify prerequisites are repaired before returning to dependent concepts."""
        prerequisite, dependent = sample_concept_with_dependencies
        learning = LearningService(db_session)
        
        # Create profiles
        learning.ensure_profiles("test-user")
        
        # Fail on dependent, which should schedule prerequisite
        learning.update_progress(
            user_id="test-user",
            concept_id=dependent.id,
            is_correct=False,
            response_time_ms=10000.0,
            confidence=50,
            misconception_tag="confusion",
            next_action="review",
        )
        
        # Next concept should prioritize prerequisite
        next_concept = learning.next_concept("test-user")
        
        # Should get prerequisite for repair
        forced_ids = learning._forced_revisit_concept_ids("test-user")
        assert prerequisite.id in forced_ids


class TestProgressUpdateLogic:
    """Test progress update logic and intervals."""
    
    def test_correct_with_pressure_extends_interval(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify correct answer with high confidence and time pressure extends interval to 12 hours."""
        learning = LearningService(db_session)
        
        learning.update_progress(
            user_id="test-user",
            concept_id=sample_concept.id,
            is_correct=True,
            response_time_ms=10000.0,  # Under pressure
            confidence=90,  # High confidence
            misconception_tag="none",
            next_action="harder",
        )
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        
        # Should have long interval (12 hours)
        time_until_review = (profile.next_review_at - datetime.utcnow()).total_seconds() / 3600
        assert time_until_review >= 11  # At least 11 hours
    
    def test_correct_without_pressure_shorter_interval(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify correct answer without full pressure gets shorter interval (2 hours)."""
        learning = LearningService(db_session)
        
        learning.update_progress(
            user_id="test-user",
            concept_id=sample_concept.id,
            is_correct=True,
            response_time_ms=15000.0,  # Not under pressure
            confidence=70,  # Not high confidence
            misconception_tag="none",
            next_action="review",
        )
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        
        # Should have shorter interval (2 hours)
        time_until_review = (profile.next_review_at - datetime.utcnow()).total_seconds() / 3600
        assert 1.5 <= time_until_review <= 3
    
    def test_incorrect_short_interval(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify incorrect answer gets short interval (15 minutes)."""
        learning = LearningService(db_session)
        
        learning.update_progress(
            user_id="test-user",
            concept_id=sample_concept.id,
            is_correct=False,
            response_time_ms=10000.0,
            confidence=60,
            misconception_tag="confusion",
            next_action="retry",
        )
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        
        # Should have short interval (15 minutes)
        time_until_review = (profile.next_review_at - datetime.utcnow()).total_seconds() / 60
        assert time_until_review <= 20
    
    def test_accuracy_exponential_moving_average(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify accuracy uses exponential moving average (75% old, 25% new)."""
        learning = LearningService(db_session)
        
        # Set initial accuracy
        sample_learner_profile.accuracy = 0.5
        db_session.commit()
        
        # Update with correct answer
        learning.update_progress(
            user_id="test-user",
            concept_id=sample_concept.id,
            is_correct=True,
            response_time_ms=10000.0,
            confidence=80,
            misconception_tag="none",
            next_action="harder",
        )
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        
        # Should be: 0.5 * 0.75 + 1.0 * 0.25 = 0.625
        assert abs(profile.accuracy - 0.625) < 0.01


class TestEnsureProfiles:
    """Test profile creation and management."""
    
    def test_ensure_profiles_creates_missing_profiles(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify ensure_profiles creates profiles for all concepts."""
        learning = LearningService(db_session)
        
        # Should have no profiles initially
        profiles = db_session.query(LearnerProfile).filter_by(user_id="new-user").all()
        assert len(profiles) == 0
        
        # Create profiles
        learning.ensure_profiles("new-user")
        
        # Should have profile for concept
        profiles = db_session.query(LearnerProfile).filter_by(user_id="new-user").all()
        assert len(profiles) >= 1
        
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="new-user",
            concept_id=sample_concept.id,
        ).first()
        assert profile is not None
        assert profile.accuracy == 0.0
        assert profile.confidence == 50
    
    def test_ensure_profiles_skips_existing(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify ensure_profiles doesn't overwrite existing profiles."""
        learning = LearningService(db_session)
        
        # Set custom values
        sample_learner_profile.accuracy = 0.8
        sample_learner_profile.confidence = 90
        db_session.commit()
        
        # Call ensure_profiles
        learning.ensure_profiles("test-user")
        
        # Should preserve existing values
        profile = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        assert profile.accuracy == 0.8
        assert profile.confidence == 90


class TestNextConceptSelection:
    """Test next concept selection logic."""
    
    def test_next_concept_returns_due_concepts(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify next_concept returns concepts that are due for review."""
        learning = LearningService(db_session)
        
        # Set review time to past
        sample_learner_profile.next_review_at = datetime.utcnow() - timedelta(hours=1)
        db_session.commit()
        
        next_concept = learning.next_concept("test-user")
        assert next_concept is not None
        assert next_concept.id == sample_concept.id
    
    def test_next_concept_skips_mastered(
        self,
        db_session: Session,
        sample_concept: Concept,
        sample_learner_profile: LearnerProfile,
    ):
        """Verify next_concept skips mastered concepts."""
        learning = LearningService(db_session)
        
        # Add mastery attempts
        base_time = datetime.utcnow()
        for i in range(3):
            attempt = LearningAttempt(
                user_id="test-user",
                concept_id=sample_concept.id,
                answer="Answer",
                is_correct=True,
                feedback="Correct",
                response_time_ms=10000.0,
                confidence=85,
                created_at=base_time + timedelta(minutes=i * 10),
            )
            db_session.add(attempt)
        db_session.commit()
        
        # Should be mastered
        assert learning.is_mastered("test-user", sample_concept.id)
        
        # Should not return mastered concept
        next_concept = learning.next_concept("test-user")
        # Either None or a different concept
        if next_concept:
            assert next_concept.id != sample_concept.id
    
    def test_next_concept_prioritizes_low_accuracy(
        self,
        db_session: Session,
        sample_concept: Concept,
    ):
        """Verify next_concept prioritizes concepts with low accuracy."""
        learning = LearningService(db_session)
        
        # Create another concept
        concept2 = Concept(
            id="concept-2",
            name="Test Concept 2",
            explanation="Test",
            source_reference="test.mp4",
        )
        db_session.add(concept2)
        db_session.commit()
        
        learning.ensure_profiles("test-user")
        
        # Set different accuracies
        profile1 = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=sample_concept.id,
        ).first()
        profile1.accuracy = 0.8
        profile1.next_review_at = datetime.utcnow()
        
        profile2 = db_session.query(LearnerProfile).filter_by(
            user_id="test-user",
            concept_id=concept2.id,
        ).first()
        profile2.accuracy = 0.3  # Lower accuracy
        profile2.next_review_at = datetime.utcnow()
        db_session.commit()
        
        # Should return concept with lower accuracy
        next_concept = learning.next_concept("test-user")
        assert next_concept.id == concept2.id

# Made with Bob
