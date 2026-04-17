"""
Flashcard Service with SM-2 Spaced Repetition Algorithm
Generates and schedules flashcards for optimal retention
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.db import Flashcard, Concept, LearnerProfile
from app.services.streaming_service import StreamingService
from app.core.settings import settings
import json


class FlashcardService:
    """
    Manages flashcard generation and SM-2 spaced repetition scheduling.
    """

    CARD_TYPES = ["definition", "analogy", "application", "mistake"]

    def __init__(self, db: Session):
        self.db = db
        self.streaming = StreamingService()

    async def generate_flashcards_for_concept(
        self,
        concept: Concept,
        context_chunks: List[str],
        min_cards: int = 5,
    ) -> List[Flashcard]:
        """
        Generate flashcards for a concept (mix of all 4 types).
        
        Args:
            concept: Concept to generate cards for
            context_chunks: RAG context from source material
            min_cards: Minimum number of cards to generate
        
        Returns:
            List of generated Flashcard objects
        """
        # Build context
        context = "\n".join(f"- {chunk[:200]}" for chunk in context_chunks[:4])
        
        # Generate cards for each type
        cards = []
        
        for card_type in self.CARD_TYPES:
            card = await self._generate_card(
                concept=concept,
                card_type=card_type,
                context=context,
            )
            if card:
                cards.append(card)
        
        # Generate additional cards if needed
        while len(cards) < min_cards:
            # Generate extra application or definition cards
            extra_type = "application" if len(cards) % 2 == 0 else "definition"
            card = await self._generate_card(
                concept=concept,
                card_type=extra_type,
                context=context,
            )
            if card:
                cards.append(card)
            else:
                break  # Can't generate more
        
        # Save to database
        for card in cards:
            self.db.add(card)
        self.db.commit()
        
        return cards

    async def _generate_card(
        self,
        concept: Concept,
        card_type: str,
        context: str,
    ) -> Optional[Flashcard]:
        """Generate a single flashcard of specified type"""
        
        prompts = {
            "definition": f"""Create a definition flashcard for {concept.name}.

Context: {context}

Front: Ask for the plain-language definition
Back: Provide clear, jargon-free definition (2-3 sentences)
Cue: Hint for answering

Return JSON:
{{"front": "What is...", "back": "Definition...", "cue": "Hint..."}}""",

            "analogy": f"""Create an analogy flashcard for {concept.name}.

Context: {context}

Front: "What's {concept.name} like in real life?"
Back: Simple real-world analogy (2-3 sentences)
Cue: Hint about the analogy domain

Return JSON:
{{"front": "Question...", "back": "Analogy...", "cue": "Hint..."}}""",

            "application": f"""Create an application flashcard for {concept.name}.

Context: {context}

Front: Present a scenario where {concept.name} applies
Back: Explain which concept applies and why (2-3 sentences)
Cue: Hint about the scenario

Return JSON:
{{"front": "Scenario...", "back": "Application...", "cue": "Hint..."}}""",

            "mistake": f"""Create a mistake flashcard for {concept.name}.

Context: {context}

Front: Present a wrong statement about {concept.name}
Back: Explain what's wrong and the correct version (2-3 sentences)
Cue: Hint about the error

