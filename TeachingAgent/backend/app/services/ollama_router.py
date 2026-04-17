from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any

import httpx

from app.core.settings import settings


@dataclass(frozen=True)
class TaskModels:
    parser: str
    chunker: str
    graph: str
    teacher: str
    teacher_fallback: str
    quiz: str
    fast_ui: str
    coding: str


class OllamaRouter:
    def __init__(self) -> None:
        self.models = TaskModels(
            parser=settings.model_parser,
            chunker=settings.model_chunker,
            graph=settings.model_graph,
            teacher=settings.model_teacher,
            teacher_fallback=settings.model_teacher_fallback,
            quiz=settings.model_quiz,
            fast_ui=settings.model_fast_ui,
            coding=settings.model_coding,
        )

    @staticmethod
    def _task_to_model(task: str, models: TaskModels) -> str:
        mapping = {
            "parser": models.parser,
            "chunker": models.chunker,
            "knowledge_graph": models.graph,
            "teacher": models.teacher,
            "teacher_fallback": models.teacher_fallback,
            "quiz": models.quiz,
            "fast_ui": models.fast_ui,
            "coding": models.coding,
        }
        return mapping.get(task, models.fast_ui)

    @staticmethod
    def _task_model_candidates(task: str, models: TaskModels) -> list[str]:
        preferred = OllamaRouter._task_to_model(task, models)
        if task == "teacher":
            return [preferred, models.teacher_fallback, models.fast_ui]
        if task == "quiz":
            return [preferred, models.fast_ui, models.teacher_fallback]
        return [preferred, models.fast_ui] if preferred != models.fast_ui else [models.fast_ui]

    async def chat(self, task: str, system_prompt: str, user_prompt: str, temperature: float = 0.2, timeout: float = 90.0) -> str:
        candidates = self._task_model_candidates(task, self.models)
        last_error: Exception | None = None
        # Allow heavier local models enough time while still enforcing an upper bound.
        total_budget_sec = min(max(timeout, 2.0), 45.0)
        deadline = time.monotonic() + total_budget_sec

        for model in candidates:
            remaining = deadline - time.monotonic()
            if remaining <= 0.5:
                break
            payload: dict[str, Any] = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
                "options": {"temperature": temperature},
            }
            try:
                per_model_timeout = min(max(remaining - 0.1, 0.5), 30.0)
                async with httpx.AsyncClient(timeout=per_model_timeout) as client:
                    response = await client.post(f"{settings.ollama_base_url}/api/chat", json=payload)
                    response.raise_for_status()
                    body = response.json()
                message = body.get("message", {})
                content = str(message.get("content", "")).strip()
                if content:
                    return content
            except Exception as exc:  # pragma: no cover - network/model availability
                last_error = exc
                continue

        if last_error:
            raise last_error
        raise RuntimeError("No model response was returned.")

    async def embeddings(self, text: str) -> list[float]:
        payload = {
            "model": self.models.parser,
            "prompt": text,
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(f"{settings.ollama_base_url}/api/embeddings", json=payload)
            if response.status_code >= 400:
                return self._hash_embedding(text)
            data = response.json()
        embedding = data.get("embedding")
        if isinstance(embedding, list) and embedding:
            return [float(x) for x in embedding]
        return self._hash_embedding(text)

    @staticmethod
    def _hash_embedding(text: str, width: int = 128) -> list[float]:
        vector = [0.0] * width
        for index, char in enumerate(text):
            slot = (ord(char) + index) % width
            vector[slot] += 1.0
        norm = sum(value * value for value in vector) ** 0.5
        if norm == 0:
            return vector
        return [value / norm for value in vector]
