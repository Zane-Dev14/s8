"""
Interactive Teaching Service - Real-time conversational teaching with Ollama
Generates engaging, non-technical explanations like a real teacher would explain
"""
import asyncio
import json
import re
from typing import Dict, List, Optional
from app.services.ollama_router import OllamaRouter


class InteractiveTeacherService:
    """
    Generates real-time, conversational teaching content using Ollama.
    Speaks like Goku - energetic, encouraging, uses simple analogies.
    """

    SECTION_ORDER = [
        "hook",
        "analogy",
        "core_concept",
        "visual_description",
        "real_example",
        "why_it_matters",
        "practice_scenario",
        "common_mistake",
        "encouragement",
    ]
    DEFAULT_VISUAL_DESCRIPTION = (
        "Visualize: sender on the left, receiver on the right, and a locked tunnel between them."
    )
    DEFAULT_REAL_EXAMPLE = (
        "In your bootcamp flow, this is how partner files move safely between systems."
    )
    
    def __init__(self):
        self.ollama = OllamaRouter()
    
    async def generate_teaching_session(
        self,
        concept_name: str,
        concept_explanation: str,
        source_chunks: List[str],
        learner_level: str = "beginner"
    ) -> Dict:
        """
        Generate a complete interactive teaching session with:
        - Conversational introduction (Goku-style)
        - Simple analogy
        - Step-by-step breakdown
        - Visual description (for diagrams)
        - Practice scenario
        - Encouragement
        """
        
        # Build compact, grounded context from the best available chunks.
        context_lines = [self._trim_for_prompt(item, 260) for item in source_chunks[:6] if item.strip()]
        context = "\n".join(f"- {item}" for item in context_lines)
        
        # Generate conversational teaching content
        teaching_prompt = f"""You are a high-energy mentor teaching {concept_name} to a beginner. Be energetic, encouraging, and use simple analogies.

CONCEPT: {concept_name}
TECHNICAL DETAILS: {concept_explanation}
SOURCE MATERIAL:
{context}

    Audience rules:
    - Keep language at middle-school level.
    - Avoid heavy jargon.
    - If you must use a technical word, explain it immediately in plain words.
    - Keep each sentence short and concrete.

Generate a teaching session with these sections:

1. HOOK (1-2 sentences): Start with an exciting hook that makes them curious. Use "Hey!" or "Alright!" like Goku would.

2. SIMPLE ANALOGY (2-3 sentences): Explain using a real-world analogy anyone can understand. No technical jargon.

3. CORE CONCEPT (3-4 sentences): Explain the main idea in simple terms. Break it down step-by-step.

4. VISUAL DESCRIPTION (2-3 sentences): Describe a concrete picture with parts, flow direction, and failure point.

5. REAL EXAMPLE (2-3 sentences): Use one specific partner/file workflow detail grounded in SOURCE MATERIAL.

6. WHY IT MATTERS (2 sentences): Explain why this is important and powerful.

7. PRACTICE SCENARIO (1-2 sentences): Give them a simple scenario to think about.

8. COMMON MISTAKE (1-2 sentences): Name one realistic mistake and how to avoid it.

9. ENCOURAGEMENT (1 sentence): End with energetic encouragement.

Keep it conversational, energetic, and simple. Avoid technical terms unless you explain them immediately.
Use grounded details from SOURCE MATERIAL for core_concept/visual_description/real_example/why_it_matters/practice_scenario/common_mistake.
Return strict JSON only with keys: hook, analogy, core_concept, visual_description, real_example, why_it_matters, practice_scenario, common_mistake, encouragement"""

        try:
            response = await self.ollama.chat(
                task="teacher",
                system_prompt=(
                    "You are an energetic and encouraging teacher who explains complex topics "
                    "with simple analogies and plain language. Keep explanations practical, accurate, and clear. "
                    "Never skip required keys and always return valid JSON."
                ),
                user_prompt=teaching_prompt,
                temperature=0.45,
                timeout=16.0,
            )
            
            # Parse JSON response
            teaching_content = self._normalize_sections(
                concept_name=concept_name,
                concept_explanation=concept_explanation,
                source_chunks=source_chunks,
                sections=self._safe_parse_json(response),
            )
            if not teaching_content:
                raise ValueError("Teaching content was not valid JSON")

            flashcards = self._generate_flashcards(teaching_content)
            
            return {
                "concept_name": concept_name,
                "teaching_style": "goku_conversational",
                "learner_level": learner_level,
                "sections": teaching_content,
                "flashcards": flashcards,
                "has_audio": False,  # Will be generated separately
                "diagrams": self._find_relevant_diagrams(concept_name),
                "interactive_elements": self._generate_interactive_elements(concept_name)
            }
            
        except json.JSONDecodeError:
            # Fallback to structured parsing if JSON fails
            return self._fallback_teaching_content(concept_name, concept_explanation, response)
        except Exception as e:
            print(f"Error generating teaching session: {e}")
            return self._fallback_teaching_content(concept_name, concept_explanation, "")
    
    def _find_relevant_diagrams(self, concept_name: str) -> List[Dict]:
        """
        Find relevant diagrams from bootcamp materials based on concept
        """
        diagrams = []
        
        # Map concepts to available diagrams
        diagram_mapping = {
            "SFTP": [
                {
                    "path": "/bootcamp/SFTP Files/SFTP.jpg",
                    "title": "SFTP Architecture",
                    "description": "How SFTP securely transfers files"
                },
                {
                    "path": "/bootcamp/SFTP Files/SSH_simplified_protocol_diagram.png",
                    "title": "SSH Protocol Flow",
                    "description": "Step-by-step SSH connection process"
                }
            ],
            "Business Process": [
                {
                    "path": "/bootcamp/RealTime_Scenario_CaseStudy_Flow.png",
                    "title": "Real-Time Scenario Flow",
                    "description": "Complete business process workflow"
                }
            ],
            "Architecture": [
                {
                    "path": "/bootcamp/Sample_Architecture.png",
                    "title": "B2Bi Architecture",
                    "description": "System architecture overview"
                }
            ],
            "Mailbox": [
                {
                    "path": "/bootcamp/RealTime_Scenario_CaseStudy_Flow.png",
                    "title": "Mailbox Extraction Flow",
                    "description": "How mailbox extraction works"
                }
            ]
        }
        
        # Find matching diagrams
        for key, diagram_list in diagram_mapping.items():
            if key.lower() in concept_name.lower():
                diagrams.extend(diagram_list)
        
        return diagrams
    
    def _generate_interactive_elements(self, concept_name: str) -> List[Dict]:
        """
        Generate interactive elements for the teaching session
        """
        return [
            {
                "type": "highlight_animation",
                "trigger": "on_section_view",
                "description": "Highlight key terms as they're explained"
            },
            {
                "type": "progress_indicator",
                "trigger": "continuous",
                "description": "Show learning progress through sections"
            },
            {
                "type": "pause_for_thought",
                "trigger": "after_analogy",
                "duration_seconds": 3,
                "message": "Take a moment to think about this analogy..."
            },
            {
                "type": "visual_reveal",
                "trigger": "on_visual_description",
                "description": "Reveal diagram with animated explanation"
            }
        ]

    async def generate_mermaid_diagram(self, concept_name: str, sections: Dict[str, str]) -> Optional[Dict]:
        section_points = "\n".join(
            f"- {key.replace('_', ' ').title()}: {str(value)[:180]}"
            for key, value in list(sections.items())[:6]
        )
        prompt = f"""Create one Mermaid flowchart for teaching this concept.

Concept: {concept_name}
Teaching points:
{section_points}

Rules:
- Output only Mermaid code, no markdown fences.
- Start with: flowchart TD
- Use 6-10 nodes.
- Keep node labels short and beginner-friendly.
- Show a clear learning progression from idea -> process -> outcome.
"""

        try:
            raw = await self.ollama.chat(
                task="fast_ui",
                system_prompt="You generate clean Mermaid diagrams for educational explanations.",
                user_prompt=prompt,
                temperature=0.2,
                timeout=1.0,
            )
            code = raw.strip()
            code = re.sub(r"^```(?:mermaid)?", "", code, flags=re.IGNORECASE).strip()
            code = re.sub(r"```$", "", code).strip()
            if "flowchart" not in code.lower():
                return self._fallback_mermaid_diagram(concept_name, sections)

            return {
                "title": f"{concept_name} - Concept Flow",
                "description": "Auto-generated concept map from the teaching narrative.",
                "image_url": "",
                "source_path": "ollama:mermaid",
                "mermaid_code": code,
            }
        except Exception:
            return self._fallback_mermaid_diagram(concept_name, sections)

    @staticmethod
    def _fallback_mermaid_diagram(concept_name: str, sections: Dict[str, str]) -> Dict:
        section_names = [key.replace("_", " ").title() for key in list(sections.keys())[:6]]
        if not section_names:
            section_names = ["Understand", "Apply", "Validate"]

        nodes = [
            "A[Source Signal]",
            "B[Validate Inputs]",
            "C[Apply {0}]".format(re.sub(r"[^a-zA-Z0-9 /-]", "", concept_name)[:28] or "Concept"),
            "D[Secure Transfer Path]",
            "E[Partner Outcome]",
            "F[Failure Checkpoint]",
            "G[Recovery Action]",
        ]
        edges = [
            "A --> B",
            "B --> C",
            "C --> D",
            "D --> E",
            "D --> F",
            "F --> G",
            "G --> D",
        ]

        for idx, name in enumerate(section_names[:3], start=1):
            node_id = chr(ord("G") + idx)
            safe_name = re.sub(r"[^a-zA-Z0-9 /-]", "", name)[:30] or f"Step {idx}"
            nodes.append(f"{node_id}[{safe_name}]")
            edges.append(f"C --> {node_id}")

        code = "flowchart TD\n  " + "\n  ".join(nodes + edges)
        return {
            "title": f"{concept_name} - Concept Flow",
            "description": "Generated concept map (fallback).",
            "image_url": "",
            "source_path": "fallback:mermaid",
            "mermaid_code": code,
        }
    
    def _fallback_teaching_content(
        self,
        concept_name: str,
        concept_explanation: str,
        raw_response: str
    ) -> Dict:
        """
        Fallback teaching content if Ollama generation fails
        """
        return {
            "concept_name": concept_name,
            "teaching_style": "goku_conversational",
            "learner_level": "beginner",
            "sections": self._normalize_sections(
                concept_name=concept_name,
                concept_explanation=concept_explanation,
                source_chunks=[],
                sections={
                    "hook": f"Alright, quick win: {concept_name} is easier than it sounds.",
                    "analogy": f"Picture a locked delivery lane. {concept_name} is that lane for your files.",
                    "core_concept": self._plain_summary(concept_explanation, concept_name),
                    "visual_description": self.DEFAULT_VISUAL_DESCRIPTION,
                    "real_example": self.DEFAULT_REAL_EXAMPLE,
                    "why_it_matters": "If this step fails, files do not arrive safely. If it works, business keeps moving.",
                    "practice_scenario": "You need to send a partner file today. Which secure path do you choose and why?",
                    "common_mistake": "A common mistake is mixing up secure and non-secure transfer paths.",
                    "encouragement": "Nice progress. One step at a time and you will own this.",
                },
            ),
            "flashcards": self._generate_flashcards(
                self._normalize_sections(
                    concept_name=concept_name,
                    concept_explanation=concept_explanation,
                    source_chunks=[],
                    sections={
                        "hook": f"Hey! Let's learn about {concept_name} together!",
                        "analogy": f"Think of {concept_name} like a delivery system - it gets things from point A to point B safely.",
                        "core_concept": concept_explanation,
                        "visual_description": self.DEFAULT_VISUAL_DESCRIPTION,
                        "real_example": self.DEFAULT_REAL_EXAMPLE,
                        "why_it_matters": "This is crucial for secure business operations!",
                        "practice_scenario": "Name one step you would take first in a real partner file handoff.",
                        "common_mistake": "People skip validation and only discover failures after delivery windows close.",
                        "encouragement": "You got this.",
                    },
                )
            ),
            "has_audio": False,
            "diagrams": self._find_relevant_diagrams(concept_name),
            "interactive_elements": self._generate_interactive_elements(concept_name)
        }

    @staticmethod
    def _plain_summary(text: str, concept_name: str) -> str:
        if not text:
            return f"{concept_name} is a safe way to move files between systems."
        cleaned = text
        replacements = {
            "protocol": "method",
            "authentication": "identity check",
            "encrypted": "locked",
            "encryption": "locking",
            "transmitted": "sent",
            "channel": "path",
        }
        for original, replacement in replacements.items():
            cleaned = re.sub(rf"\b{re.escape(original)}\b", replacement, cleaned, flags=re.IGNORECASE)
        parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]
        return " ".join(parts[:2])

    @staticmethod
    def _generate_flashcards(sections: Dict[str, str]) -> List[Dict]:
        prompts = {
            "hook": "What is this lesson about in one simple sentence?",
            "analogy": "What everyday analogy explains this idea?",
            "core_concept": "What is the core idea, in plain words?",
            "visual_description": "What picture should you see in your head for this concept?",
            "real_example": "What is one real situation where this shows up?",
            "why_it_matters": "Why does this matter in real work?",
            "practice_scenario": "What should you do in the practice scenario?",
            "common_mistake": "What mistake should you avoid first?",
        }
        cues = {
            "hook": "Start broad",
            "analogy": "Use simple comparisons",
            "core_concept": "Keep words short",
            "visual_description": "Describe left, right, and secure path",
            "real_example": "Use one concrete case",
            "why_it_matters": "Connect to outcomes",
            "practice_scenario": "Explain your next action",
            "common_mistake": "Name the trap and the fix",
        }

        cards: List[Dict] = []
        for key, text in sections.items():
            cleaned = str(text).strip()
            if not cleaned:
                continue
            cards.append(
                {
                    "id": key,
                    "front": prompts.get(key, f"Explain {key.replace('_', ' ')} in your own words."),
                    "back": cleaned,
                    "cue": cues.get(key, "Use simple words"),
                }
            )

        core = sections.get("core_concept", "").strip()
        mistake = sections.get("common_mistake", "").strip()
        if core:
            cards.append(
                {
                    "id": "transfer-path-check",
                    "front": "When would you stop the flow and re-check before sending files?",
                    "back": mistake or core,
                    "cue": "State trigger, risk, and correction",
                }
            )
        return cards
    
    async def generate_audio_teaching(
        self,
        teaching_content: Dict,
        voice_style: str = "energetic_teacher",
        voice_profile: Optional[str] = None,
    ) -> Dict:
        """
        Generate TTS audio for the teaching session.
        Uses a single synthesis pass for the full lesson to keep startup under 60s.
        """
        from app.services.tts_service import TTSService

        tts_service = TTSService()
        sections = teaching_content.get("sections", {})
        ordered_keys = [key for key in self.SECTION_ORDER if sections.get(key)]
        section_items = [(key, str(sections[key])) for key in ordered_keys]
        if not section_items:
            return {
                "total_duration_seconds": 0.0,
                "segments": [],
                "voice_style": voice_style,
                "voice_profile": voice_profile or "",
            }

        subtitle_lines: list[tuple[str, str]] = []
        for section_name, section_text in section_items:
            subtitle = self._subtitle_line(section_name, section_text)
            if subtitle:
                subtitle_lines.append((section_name, subtitle))

        if not subtitle_lines:
            return {
                "total_duration_seconds": 0.0,
                "segments": [],
                "voice_style": voice_style,
                "voice_profile": voice_profile or "",
            }

        narration_text = " ".join(line for _, line in subtitle_lines).strip()
        if len(narration_text) > 720:
            narration_text = narration_text[:720].rsplit(" ", 1)[0] + "."

        try:
            audio_path = await asyncio.wait_for(
                asyncio.to_thread(
                    tts_service.synthesize,
                    narration_text,
                    1.25,
                    "teaching",
                    self._extract_key_terms(narration_text)[:12],
                    voice_profile,
                ),
                timeout=35.0,
            )
        except Exception:
            return {
                "total_duration_seconds": 0.0,
                "segments": [],
                "voice_style": voice_style,
                "voice_profile": voice_profile or "",
            }

        if not str(audio_path).lower().endswith((".wav", ".mp3", ".ogg")):
            return {
                "total_duration_seconds": 0.0,
                "segments": [],
                "voice_style": voice_style,
                "voice_profile": voice_profile or "",
            }

        total_words = max(len(narration_text.split()), 1)
        total_duration = (total_words / 150.0) * 60.0
        section_word_counts = [max(len(line.split()), 1) for _, line in subtitle_lines]
        total_section_words = sum(section_word_counts)

        audio_segments: List[Dict] = []
        for index, (section_name, subtitle_text) in enumerate(subtitle_lines):
            ratio = section_word_counts[index] / max(total_section_words, 1)
            audio_segments.append(
                {
                    "section": section_name,
                    "audio_path": audio_path,
                    "duration_seconds": max(total_duration * ratio, 1.0),
                    "text": subtitle_text,
                }
            )

        return {
            "total_duration_seconds": total_duration,
            "segments": audio_segments,
            "voice_style": voice_style,
            "voice_profile": voice_profile or "",
        }

    def _normalize_sections(
        self,
        *,
        concept_name: str,
        concept_explanation: str,
        source_chunks: List[str],
        sections: Dict,
    ) -> Dict[str, str]:
        if not isinstance(sections, dict):
            sections = {}

        def _value(key: str) -> str:
            return self._trim_for_prompt(str(sections.get(key, "")).strip(), 420)

        normalized: Dict[str, str] = {
            "hook": _value("hook") or f"Alright, quick win: {concept_name} is easier than it sounds.",
            "analogy": _value("analogy") or f"Think of {concept_name} like a locked delivery lane for business files.",
            "core_concept": _value("core_concept") or self._plain_summary(concept_explanation, concept_name),
            "visual_description": _value("visual_description")
            or f"Picture this: {concept_name} starts on the sender side, moves through a verified secure path, and lands at the receiver with checks logged.",
            "real_example": _value("real_example")
            or f"A partner drops a purchase-order file, validation runs, and the transfer completes only after identity and integrity checks pass.",
            "why_it_matters": _value("why_it_matters")
            or "If this step fails, files can be delayed or rejected. If it works, partner delivery stays safe and reliable.",
            "practice_scenario": _value("practice_scenario")
            or f"A partner file must move today. How would you apply {concept_name} so delivery is secure and predictable?",
            "common_mistake": _value("common_mistake")
            or "Teams often skip pre-transfer checks and only notice failures after the handoff window closes.",
            "encouragement": _value("encouragement") or "Nice progress. One clear step at a time and you will own this topic.",
        }

        # Keep order stable for deterministic UI progression and flashcards.
        ordered: Dict[str, str] = {}
        for key in self.SECTION_ORDER:
            ordered[key] = normalized.get(key, "").strip()

        source_hint = self._first_source_hint(source_chunks)
        if source_hint and source_hint.lower() not in ordered["core_concept"].lower():
            ordered["core_concept"] = f"{ordered['core_concept']} Source hint: {source_hint}.".strip()
        if source_hint and source_hint.lower() not in ordered["real_example"].lower():
            ordered["real_example"] = f"{ordered['real_example']} Grounding: {source_hint}.".strip()

        return ordered

    @staticmethod
    def _subtitle_line(section_name: str, section_text: str) -> str:
        cleaned = re.sub(r"\s+", " ", str(section_text or "")).strip()
        if not cleaned:
            return ""

        sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", cleaned) if item.strip()]
        lead = " ".join(sentences[:2]) if sentences else cleaned
        lead = lead[:220].rsplit(" ", 1)[0] + "." if len(lead) > 220 else lead
        label = section_name.replace("_", " ").title()
        return f"{label}. {lead}".strip()

    @staticmethod
    def _first_source_hint(source_chunks: List[str]) -> str:
        for chunk in source_chunks:
            cleaned = chunk.strip()
            if not cleaned:
                continue
            sentence = re.split(r"(?<=[.!?])\s+", cleaned)[0].strip("- ")
            if sentence:
                return InteractiveTeacherService._trim_for_prompt(sentence, 120)
        return ""

    @staticmethod
    def _trim_for_prompt(text: str, limit: int) -> str:
        cleaned = re.sub(r"\s+", " ", text or "").strip()
        if len(cleaned) <= limit:
            return cleaned
        return cleaned[:limit].rsplit(" ", 1)[0].strip() + "..."

    async def assess_comprehension(
        self,
        concept_name: str,
        learner_summary: str,
        learner_example: str,
        learner_failure_mode: str,
        source_chunks: List[str],
    ) -> Dict:
        grounding_notes = "\n".join(source_chunks[:4])
        prompt = f"""Evaluate if this learner genuinely understands {concept_name}.

Learner summary:
{learner_summary}

Learner example:
{learner_example}

Learner failure mode:
{learner_failure_mode}

Grounding notes:
{grounding_notes}

Return JSON with:
- understood: boolean
- score: integer 0-100
- feedback: 2-3 short sentences in plain language
- next_step: one of ready_for_question or needs_reteach"""

        try:
            raw = await self.ollama.chat(
                task="teacher",
                system_prompt=(
                    "You are a strict but kind tutor. Evaluate understanding without jargon. "
                    "Use plain-language coaching."
                ),
                user_prompt=prompt,
                temperature=0.2,
                timeout=90.0,
            )
            parsed = self._safe_parse_json(raw)
            if parsed:
                understood = bool(parsed.get("understood", False))
                score = int(parsed.get("score", 0))
                next_step = str(parsed.get("next_step", "needs_reteach"))
                if next_step not in {"ready_for_question", "needs_reteach"}:
                    next_step = "needs_reteach"
                return {
                    "understood": understood,
                    "score": max(0, min(score, 100)),
                    "feedback": str(parsed.get("feedback", "Let's tighten your understanding with one more explanation.")).strip(),
                    "next_step": next_step,
                }
        except Exception:
            pass

        return self._heuristic_comprehension(learner_summary, learner_example, learner_failure_mode)
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms that should be emphasized in speech
        """
        # Simple extraction - can be enhanced with NLP
        key_indicators = ["important", "crucial", "key", "remember", "note"]
        words = text.split()
        key_terms = []
        
        for i, word in enumerate(words):
            if word.lower() in key_indicators and i + 1 < len(words):
                key_terms.append(words[i + 1])
        
        return key_terms
    
    async def stream_teaching_session(
        self,
        concept_name: str,
        concept_explanation: str,
        source_chunks: List[str]
    ):
        """
        Stream teaching content in real-time (for progressive rendering)
        """
        # Generate teaching content
        teaching_content = await self.generate_teaching_session(
            concept_name,
            concept_explanation,
            source_chunks
        )
        
        # Yield each section progressively
        for section_name, section_text in teaching_content["sections"].items():
            yield {
                "section": section_name,
                "content": section_text,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            # Small delay between sections for natural pacing
            await asyncio.sleep(0.5)

    @staticmethod
    def _safe_parse_json(raw: str) -> Dict:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _heuristic_comprehension(summary: str, example: str, failure_mode: str) -> Dict:
        lengths = [len(summary.split()), len(example.split()), len(failure_mode.split())]
        score = min(100, int(sum(min(part, 20) for part in lengths) * (100 / 60)))
        understood = score >= 65
        if understood:
            feedback = "Nice work. You explained the idea, gave a concrete example, and described what can go wrong."
            next_step = "ready_for_question"
        else:
            feedback = (
                "You are close, but parts are still vague. Use simpler words, give one concrete situation, "
                "and describe one specific failure."
            )
            next_step = "needs_reteach"
        return {
            "understood": understood,
            "score": score,
            "feedback": feedback,
            "next_step": next_step,
        }
