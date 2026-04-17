"""
Quiz Service - RAG-Grounded Question Generation and Evaluation
Generates questions from source material and evaluates answers with misconception detection
"""
import json
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.db import QuizQuestion, Concept, ContentChunk, LearningAttempt
from app.services.streaming_service import StreamingService
from app.core.settings import settings


class QuizService:
    """
    Manages quiz question generation and answer evaluation.
    All questions are grounded in source material via RAG.
    """

    QUESTION_TYPES = ["multiple_choice", "free_answer", "scenario", "fill_blank"]
    MISCONCEPTION_TAGS = ["false_confidence", "lucky_guess", "fragile", "confused"]

    def __init__(self, db: Session):
        self.db = db
        self.streaming = StreamingService()

    async def generate_questions_for_concept(
        self,
        concept: Concept,
        context_chunks: List[str],
        count: int = 5,
    ) -> List[QuizQuestion]:
        """
        Generate quiz questions for a concept.
        Mix of question types, all grounded in source material.
        
        Args:
            concept: Concept to generate questions for
            context_chunks: RAG context from source material
            count: Number of questions to generate
        
        Returns:
            List of QuizQuestion objects
        """
        questions = []
        
        # Generate different types
        type_distribution = {
            "multiple_choice": 2,
            "free_answer": 1,
            "scenario": 1,
            "fill_blank": 1,
        }
        
        for q_type, num in type_distribution.items():
            if len(questions) >= count:
                break
            
            for _ in range(num):
                question = await self._generate_question(
                    concept=concept,
                    question_type=q_type,
                    context_chunks=context_chunks,
                )
                if question:
                    questions.append(question)
                    if len(questions) >= count:
                        break
        
        # Save to database
        for q in questions:
            self.db.add(q)
        self.db.commit()
        
        return questions

    async def _generate_question(
        self,
        concept: Concept,
        question_type: str,
        context_chunks: List[str],
    ) -> Optional[QuizQuestion]:
        """Generate a single question of specified type"""
        
        context = "\n".join(f"- {chunk[:200]}" for chunk in context_chunks[:4])
        
        prompts = {
            "multiple_choice": f"""Create a multiple-choice question about {concept.name}.

Context from source material:
{context}

Requirements:
- Question must be answerable from the context
- 4 options (A, B, C, D)
- Only one correct answer
- Distractors should be plausible but wrong
- Test understanding, not memorization

Return JSON:
{{
  "question": "Question text?",
  "correct_answer": "A",
  "options": {{
    "A": "Correct option",
    "B": "Distractor 1",
    "C": "Distractor 2",
    "D": "Distractor 3"
  }},
  "difficulty": 1-5
}}""",

            "free_answer": f"""Create a free-answer question about {concept.name}.

Context from source material:
{context}

Requirements:
- Requires explanation in learner's own words
- Tests deep understanding
- Answerable from context
- 2-3 sentence answer expected

Return JSON:
{{
  "question": "Explain...",
  "correct_answer": "Expected answer with key points",
  "difficulty": 1-5
}}""",

            "scenario": f"""Create a scenario-based question about {concept.name}.

Context from source material:
{context}

Requirements:
- Present a realistic situation
- Ask what concept applies and why
- Test application, not recall
- Grounded in source material

Return JSON:
{{
  "question": "Scenario: ... What should you do?",
  "correct_answer": "Apply {concept.name} because...",
  "difficulty": 1-5
}}""",

            "fill_blank": f"""Create a fill-in-the-blank question about {concept.name}.

Context from source material:
{context}

Requirements:
- Remove a key term or phrase
- Must be answerable from context
- Test specific knowledge
- One clear correct answer

Return JSON:
{{
  "question": "The process of ___ is essential for...",
  "correct_answer": "specific term",
  "difficulty": 1-5
}}""",
        }
        
        prompt = prompts.get(question_type, prompts["multiple_choice"])
        
        system_prompt = (
            "You create educational quiz questions grounded in source material. "
            "Questions must be fair, clear, and test real understanding. "
            "Return valid JSON only."
        )
        
        response_stream = self.streaming.stream_chat(
            model=settings.model_eval,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.4,
            max_tokens=400,
        )
        
        response_text = await self.streaming.collect_full_response(response_stream)
        
        try:
            data = json.loads(response_text)
            
            # Extract distractors for multiple choice
            distractors = []
            if question_type == "multiple_choice" and "options" in data:
                options = data["options"]
                correct = data["correct_answer"]
                distractors = [v for k, v in options.items() if k != correct]
            
            return QuizQuestion(
                concept_id=concept.id,
                question_type=question_type,
                question=data.get("question", "")[:1000],
                correct_answer=data.get("correct_answer", "")[:1000],
                distractors_json=json.dumps(distractors),
                difficulty=max(1, min(5, int(data.get("difficulty", 3)))),
                source_chunks=json.dumps([chunk[:200] for chunk in context_chunks[:3]]),
            )
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    async def evaluate_answer(
        self,
        question: QuizQuestion,
        user_answer: str,
        confidence: int,  # 0-100
        response_time_ms: float,
    ) -> Dict:
        """
        Evaluate user's answer with RAG-grounded feedback.
        Detects misconceptions and provides targeted feedback.
        
        Returns:
            Dict with: is_correct, score, feedback, misconception_tag, next_action
        """
        # Get context chunks
        try:
            context_chunks = json.loads(question.source_chunks)
        except json.JSONDecodeError:
            context_chunks = []
        
        context = "\n".join(f"- {chunk}" for chunk in context_chunks)
        
        prompt = f"""Evaluate this answer about the concept.

Question: {question.question}
Correct answer: {question.correct_answer}
User's answer: {user_answer}

Source material context:
{context}

Evaluate:
1. Is the answer correct? (yes/no)
2. Score out of 100
3. What did they get right/wrong?
4. Provide 2-3 sentences of plain-language feedback

Return JSON:
{{
  "is_correct": true/false,
  "score": 0-100,
  "feedback": "Plain language feedback...",
  "key_points_missed": ["point1", "point2"] or []
}}"""

        system_prompt = (
            "You are a strict but encouraging tutor. Evaluate answers fairly. "
            "Provide constructive feedback in plain language. Return valid JSON only."
        )

        response_stream = self.streaming.stream_chat(
            model=settings.model_eval,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.2,
            max_tokens=300,
        )

        response_text = await self.streaming.collect_full_response(response_stream)

        try:
            result = json.loads(response_text)
            is_correct = bool(result.get("is_correct", False))
            score = max(0, min(100, int(result.get("score", 0))))
            feedback = str(result.get("feedback", "")).strip()
        except (json.JSONDecodeError, KeyError, ValueError):
            # Fallback heuristic
            is_correct = self._simple_match(user_answer, question.correct_answer)
            score = 100 if is_correct else 0
            feedback = "Correct!" if is_correct else "Not quite. Review the concept and try again."

        # Detect misconception
        misconception_tag = self._detect_misconception(
            is_correct=is_correct,
            confidence=confidence,
            response_time_ms=response_time_ms,
        )

        # Determine next action
        next_action = self._determine_next_action(
            is_correct=is_correct,
            misconception_tag=misconception_tag,
            score=score,
        )

        return {
            "is_correct": is_correct,
            "score": score,
            "feedback": feedback,
            "misconception_tag": misconception_tag,
            "next_action": next_action,
            "confidence": confidence,
            "response_time_ms": response_time_ms,
        }

    def _detect_misconception(
        self,
        is_correct: bool,
        confidence: int,
        response_time_ms: float,
    ) -> str:
        """
        Detect type of misconception based on performance.
        
        Tags:
        - false_confidence: Wrong but high confidence
        - lucky_guess: Correct but very low confidence
        - fragile: Correct but slow + medium confidence
        - confused: Wrong and slow
        """
        if not is_correct:
            if confidence >= 80:
                return "false_confidence"
            elif response_time_ms >= 18000:
                return "confused"
            else:
                return ""
        else:
            if confidence <= 40:
                return "lucky_guess"
            elif response_time_ms >= 15000 and confidence < 70:
                return "fragile"
            else:
                return ""

    def _determine_next_action(
        self,
        is_correct: bool,
        misconception_tag: str,
        score: int,
    ) -> str:
        """
        Determine what learner should do next.
        
        Actions:
        - continue: Move to next question
        - review: Review concept briefly
        - rebuild: Reteach concept from scratch
        - practice_more: More questions on same concept
        """
        if not is_correct:
            if misconception_tag == "false_confidence":
                return "rebuild"
            elif score < 30:
                return "rebuild"
            else:
                return "review"
        else:
            if misconception_tag in ["lucky_guess", "fragile"]:
                return "practice_more"
            else:
                return "continue"

    @staticmethod
    def _simple_match(user_answer: str, correct_answer: str) -> bool:
        """Simple string matching fallback"""
        user_lower = user_answer.lower().strip()
        correct_lower = correct_answer.lower().strip()
        
        # Exact match
        if user_lower == correct_lower:
            return True
        
        # Substring match (for fill-in-blank)
        if correct_lower in user_lower or user_lower in correct_lower:
            return True
        
        # Word overlap (>70% of correct answer words present)
        correct_words = set(correct_lower.split())
        user_words = set(user_lower.split())
        if correct_words:
            overlap = len(correct_words & user_words) / len(correct_words)
            return overlap >= 0.7
        
        return False

    def get_next_question(
        self,
        user_id: str,
        concept_id: str,
    ) -> Optional[QuizQuestion]:
        """
        Get next question for user on this concept.
        Adapts difficulty based on performance.
        """
        # Get recent attempts
        recent_attempts = list(
            self.db.scalars(
                select(LearningAttempt)
                .where(
                    LearningAttempt.user_id == user_id,
                    LearningAttempt.concept_id == concept_id,
                )
                .order_by(LearningAttempt.created_at.desc())
                .limit(5)
            ).all()
        )
        
        # Calculate average performance
        if recent_attempts:
            avg_correct = sum(1 for a in recent_attempts if a.is_correct) / len(recent_attempts)
            target_difficulty = 3 if avg_correct >= 0.7 else 2 if avg_correct >= 0.4 else 1
        else:
            target_difficulty = 1  # Start easy
        
        # Get question near target difficulty
        question = self.db.scalar(
            select(QuizQuestion)
            .where(QuizQuestion.concept_id == concept_id)
            .where(QuizQuestion.difficulty >= target_difficulty - 1)
            .where(QuizQuestion.difficulty <= target_difficulty + 1)
            .order_by(QuizQuestion.difficulty.asc())
            .limit(1)
        )
        
        return question

# Made with Bob
