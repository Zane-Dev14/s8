"""
Teaching Session Service - 8-Section Goku-Style Teaching Flow
Implements the complete teaching experience with streaming support
"""
from typing import Dict, List, AsyncGenerator
from sqlalchemy.orm import Session
from sqlalchemy import select
import json

from app.models.db import Concept, ContentChunk
from app.services.streaming_service import StreamingService
from app.services.goku_tts_service import GokuTTSService
from app.core.settings import settings


class TeachingSessionService:
    """
    Manages complete teaching sessions with 8-section flow:
    1. HOOK - Why should you care?
    2. ANALOGY - Real-world comparison
    3. CORE - What it actually is
    4. VISUAL - Diagram description
    5. EXAMPLE - Concrete walkthrough
    6. MISTAKE - Common misunderstanding
    7. PRACTICE - Quick scenario
    8. QUIZ UNLOCK - Ready for questions
    """

    SECTION_ORDER = [
        "hook",
        "analogy",
        "core",
        "visual",
        "example",
        "mistake",
        "practice",
        "encouragement",
    ]

    def __init__(self, db: Session):
        self.db = db
        self.streaming = StreamingService()
        self.tts = GokuTTSService()

    async def stream_teaching_session(
        self,
        concept: Concept,
        user_level: str = "beginner",
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream complete teaching session section by section.
        
        Yields:
            Dict with: {
                "section": section_name,
                "content": text,
                "audio_url": optional_audio_path,
                "progress": current/total,
                "done": boolean
            }
        """
        # Get RAG context
        context_chunks = await self._get_context_chunks(concept)
        
        total_sections = len(self.SECTION_ORDER)
        
        for idx, section_name in enumerate(self.SECTION_ORDER, 1):
            # Stream section content
            section_text = ""
            
            async for token_data in self.streaming.stream_teaching_section(
                concept_name=concept.name,
                section_name=section_name,
                context_chunks=context_chunks,
                section_type=section_name,
            ):
                try:
                    data = json.loads(token_data)
                    if data.get("done"):
                        break
                    if "token" in data:
                        section_text += data["token"]
                        # Yield token for real-time display
                        yield {
                            "type": "token",
                            "section": section_name,
                            "token": data["token"],
                            "progress": f"{idx}/{total_sections}",
                        }
                except json.JSONDecodeError:
                    continue
            
            # Section complete - generate audio in background
            audio_url = ""
            try:
                audio_path = await self.tts.speak(
                    self.tts.add_pacing_pauses(section_text),
                    speed=1.15,
                    cache=True,
                )
                audio_url = self.tts.get_audio_url(audio_path)
            except Exception:
                pass  # Audio is optional
            
            # Yield complete section
            yield {
                "type": "section_complete",
                "section": section_name,
                "content": section_text,
                "audio_url": audio_url,
                "progress": f"{idx}/{total_sections}",
                "done": False,
            }
            
            # Pre-generate audio for next section if not last
            if idx < total_sections:
                next_section = self.SECTION_ORDER[idx]
                # Fire and forget
                try:
                    next_prompt = self.streaming._build_section_prompt(
                        concept.name,
                        next_section,
                        context_chunks,
                        next_section,
                    )
                    # This will cache for next section
                    asyncio.create_task(
                        self.tts.pre_generate_next_section(next_prompt, speed=1.15)
                    )
                except Exception:
                    pass
        
        # Session complete
        yield {
            "type": "session_complete",
            "section": "complete",
            "content": "",
            "audio_url": "",
            "progress": f"{total_sections}/{total_sections}",
            "done": True,
        }

    async def generate_full_session(
        self,
        concept: Concept,
        user_level: str = "beginner",
    ) -> Dict:
        """
        Generate complete teaching session (non-streaming).
        Use only when streaming is not possible.
        
        Returns:
            Dict with all sections and metadata
        """
        context_chunks = await self._get_context_chunks(concept)
        
        sections = {}
        audio_paths = {}
        
        for section_name in self.SECTION_ORDER:
            # Generate section content
            section_stream = self.streaming.stream_teaching_section(
                concept_name=concept.name,
                section_name=section_name,
                context_chunks=context_chunks,
                section_type=section_name,
            )
            
            section_text = await self.streaming.collect_full_response(section_stream)
            sections[section_name] = section_text
            
            # Generate audio
            try:
                audio_path = await self.tts.speak(
                    self.tts.add_pacing_pauses(section_text),
                    speed=1.15,
                    cache=True,
                )
                audio_paths[section_name] = self.tts.get_audio_url(audio_path)
            except Exception:
                audio_paths[section_name] = ""
        
        return {
            "concept_name": concept.name,
            "plain_name": concept.plain_name or concept.name,
            "difficulty": concept.difficulty,
            "sections": sections,
            "audio_paths": audio_paths,
            "section_order": self.SECTION_ORDER,
            "user_level": user_level,
        }

    async def assess_comprehension(
        self,
        concept: Concept,
        learner_summary: str,
        learner_example: str,
        learner_mistake: str,
    ) -> Dict:
        """
        Assess if learner truly understands the concept.
        Gates access to quiz questions.
        
        Returns:
            Dict with: understood (bool), score (0-100), feedback (str), next_step (str)
        """
        context_chunks = await self._get_context_chunks(concept)
        context = "\n".join(f"- {chunk[:200]}" for chunk in context_chunks[:3])
        
        prompt = f"""Evaluate if this learner genuinely understands {concept.name}.

Learner's summary: {learner_summary}
Learner's example: {learner_example}
Learner's mistake description: {learner_mistake}

Source material context:
{context}

Evaluate:
1. Do they understand the core concept? (not just memorized)
2. Can they apply it to a real situation?
3. Do they know what can go wrong?

Return JSON:
{{
  "understood": true/false,
  "score": 0-100,
  "feedback": "2-3 sentences in plain language",
  "next_step": "ready_for_quiz" or "needs_reteach"
}}"""

        system_prompt = (
            "You are a strict but kind tutor. Evaluate real understanding vs surface recall. "
            "Use plain-language coaching."
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
            return {
                "understood": bool(result.get("understood", False)),
                "score": max(0, min(100, int(result.get("score", 0)))),
                "feedback": str(result.get("feedback", "Let's review this concept again.")).strip(),
                "next_step": str(result.get("next_step", "needs_reteach")),
            }
        except (json.JSONDecodeError, KeyError, ValueError):
            # Fallback heuristic
            return self._heuristic_comprehension(
                learner_summary,
                learner_example,
                learner_mistake,
            )

    def _heuristic_comprehension(
        self,
        summary: str,
        example: str,
        mistake: str,
    ) -> Dict:
        """Fallback comprehension check using simple heuristics"""
        lengths = [len(summary.split()), len(example.split()), len(mistake.split())]
        
        # Score based on completeness
        score = min(100, int(sum(min(part, 20) for part in lengths) * (100 / 60)))
        understood = score >= 65
        
        if understood:
            feedback = "Good work! You explained the idea, gave an example, and described what can go wrong."
            next_step = "ready_for_quiz"
        else:
            feedback = "You're close, but let's clarify. Use simpler words, give one concrete situation, and describe one specific failure."
            next_step = "needs_reteach"
        
        return {
            "understood": understood,
            "score": score,
            "feedback": feedback,
            "next_step": next_step,
        }

    async def _get_context_chunks(self, concept: Concept, limit: int = 8) -> List[str]:
        """Get relevant content chunks for concept (RAG)"""
        # Get chunks from source files
        # TODO: Use ChromaDB for semantic search
        # For now, get chunks from concept's source reference
        
        chunks = list(
            self.db.scalars(
                select(ContentChunk)
                .where(ContentChunk.source_reference.contains(concept.name))
                .limit(limit)
            ).all()
        )
        
        if not chunks:
            # Fallback: use concept's own content
            return [
                concept.explanation or "",
                concept.example or "",
                concept.why_it_matters or "",
            ]
        
        return [chunk.text for chunk in chunks if chunk.text]

    def get_section_metadata(self, section_name: str) -> Dict:
        """Get metadata about a teaching section"""
        metadata = {
            "hook": {
                "title": "Why This Matters",
                "icon": "🎯",
                "duration_estimate": "30 seconds",
                "purpose": "Grab attention and show relevance",
            },
            "analogy": {
                "title": "Real-World Comparison",
                "icon": "🌍",
                "duration_estimate": "45 seconds",
                "purpose": "Make it relatable and memorable",
            },
            "core": {
                "title": "The Core Concept",
                "icon": "💡",
                "duration_estimate": "60 seconds",
                "purpose": "Explain what it actually is",
            },
            "visual": {
                "title": "Picture This",
                "icon": "🎨",
                "duration_estimate": "45 seconds",
                "purpose": "Create a mental model",
            },
            "example": {
                "title": "Concrete Example",
                "icon": "📝",
                "duration_estimate": "60 seconds",
                "purpose": "Show it in action",
            },
            "mistake": {
                "title": "Common Pitfall",
                "icon": "⚠️",
                "duration_estimate": "30 seconds",
                "purpose": "Avoid typical errors",
            },
            "practice": {
                "title": "Think About This",
                "icon": "🤔",
                "duration_estimate": "30 seconds",
                "purpose": "Apply your understanding",
            },
            "encouragement": {
                "title": "You Got This!",
                "icon": "💪",
                "duration_estimate": "15 seconds",
                "purpose": "Build confidence",
            },
        }
        
        return metadata.get(section_name, {
            "title": section_name.replace("_", " ").title(),
            "icon": "📚",
            "duration_estimate": "30 seconds",
            "purpose": "Learn this concept",
        })


# Import asyncio for task creation
import asyncio

# Made with Bob
