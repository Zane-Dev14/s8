from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db import Concept, ConceptEdge, LearnerProfile, LearningAttempt


class LearningService:
    def __init__(self, db: Session):
        self.db = db

    def ensure_profiles(self, user_id: str = "local-user") -> None:
        concepts = list(self.db.scalars(select(Concept)).all())
        for concept in concepts:
            existing = self.db.scalar(
                select(LearnerProfile).where(
                    LearnerProfile.user_id == user_id,
                    LearnerProfile.concept_id == concept.id,
                )
            )
            if existing:
                continue
            profile = LearnerProfile(
                user_id=user_id,
                concept_id=concept.id,
                accuracy=0.0,
                response_time_ms=0.0,
                retries=0,
                confidence=50,
                next_review_at=datetime.utcnow(),
            )
            self.db.add(profile)
        self.db.commit()

    def is_mastered(self, user_id: str, concept_id: str) -> bool:
        attempts = list(
            self.db.scalars(
                select(LearningAttempt)
                .where(LearningAttempt.user_id == user_id, LearningAttempt.concept_id == concept_id)
                .order_by(LearningAttempt.created_at.asc())
            ).all()
        )
        qualifying = [
            item
            for item in attempts
            if item.is_correct and item.confidence >= 80 and item.response_time_ms <= 12000
        ]
        if len(qualifying) < 3:
            return False

        checkpoints = qualifying[-3:]
        spaced_minutes = []
        for index in range(1, len(checkpoints)):
            delta = checkpoints[index].created_at - checkpoints[index - 1].created_at
            spaced_minutes.append(delta.total_seconds() / 60.0)
        return all(minutes >= 8.0 for minutes in spaced_minutes)

    def next_concept(self, user_id: str = "local-user") -> Concept | None:
        self.ensure_profiles(user_id)
        now = datetime.utcnow()

        forced_revisit_ids = self._forced_revisit_concept_ids(user_id)
        for concept_id in forced_revisit_ids:
            if self.is_mastered(user_id, concept_id):
                continue
            concept = self.db.get(Concept, concept_id)
            if concept:
                return concept

        due_profiles = list(
            self.db.scalars(
                select(LearnerProfile)
                .where(LearnerProfile.user_id == user_id, LearnerProfile.next_review_at <= now)
                .order_by(LearnerProfile.accuracy.asc(), LearnerProfile.retries.desc())
            ).all()
        )
        if not due_profiles:
            due_profiles = list(
                self.db.scalars(
                    select(LearnerProfile)
                    .where(LearnerProfile.user_id == user_id)
                    .order_by(LearnerProfile.accuracy.asc(), LearnerProfile.retries.desc())
                ).all()
            )
        if not due_profiles:
            return None

        for profile in due_profiles:
            if not self.is_mastered(user_id, profile.concept_id):
                concept = self.db.get(Concept, profile.concept_id)
                if concept:
                    return concept

        selected = due_profiles[0]
        return self.db.get(Concept, selected.concept_id)

    def update_progress(
        self,
        *,
        user_id: str,
        concept_id: str,
        is_correct: bool,
        response_time_ms: float,
        confidence: int,
        misconception_tag: str,
        next_action: str,
    ) -> None:
        profile = self.db.scalar(
            select(LearnerProfile).where(
                LearnerProfile.user_id == user_id,
                LearnerProfile.concept_id == concept_id,
            )
        )
        if not profile:
            return

        previous_accuracy = profile.accuracy
        score = 1.0 if is_correct else 0.0
        profile.accuracy = (previous_accuracy * 0.75) + (score * 0.25)
        profile.response_time_ms = (profile.response_time_ms * 0.7) + (response_time_ms * 0.3)
        profile.confidence = confidence

        under_pressure = response_time_ms <= 12000
        high_confidence = confidence >= 80

        if is_correct and high_confidence and under_pressure:
            interval = timedelta(hours=12)
            profile.retries = max(0, profile.retries - 1)
        elif is_correct:
            interval = timedelta(hours=2)
            profile.retries = max(0, profile.retries - 1)
        else:
            interval = timedelta(minutes=15)
            profile.retries += 1

        if misconception_tag == "false_confidence":
            interval = timedelta(minutes=5)
            profile.retries += 2
        elif next_action == "rebuild":
            interval = timedelta(minutes=7)

        if not is_correct:
            self._schedule_dependency_revisit(user_id, concept_id)

        profile.next_review_at = datetime.utcnow() + interval
        self.db.add(profile)
        self.db.commit()

    def pressure_failures(self, user_id: str, concept_id: str) -> int:
        attempts = list(
            self.db.scalars(
                select(LearningAttempt).where(
                    LearningAttempt.user_id == user_id,
                    LearningAttempt.concept_id == concept_id,
                )
            ).all()
        )
        failures = [item for item in attempts if (not item.is_correct) and item.response_time_ms <= 12000]
        return len(failures)

    def _forced_revisit_concept_ids(self, user_id: str) -> list[str]:
        recent_attempts = list(
            self.db.scalars(
                select(LearningAttempt)
                .where(LearningAttempt.user_id == user_id)
                .order_by(LearningAttempt.created_at.desc())
                .limit(64)
            ).all()
        )
        forced: list[str] = []
        for attempt in recent_attempts:
            if attempt.concept_id in forced:
                continue
            if attempt.is_correct and attempt.confidence <= 40:
                forced.append(attempt.concept_id)
                continue
            if (not attempt.is_correct) and attempt.confidence >= 80:
                forced.append(attempt.concept_id)
                continue
            if (not attempt.is_correct) and attempt.response_time_ms >= 18000:
                forced.append(attempt.concept_id)

        prerequisites: list[str] = []
        for concept_id in forced:
            for prereq_id in self._dependency_prerequisites(concept_id):
                if prereq_id not in prerequisites:
                    prerequisites.append(prereq_id)
        return prerequisites + forced

    def _dependency_prerequisites(self, concept_id: str) -> list[str]:
        edges = list(
            self.db.scalars(
                select(ConceptEdge).where(
                    ConceptEdge.target_concept_id == concept_id,
                    ConceptEdge.edge_type.in_(["depends_on", "part_of"]),
                )
            ).all()
        )
        return [edge.source_concept_id for edge in edges]

    def _schedule_dependency_revisit(self, user_id: str, concept_id: str) -> None:
        prerequisite_ids = self._dependency_prerequisites(concept_id)
        if not prerequisite_ids:
            return
        for prereq_id in prerequisite_ids:
            profile = self.db.scalar(
                select(LearnerProfile).where(
                    LearnerProfile.user_id == user_id,
                    LearnerProfile.concept_id == prereq_id,
                )
            )
            if not profile:
                continue
            profile.next_review_at = datetime.utcnow()
            profile.retries += 1
            self.db.add(profile)
        self.db.commit()
