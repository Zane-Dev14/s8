from __future__ import annotations

import json
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db import Concept, ConceptEdge, ContentChunk
from app.services.ollama_router import OllamaRouter


class KnowledgeGraphService:
    def __init__(self, db: Session, router: OllamaRouter):
        self.db = db
        self.router = router

    async def build_graph(self) -> tuple[int, int]:
        chunks = list(self.db.scalars(select(ContentChunk)).all())
        if not chunks:
            return 0, 0

        concept_specs = await self._extract_concepts(chunks)
        concept_by_name: dict[str, Concept] = {}

        for spec in concept_specs:
            # Validate spec has required fields
            if not isinstance(spec, dict) or "name" not in spec:
                print(f"Skipping invalid concept spec: {spec}")
                continue
                
            name = spec["name"].strip()
            if not name:
                continue
            existing = concept_by_name.get(name.lower())
            if existing:
                continue

            concept = Concept(
                name=name,
                why_it_matters=spec.get("why_it_matters", ""),
                intuition=spec.get("intuition", ""),
                explanation=spec.get("explanation", ""),
                example=spec.get("example", ""),
                common_mistake=spec.get("common_mistake", ""),
                checkpoint_question=spec.get("checkpoint_question", ""),
                hard_follow_up=spec.get("hard_follow_up", ""),
                source_reference=spec.get("source_reference", ""),
            )
            self.db.add(concept)
            self.db.flush()
            concept_by_name[name.lower()] = concept
            print(f"  ✓ Created concept: {name}")

        self.db.commit()

        concept_list = list(self.db.scalars(select(Concept)).all())
        edges_inserted = self._build_edges(concept_list)
        return len(concept_list), edges_inserted

    async def _extract_concepts(self, chunks: list[ContentChunk]) -> list[dict[str, str]]:
        # Group chunks by source to get better context
        chunks_by_source: dict[str, list[ContentChunk]] = {}
        for chunk in chunks:
            source = chunk.source_reference or "unknown"
            chunks_by_source.setdefault(source, []).append(chunk)
        
        # Find the main bootcamp topics PDF
        bootcamp_pdf = None
        for src in chunks_by_source.keys():
            if "bootcamp-topics" in src.lower() or "bb101" in src.lower() and ".pdf" in src.lower():
                bootcamp_pdf = src
                break
        
        # Build text prioritizing bootcamp PDF
        text_parts = []
        if bootcamp_pdf:
            print(f"  Found bootcamp PDF: {bootcamp_pdf}")
            pdf_chunks = chunks_by_source[bootcamp_pdf]
            pdf_text = "\n".join(c.text for c in pdf_chunks[:100])  # More chunks from main PDF
            text_parts.append(f"=== MAIN CURRICULUM: {bootcamp_pdf} ===\n{pdf_text}\n")
        
        # Add other important documents
        priority_sources = [
            src for src in chunks_by_source.keys()
            if src != bootcamp_pdf and any(ext in src.lower() for ext in ['.pdf', '.docx', '.txt'])
            and not any(skip in src.lower() for skip in ['ppk', 'exe', 'xlsx', 'mp4'])
        ]
        
        for source in priority_sources[:5]:  # Top 5 additional sources
            source_chunks = chunks_by_source[source][:20]
            source_text = "\n".join(c.text for c in source_chunks)
            text_parts.append(f"=== {source} ===\n{source_text}\n")
        
        merged_text = "\n\n".join(text_parts)[:100000]  # 100K char limit
        print(f"  Analyzing {len(merged_text)} characters from {len(text_parts)} sources")
        
        system = (
            "You are an expert at extracting learning concepts from technical training materials. "
            "Analyze the bootcamp content and identify the KEY TOPICS that learners need to master. "
            "Focus on:\n"
            "- Core technologies and protocols (SFTP, HTTP, EDI, etc.)\n"
            "- Key product features (Mailboxes, Business Processes, Maps, etc.)\n"
            "- Important concepts (Routing, Transformation, Security, etc.)\n"
            "- Practical skills (Configuration, Troubleshooting, Development, etc.)\n\n"
            "IGNORE:\n"
            "- Generic words like 'Name', 'Description', 'Format'\n"
            "- Technical codes like 'U0000', 'U00FF'\n"
            "- File extensions or binary data\n\n"
            "Return ONLY a JSON array. Each concept must have:\n"
            "{\n"
            '  "name": "Clear, specific concept name",\n'
            '  "why_it_matters": "Why this is important for B2B integration",\n'
            '  "intuition": "Simple analogy or mental model",\n'
            '  "explanation": "Technical explanation with key details",\n'
            '  "example": "Concrete example from the bootcamp",\n'
            '  "common_mistake": "What learners often get wrong",\n'
            '  "checkpoint_question": "Question to verify understanding",\n'
            '  "hard_follow_up": "Advanced question for mastery",\n'
            '  "source_reference": "Which file/section this came from"\n'
            "}\n\n"
            "Extract 8-15 high-quality concepts. Return ONLY the JSON array, no other text."
        )
        
        user = (
            "Analyze this IBM Sterling B2B Integrator bootcamp content and extract the key learning concepts.\n"
            "Focus on topics that appear in lesson titles, headings, and repeated explanations.\n\n"
            f"BOOTCAMP CONTENT:\n{merged_text}\n\n"
            "Return the JSON array of concepts:"
        )
        
        try:
            print("  Sending request to Ollama...")
            raw = await self.router.chat("knowledge_graph", system, user, temperature=0.1, timeout=300.0)
            print(f"  Received response ({len(raw)} chars)")
            print(f"  First 500 chars: {raw[:500]}")
            
            parsed = self._safe_parse_array(raw)
            print(f"  Parsed {len(parsed)} concepts from response")
            
            if parsed and len(parsed) >= 5:  # Need at least 5 good concepts
                return parsed
            else:
                print(f"  Not enough valid concepts ({len(parsed)}), using heuristic fallback")
        except Exception as e:
            print(f"  Ollama extraction failed: {e}, falling back to heuristic")
        
        print("  Using heuristic concept extraction...")
        return self._heuristic_concepts(chunks)

    def _build_edges(self, concepts: list[Concept]) -> int:
        self.db.query(ConceptEdge).delete()
        self.db.commit()

        edges = 0
        for index, concept in enumerate(concepts):
            next_window = concepts[index + 1 : index + 3]
            for target in next_window:
                edge = ConceptEdge(
                    source_concept_id=concept.id,
                    target_concept_id=target.id,
                    edge_type="depends_on" if index % 2 == 0 else "part_of",
                )
                self.db.add(edge)
                edges += 1

        self.db.commit()
        return edges

    @staticmethod
    def _safe_parse_array(raw: str) -> list[dict[str, str]]:
        raw = raw.strip()
        if not raw:
            return []
        match = re.search(r"\[[\s\S]*\]", raw)
        if not match:
            return []
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            return []
        if not isinstance(parsed, list):
            return []

        normalized: list[dict[str, str]] = []
        for item in parsed:
            if isinstance(item, dict):
                # Normalize keys - handle variations like "concept" vs "name"
                normalized_item: dict[str, str] = {}
                for key, value in item.items():
                    key_lower = str(key).lower()
                    # Map common variations to expected keys
                    if key_lower in ["concept", "topic", "title"]:
                        normalized_item["name"] = str(value)
                    elif key_lower in ["explanation", "description", "details"]:
                        normalized_item["explanation"] = str(value)
                    elif key_lower in ["mistake", "common_mistake", "pitfall"]:
                        normalized_item["common_mistake"] = str(value)
                    else:
                        normalized_item[str(key)] = str(value)
                
                # Only include if we have at least a name
                if "name" in normalized_item:
                    normalized.append(normalized_item)
        
        return normalized

    @staticmethod
    def _heuristic_concepts(chunks: list[ContentChunk]) -> list[dict[str, str]]:
        frequency: dict[str, int] = {}
        source_for_word: dict[str, str] = {}

        for chunk in chunks:
            words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", chunk.text)
            for word in words:
                key = word.lower()
                frequency[key] = frequency.get(key, 0) + 1
                source_for_word.setdefault(key, chunk.source_reference)

        ranked = sorted(frequency.items(), key=lambda item: item[1], reverse=True)[:16]
        concepts: list[dict[str, str]] = []
        for word, _count in ranked:
            title = word.replace("_", " ").title()
            concepts.append(
                {
                    "name": title,
                    "why_it_matters": f"{title} appears repeatedly and influences workflow behavior.",
                    "intuition": f"Think of {title} as a control point in the B2Bi flow.",
                    "explanation": f"{title} is referenced across source artifacts and should be mastered early.",
                    "example": f"Observed in source path {source_for_word[word]}",
                    "common_mistake": f"Treating {title} as isolated rather than linked to upstream/downstream steps.",
                    "checkpoint_question": f"Where does {title} appear in the timeline, and what does it trigger?",
                    "hard_follow_up": f"Explain how {title} changes behavior under failure conditions.",
                    "source_reference": source_for_word[word],
                }
            )
        return concepts
