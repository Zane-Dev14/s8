"""
Domain-Agnostic Concept Extraction Service
Extracts learning concepts from any subject's materials without hardcoded domain knowledge
"""
import json
from typing import Dict, List, Optional

from app.services.streaming_service import StreamingService
from app.core.settings import settings


class ConceptExtractionService:
    """
    Extracts concepts from educational materials in a domain-agnostic way.
    No hardcoded assumptions about SFTP, Mailbox, or any specific domain.
    """

    def __init__(self):
        self.streaming = StreamingService()

    async def extract_concepts(
        self,
        subject_name: str,
        content_chunks: List[str],
        max_concepts: int = 20,
    ) -> List[Dict]:
        """
        Extract key learning concepts from subject materials.
        
        Args:
            subject_name: Name of the subject (e.g., "Networking", "Blockchain")
            content_chunks: Text chunks from source materials
            max_concepts: Maximum number of concepts to extract
        
        Returns:
            List of concept dicts with: name, plain_name, difficulty, explanation, etc.
        """
        # Build context from chunks
        context = self._build_context(content_chunks)
        
        # Generate extraction prompt
        prompt = self._build_extraction_prompt(subject_name, context, max_concepts)
        
        system_prompt = (
            "You are an expert at extracting learning concepts from educational materials. "
            "Analyze content and identify KEY TOPICS that learners need to master. "
            "Focus on concepts that appear repeatedly, have clear explanations, and build on each other. "
            "Return valid JSON only."
        )
        
        # Stream response and collect
        response_stream = self.streaming.stream_chat(
            model=settings.model_eval,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.3,
            max_tokens=2000,
        )
        
        response_text = await self.streaming.collect_full_response(response_stream)
        
        # Parse JSON response
        concepts = self._parse_concepts_response(response_text)
        
        # Validate and clean concepts
        return self._validate_concepts(concepts, subject_name)

    def _build_context(self, content_chunks: List[str], max_chars: int = 8000) -> str:
        """Build context string from content chunks"""
        context_parts = []
        total_chars = 0
        
        for chunk in content_chunks:
            chunk_text = chunk.strip()
            if not chunk_text:
                continue
            
            # Truncate chunk if too long
            if len(chunk_text) > 500:
                chunk_text = chunk_text[:500] + "..."
            
            if total_chars + len(chunk_text) > max_chars:
                break
            
            context_parts.append(f"- {chunk_text}")
            total_chars += len(chunk_text)
        
        return "\n".join(context_parts)

    def _build_extraction_prompt(
        self,
        subject_name: str,
        context: str,
        max_concepts: int,
    ) -> str:
        """Build domain-agnostic extraction prompt"""
        return f"""Analyze this {subject_name} educational content and extract the key learning concepts.

CONTENT:
{context}

Extract up to {max_concepts} concepts that:
1. Appear repeatedly or are emphasized in the content
2. Have clear explanations or examples
3. Build on each other (some concepts depend on others)
4. Are essential for understanding {subject_name}

For each concept, provide:
- name: The technical/formal name
- plain_name: A simple, jargon-free name (e.g., "How data moves securely" not "SFTP protocol")
- difficulty: "beginner", "intermediate", or "advanced"
- explanation: 2-3 sentence technical explanation
- example: One concrete example from the content
- common_mistake: What learners often get wrong
- prerequisites: List of concept names this depends on (empty list if none)

Return ONLY valid JSON in this format:
{{
  "concepts": [
    {{
      "name": "Concept Name",
      "plain_name": "Simple Name",
      "difficulty": "beginner",
      "explanation": "Technical explanation...",
      "example": "Concrete example...",
      "common_mistake": "Common error...",
      "prerequisites": ["Other Concept"]
    }}
  ]
}}

Return JSON only, no markdown fences."""

    def _parse_concepts_response(self, response_text: str) -> List[Dict]:
        """Parse JSON response from LLM"""
        try:
            # Try direct JSON parse
            data = json.loads(response_text)
            if isinstance(data, dict) and "concepts" in data:
                return data["concepts"]
            return []
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown fences
        import re
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*\})\s*```', response_text)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                if isinstance(data, dict) and "concepts" in data:
                    return data["concepts"]
            except json.JSONDecodeError:
                pass
        
        # Try to find any JSON object
        json_match = re.search(r'\{[\s\S]*"concepts"[\s\S]*\}', response_text)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                if isinstance(data, dict) and "concepts" in data:
                    return data["concepts"]
            except json.JSONDecodeError:
                pass
        
        return []

    def _validate_concepts(
        self,
        concepts: List[Dict],
        subject_name: str,
    ) -> List[Dict]:
        """Validate and clean extracted concepts"""
        validated = []
        
        for concept in concepts:
            if not isinstance(concept, dict):
                continue
            
            # Required fields
            name = concept.get("name", "").strip()
            if not name:
                continue
            
            # Build validated concept
            validated_concept = {
                "name": name,
                "plain_name": concept.get("plain_name", name).strip(),
                "difficulty": self._validate_difficulty(concept.get("difficulty", "beginner")),
                "explanation": concept.get("explanation", "").strip()[:1000],
                "example": concept.get("example", "").strip()[:1000],
                "common_mistake": concept.get("common_mistake", "").strip()[:500],
                "prerequisites": self._validate_prerequisites(concept.get("prerequisites", [])),
                "why_it_matters": concept.get("why_it_matters", f"Essential for understanding {subject_name}").strip()[:500],
            }
            
            validated.append(validated_concept)
        
        return validated

    @staticmethod
    def _validate_difficulty(difficulty: str) -> str:
        """Ensure difficulty is valid"""
        valid = ["beginner", "intermediate", "advanced"]
        difficulty = difficulty.lower().strip()
        return difficulty if difficulty in valid else "beginner"

    @staticmethod
    def _validate_prerequisites(prerequisites) -> List[str]:
        """Ensure prerequisites is a list of strings"""
        if not isinstance(prerequisites, list):
            return []
        
        return [str(p).strip() for p in prerequisites if p]

    async def build_concept_graph(
        self,
        concepts: List[Dict],
    ) -> Dict[str, List[Dict]]:
        """
        Build dependency graph from extracted concepts.
        
        Returns:
            Dict mapping concept_name -> list of edges
            Each edge: {"target": concept_name, "type": "depends_on"|"part_of"|"related_to"}
        """
        graph = {}
        concept_names = {c["name"] for c in concepts}
        
        for concept in concepts:
            name = concept["name"]
            edges = []
            
            # Add prerequisite edges
            for prereq in concept.get("prerequisites", []):
                if prereq in concept_names:
                    edges.append({
                        "target": prereq,
                        "type": "depends_on"
                    })
            
            graph[name] = edges
        
        return graph

    async def enrich_concept_with_rag(
        self,
        concept: Dict,
        content_chunks: List[str],
    ) -> Dict:
        """
        Enrich a concept with additional details from RAG context.
        
        Args:
            concept: Base concept dict
            content_chunks: Relevant content chunks
        
        Returns:
            Enriched concept with better examples and explanations
        """
        context = self._build_context(content_chunks[:5], max_chars=2000)
        
        prompt = f"""Enrich this concept with details from the source material.

CONCEPT: {concept['name']}
CURRENT EXPLANATION: {concept.get('explanation', '')}

SOURCE MATERIAL:
{context}

Provide:
1. A better real-world example grounded in the source material
2. A more specific common mistake with how to avoid it
3. Why this concept matters (2 sentences)

Return JSON:
{{
  "example": "Concrete example from source...",
  "common_mistake": "Specific mistake and fix...",
  "why_it_matters": "Why this is important..."
}}"""

        system_prompt = "You ground concepts in source material. Return valid JSON only."
        
        response_stream = self.streaming.stream_chat(
            model=settings.model_eval,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.2,
            max_tokens=400,
        )
        
        response_text = await self.streaming.collect_full_response(response_stream)
        
        try:
            enrichment = json.loads(response_text)
            concept["example"] = enrichment.get("example", concept.get("example", ""))
            concept["common_mistake"] = enrichment.get("common_mistake", concept.get("common_mistake", ""))
            concept["why_it_matters"] = enrichment.get("why_it_matters", concept.get("why_it_matters", ""))
        except json.JSONDecodeError:
            pass  # Keep original values
        
        return concept

# Made with Bob
