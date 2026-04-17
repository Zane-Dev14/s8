from __future__ import annotations

import json
import re
from typing import Literal, cast

from sqlalchemy.orm import Session

from app.models.db import Concept, LearningAttempt
from app.services.chunking_service import ChunkingService
from app.services.learning_service import LearningService
from app.services.ollama_router import OllamaRouter


NextAction = Literal["harder", "retry", "review", "rebuild", "interview"]


class TutorService:
    def __init__(self, db: Session, router: OllamaRouter):
        self.db = db
        self.router = router
        self.learning = LearningService(db)
        self.chunking = ChunkingService(db, router)

    async def start_lesson(
        self,
        user_id: str,
        mode: Literal["lesson", "interview"] = "lesson",
    ) -> tuple[Concept | None, dict[str, str], str, int]:
        concept = self.learning.next_concept(user_id)
        if not concept:
            return None, {}, "No concepts available. Run ingestion first.", 20

        lesson_preview = self._build_lesson_preview(concept)

        if mode == "interview":
            question = concept.hard_follow_up or f"Interview mode: defend {concept.name} under failure pressure."
            return concept, lesson_preview, question, 10

        question = concept.checkpoint_question or f"Explain {concept.name} in one precise operational sentence."
        return concept, lesson_preview, question, 20

    async def start_lesson_for_concept(
        self,
        concept_id: str,
        mode: Literal["lesson", "interview"] = "lesson",
    ) -> tuple[Concept | None, dict[str, str], str, int]:
        concept = self.db.get(Concept, concept_id)
        if not concept:
            return None, {}, "Requested concept is not available.", 20

        lesson_preview = self._build_lesson_preview(concept)

        if mode == "interview":
            question = concept.hard_follow_up or f"Interview mode: defend {concept.name} under failure pressure."
            return concept, lesson_preview, question, 10

        question = concept.checkpoint_question or f"Explain {concept.name} in one precise operational sentence."
        return concept, lesson_preview, question, 20

    def _build_lesson_preview(self, concept: Concept) -> dict[str, str]:
        return {
            "name": concept.name,
            "why_it_matters": self._plain_text(concept.why_it_matters),
            "intuition": self._plain_text(concept.intuition),
            "explanation": self._plain_text(concept.explanation),
            "example": self._plain_text(concept.example),
            "common_mistake": self._plain_text(concept.common_mistake),
            "source_reference": concept.source_reference,
        }

    async def evaluate_answer(
        self,
        *,
        user_id: str,
        concept: Concept,
        question: str,
        user_answer: str,
        user_confidence: int,
        response_time_ms: float,
        mode: Literal["lesson", "interview"],
    ) -> tuple[bool, str, str, NextAction, str, list[str], str, str, int]:
        retrieved = self.chunking.retrieve_relevant_chunks_with_scores(
            f"{concept.name} {question} {user_answer}",
            limit=8,
        )
        strong_retrieval = [item for item in retrieved if item.score >= 0.18]
        source_chunks = [
            f"{item.chunk.source_reference} [{item.chunk.chunk_type}] {item.chunk.text[:220]}"
            for item in strong_retrieval
        ]

        if not strong_retrieval:
            correctness = False
            explanation = (
                "Uncertain. I do not have strong grounded source chunks for this answer yet. "
                "Re-run ingestion/chunking or answer using direct source terms."
            )
            misconception_tag = "insufficient_grounding"
            next_action: NextAction = "review"
            confidence_label = "low"
            uncertainty = "high: source evidence too weak"
        else:
            correctness, explanation, misconception_tag, next_action, confidence_label, uncertainty = await self._model_eval(
                concept=concept,
                question=question,
                user_answer=user_answer,
                source_chunks=source_chunks,
            )
            if misconception_tag == "":
                misconception_tag = "none"

        derived_tag = self._derive_misconception(correctness, user_confidence, response_time_ms)
        if derived_tag != "none":
            misconception_tag = derived_tag
            if derived_tag in {"false_confidence", "hesitation_confusion"}:
                next_action = "rebuild"
            elif derived_tag in {"lucky_guess", "fragile_understanding"}:
                next_action = "review"

        if next_action == "harder" and mode == "interview":
            next_action = "interview"

        self.learning.update_progress(
            user_id=user_id,
            concept_id=concept.id,
            is_correct=correctness,
            response_time_ms=response_time_ms,
            confidence=user_confidence,
            misconception_tag=misconception_tag,
            next_action=next_action,
        )

        attempt = LearningAttempt(
            user_id=user_id,
            concept_id=concept.id,
            answer=user_answer,
            is_correct=correctness,
            feedback=explanation,
            response_time_ms=response_time_ms,
            confidence=user_confidence,
        )
        self.db.add(attempt)
        self.db.commit()

        if next_action in {"harder", "interview"}:
            next_question = concept.hard_follow_up or f"Now stress-test {concept.name}: what fails first and why?"
        elif next_action == "rebuild":
            next_question = (
                f"You thought you knew {concept.name}. You don't yet. "
                "Rebuild from first principles: define it, show a concrete example, then explain failure impact."
            )
        else:
            next_question = concept.checkpoint_question or f"Retry: what is the key idea behind {concept.name}?"

        feedback_delay_ms = 1800 if next_action in {"retry", "review", "rebuild"} else 900
        return (
            correctness,
            explanation,
            misconception_tag,
            next_action,
            next_question,
            source_chunks,
            confidence_label,
            uncertainty,
            feedback_delay_ms,
        )

    async def _model_eval(
        self,
        *,
        concept: Concept,
        question: str,
        user_answer: str,
        source_chunks: list[str],
    ) -> tuple[bool, str, str, NextAction, str, str]:
        system = (
            "You are a strict evaluator. You MUST use only provided source chunks. "
            "If source chunks are weak or insufficient, set correctness=false and uncertainty high. "
            "Return JSON: correctness(boolean), explanation(string), misconception_tag(string), "
            "next_action(one of harder|retry|review|rebuild|interview), confidence(string), uncertainty(string)."
        )
        user = (
            f"Concept: {concept.name}\n"
            f"Question: {question}\n"
            f"Learner answer: {user_answer}\n"
            f"Common mistake: {concept.common_mistake}\n"
            "Grounding source chunks:\n"
            + "\n".join(f"- {chunk}" for chunk in source_chunks)
        )
        try:
            raw = await self.router.chat("teacher", system, user, temperature=0.1)
        except Exception:
            return self._heuristic_eval(concept, user_answer, source_chunks)

        parsed = self._parse_json(raw)
        if not parsed:
            return self._heuristic_eval(concept, user_answer, source_chunks)

        correctness = parsed.get("correctness")
        explanation = str(parsed.get("explanation", "")).strip()
        misconception_tag = str(parsed.get("misconception_tag", "none")).strip() or "none"
        next_action_value = str(parsed.get("next_action", "review")).strip().lower()
        confidence_label = str(parsed.get("confidence", "medium")).strip() or "medium"
        uncertainty = str(parsed.get("uncertainty", "medium")).strip() or "medium"

        if not isinstance(correctness, bool):
            return self._heuristic_eval(concept, user_answer, source_chunks)

        if next_action_value not in {"harder", "retry", "review", "rebuild", "interview"}:
            next_action_value = "review"
        next_action = cast(NextAction, next_action_value)

        return (
            correctness,
            explanation or "Evaluation completed against grounded source chunks.",
            misconception_tag,
            next_action,
            confidence_label,
            uncertainty,
        )

    @staticmethod
    def _heuristic_eval(
        concept: Concept,
        user_answer: str,
        source_chunks: list[str],
    ) -> tuple[bool, str, str, NextAction, str, str]:
        answer_tokens = set(re.findall(r"[a-zA-Z0-9_]+", user_answer.lower()))
        source_tokens = set(re.findall(r"[a-zA-Z0-9_]+", " ".join(source_chunks).lower()))
        overlap = len(answer_tokens & source_tokens)
        ratio = overlap / max(len(source_tokens), 1)

        if ratio >= 0.12 and len(user_answer.split()) >= 12:
            return (
                True,
                "Grounded answer detected from retrieved source evidence.",
                "none",
                "harder",
                "medium",
                "low",
            )
        feedback = (
            "Uncertain or weakly grounded answer. Rebuild it from source evidence only. "
            f"Anchor intuition: {concept.intuition or concept.explanation[:180]}"
        )
        return False, feedback, "insufficient_grounding", "review", "low", "high"

    @staticmethod
    def _derive_misconception(correctness: bool, user_confidence: int, response_time_ms: float) -> str:
        if (not correctness) and user_confidence >= 80:
            return "false_confidence"
        if correctness and user_confidence <= 40:
            return "lucky_guess"
        if correctness and (user_confidence < 65 or response_time_ms > 14000):
            return "fragile_understanding"
        if (not correctness) and response_time_ms > 20000:
            return "hesitation_confusion"
        if (not correctness) and user_confidence < 35:
            return "guessing_pattern"
        return "none"

    @staticmethod
    def _parse_json(raw: str) -> dict[str, object]:
        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
        return {}

    @staticmethod
    def _plain_text(text: str) -> str:
        if not text:
            return ""
        simplified = text
        replacements = {
            "protocol": "method",
            "authentication": "identity check",
            "encrypted": "locked",
            "encryption": "locking",
            "compliance": "required policy",
            "man-in-the-middle": "someone intercepting the connection",
            "transmitted": "sent",
        }
        for original, replacement in replacements.items():
            simplified = re.sub(rf"\b{re.escape(original)}\b", replacement, simplified, flags=re.IGNORECASE)

        sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", simplified) if part.strip()]
        compact = " ".join(sentences[:3])
        return compact
