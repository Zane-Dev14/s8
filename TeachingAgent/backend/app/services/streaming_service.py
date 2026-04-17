"""
Streaming Service - Server-Sent Events for real-time text generation
Fixes the 20-30s wait by streaming tokens as they're generated
"""
import asyncio
import json
from typing import AsyncGenerator, Dict, Any

import httpx

from app.core.settings import settings


class StreamingService:
    """
    Handles streaming responses from Ollama to frontend via SSE.
    Every text generation MUST use this service.
    """

    def __init__(self):
        self.ollama_url = settings.ollama_base_url

    async def stream_chat(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion token by token.
        
        Yields:
            JSON strings with format: {"token": "word", "done": false}
            Final message: {"done": true}
        """
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    f"{self.ollama_url}/api/chat",
                    json=payload,
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        
                        try:
                            data = json.loads(line)
                            
                            # Check if generation is complete
                            if data.get("done", False):
                                yield json.dumps({"done": True})
                                break
                            
                            # Extract token from message
                            message = data.get("message", {})
                            token = message.get("content", "")
                            
                            if token:
                                yield json.dumps({"token": token, "done": False})
                        
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            # Send error as final message
            yield json.dumps({"error": str(e), "done": True})

    async def stream_generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
    ) -> AsyncGenerator[str, None]:
        """
        Stream text generation token by token (simpler API).
        
        Yields:
            JSON strings with format: {"token": "word", "done": false}
            Final message: {"done": true}
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        
                        try:
                            data = json.loads(line)
                            
                            if data.get("done", False):
                                yield json.dumps({"done": True})
                                break
                            
                            token = data.get("response", "")
                            if token:
                                yield json.dumps({"token": token, "done": False})
                        
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            yield json.dumps({"error": str(e), "done": True})

    async def stream_teaching_section(
        self,
        concept_name: str,
        section_name: str,
        context_chunks: list[str],
        section_type: str,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a single teaching section (hook, analogy, core, etc.)
        
        Args:
            concept_name: Name of the concept being taught
            section_name: Which section (hook, analogy, core_concept, etc.)
            context_chunks: RAG context from source material
            section_type: Type of section for prompt customization
        
        Yields:
            Tokens as they're generated
        """
        # Build section-specific prompt
        prompt = self._build_section_prompt(
            concept_name, section_name, context_chunks, section_type
        )
        
        system_prompt = (
            "You are a technical exam coach. Explain concepts clearly with focus on "
            "exam patterns, definitions, formulas, and PYQ trends. Be concise and precise. "
            "Include technical terms with brief explanations. Max 4-5 sentences per section."
        )
        
        # Stream using fast model with more tokens for technical content
        async for chunk in self.stream_chat(
            model=settings.model_fast,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.3,  # Lower for more precise technical content
            max_tokens=250,  # More tokens for detailed explanations
        ):
            yield chunk

    def _build_section_prompt(
        self,
        concept_name: str,
        section_name: str,
        context_chunks: list[str],
        section_type: str,
    ) -> str:
        """Build prompt for specific teaching section"""
        
        context = "\n".join(f"- {chunk[:200]}" for chunk in context_chunks[:4])
        
        prompts = {
            "hook": f"State why {concept_name} is critical for exams. Mention typical marks allocation and PYQ frequency. 2-3 sentences.",
            "analogy": f"Provide a technical comparison for {concept_name} with a related concept. Highlight key differences. 3-4 sentences.",
            "core": f"Define {concept_name} precisely. Include formula/algorithm if applicable. List key characteristics. 4-5 sentences.\n\nContext:\n{context}",
            "visual": f"Describe the architecture/structure of {concept_name}. Mention components, data flow, and interactions. 3-4 sentences.",
            "example": f"Provide a detailed technical example of {concept_name} from the source material. Include steps and outcomes. 4-5 sentences.\n\nContext:\n{context}",
            "mistake": f"Explain the most common exam mistake for {concept_name}. Provide the correct approach with reasoning. 3-4 sentences.",
            "practice": f"Give a PYQ-style scenario for {concept_name}. Ask what approach to use and why. 2-3 sentences.",
            "encouragement": f"Summarize key exam points for {concept_name}. Mention what examiners look for. 2-3 sentences.",
        }
        
        return prompts.get(section_name, f"Explain {section_name} for {concept_name} in 2-3 simple sentences.")

    async def stream_quiz_evaluation(
        self,
        concept_name: str,
        question: str,
        user_answer: str,
        correct_answer: str,
        context_chunks: list[str],
    ) -> AsyncGenerator[str, None]:
        """
        Stream evaluation of user's quiz answer.
        Uses eval model for accuracy.
        """
        context = "\n".join(f"- {chunk[:200]}" for chunk in context_chunks[:3])
        
        prompt = f"""Evaluate this answer about {concept_name}.

Question: {question}
User's answer: {user_answer}
Correct answer: {correct_answer}

Context from source:
{context}

Is the user correct? Provide brief feedback in plain language (2-3 sentences).
Start with "Correct!" or "Not quite." then explain."""

        system_prompt = (
            "You are a strict but kind tutor. Evaluate understanding without jargon. "
            "Use plain-language coaching."
        )

        async for chunk in self.stream_chat(
            model=settings.model_eval,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.2,
            max_tokens=200,
        ):
            yield chunk

    async def collect_full_response(
        self,
        stream_generator: AsyncGenerator[str, None]
    ) -> str:
        """
        Collect full response from a stream (for non-streaming contexts).
        Use sparingly - prefer streaming to frontend.
        """
        tokens = []
        async for chunk_json in stream_generator:
            try:
                data = json.loads(chunk_json)
                if data.get("done"):
                    break
                if "token" in data:
                    tokens.append(data["token"])
            except json.JSONDecodeError:
                continue
        
        return "".join(tokens)

# Made with Bob