Return JSON:
{{"front": "Wrong statement...", "back": "Correction...", "cue": "Hint..."}}""",
        }
        
        prompt = prompts.get(card_type, prompts["definition"])
        
        system_prompt = (
            "You create educational flashcards grounded in source material. "
            "Keep language simple and practical. Return valid JSON only."
        )
        
        response_stream = self.streaming.stream_chat(
            model=settings.model_fast,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.4,
            max_tokens=200,
        )
        
        response_text = await self.streaming.collect_full_response(response_stream)
        
        try:
            card_data = json.loads(response_text)
            
            return Flashcard(
                concept_id=concept.id,
                card_type=card_type,
                front=card_data.get("front", "")[:500],
                back=card_data.get("back", "")[:1000],
                cue=card_data.get("cue", "")[:256],
                ease_factor=2.5,  # SM-2 default
                interval_days=1,
                repetitions=0,
            )
        except (json.JSONDecodeError, KeyError):
            return None

    def update_card_schedule(
        self,
        card: Flashcard,
        quality: int,  # 0-5 (SM-2 quality rating)
    ) -> Flashcard:
        """
        Update flashcard schedule using SM-2 algorithm.
        
        Args:
            card: Flashcard to update
            quality: User's recall quality (0=complete blackout, 5=perfect recall)
        
        Returns:
            Updated flashcard
        """
        # SM-2 Algorithm
        if quality < 3:
            # Failed recall - reset
            card.repetitions = 0
            card.interval_days = 1
            card.ease_factor = max(1.3, card.ease_factor - 0.2)
        else:
            # Successful recall
            if card.repetitions == 0:
                card.interval_days = 1
            elif card.repetitions == 1:
                card.interval_days = 6
            else:
                card.interval_days = round(card.interval_days * card.ease_factor)
            
            card.repetitions += 1
            
            # Adjust ease factor
            card.ease_factor = max(
                1.3,
                card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            )
        
        self.db.add(card)
        self.db.commit()
        
        return card

    def get_due_cards(
        self,
        user_id: str,
        subject_id: str,
        limit: int = 20,
    ) -> List[Flashcard]:
        """
        Get flashcards due for review.
        
        Args:
            user_id: User identifier
            subject_id: Subject to get cards from
            limit: Maximum cards to return
        
        Returns:
            List of due flashcards
        """
        # Get concepts for this subject
        concepts = list(
            self.db.scalars(
                select(Concept).where(Concept.subject_id == subject_id)
            ).all()
        )
        
        concept_ids = [c.id for c in concepts]
        
        # Get due cards
        # TODO: Track per-user card reviews in separate table
        # For now, return cards that haven't been reviewed recently
        
        cards = list(
            self.db.scalars(
                select(Flashcard)
                .where(Flashcard.concept_id.in_(concept_ids))
                .order_by(Flashcard.interval_days.asc())
                .limit(limit)
            ).all()
        )
        
        return cards

    def convert_confidence_to_quality(
        self,
        correct: bool,
        confidence: int,  # 0-100
        response_time_ms: float,
    ) -> int:
        """
        Convert user performance to SM-2 quality rating (0-5).
        
        Args:
            correct: Whether answer was correct
            confidence: User's confidence (0-100)
            response_time_ms: Response time in milliseconds
        
        Returns:
            SM-2 quality rating (0-5)
        """
        if not correct:
            # Failed recall
            if confidence >= 80:
                return 1  # False confidence
            else:
                return 0  # Complete blackout
        
        # Correct recall - rate based on confidence and speed
        if confidence >= 80 and response_time_ms <= 10000:
            return 5  # Perfect recall
        elif confidence >= 70 and response_time_ms <= 15000:
            return 4  # Correct with hesitation
        elif confidence >= 60:
            return 3  # Correct with difficulty
        else:
            return 2  # Lucky guess
    
    def get_card_statistics(
        self,
        user_id: str,
        subject_id: str,
    ) -> Dict:
        """
        Get flashcard statistics for a user and subject.
        
        Returns:
            Dict with: total_cards, due_today, mastered, average_ease
        """
        # Get concepts for subject
        concepts = list(
            self.db.scalars(
                select(Concept).where(Concept.subject_id == subject_id)
            ).all()
        )
        
        concept_ids = [c.id for c in concepts]
        
        # Get all cards
        cards = list(
            self.db.scalars(
                select(Flashcard).where(Flashcard.concept_id.in_(concept_ids))
            ).all()
        )
        
        if not cards:
            return {
                "total_cards": 0,
                "due_today": 0,
                "mastered": 0,
                "average_ease": 2.5,
            }
        
        # Calculate statistics
        mastered = sum(1 for c in cards if c.repetitions >= 3 and c.ease_factor >= 2.5)
        average_ease = sum(c.ease_factor for c in cards) / len(cards)
        
        # Due today (simplified - would need review tracking)
        due_today = sum(1 for c in cards if c.interval_days <= 1)
        
        return {
            "total_cards": len(cards),
            "due_today": due_today,
            "mastered": mastered,
            "average_ease": round(average_ease, 2),
        }

# Made with Bob
