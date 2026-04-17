from __future__ import annotations

import json
import re
from dataclasses import dataclass
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.db import ContentChunk, ParsedDocument, SourceFile, TranscriptSegment
from app.services.ollama_router import OllamaRouter


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: ContentChunk
    score: float


class ChunkingService:
    def __init__(self, db: Session, router: OllamaRouter):
        self.db = db
        self.router = router

    def chunk_all(self, job_id: str) -> int:
        inserted = 0
        files = list(self.db.scalars(select(SourceFile).where(SourceFile.job_id == job_id)).all())

        for source_file in files:
            if source_file.is_video:
                segments = list(
                    self.db.scalars(
                        select(TranscriptSegment).where(TranscriptSegment.source_file_id == source_file.id)
                    ).all()
                )
                segments.sort(key=lambda item: item.start_sec)
                for index, segment in enumerate(segments):
                    previous = segments[index - 1] if index > 0 else None
                    for chunk_type, chunk_text in self._chunk_video_segment(source_file, segment, previous):
                        chunk = ContentChunk(
                            source_file_id=source_file.id,
                            transcript_segment_id=segment.id,
                            chunk_type=chunk_type,
                            text=chunk_text,
                            source_reference=(
                                f"{source_file.path}@{int(segment.start_sec)}-{int(segment.end_sec)}s"
                            ),
                        )
                        self.db.add(chunk)
                        inserted += 1
                continue

            parsed_docs = list(
                self.db.scalars(select(ParsedDocument).where(ParsedDocument.source_file_id == source_file.id)).all()
            )
            for parsed_doc in parsed_docs:
                for chunk_type, chunk_text in self._build_concept_bundle_chunks(parsed_doc.full_text):
                    chunk = ContentChunk(
                        source_file_id=source_file.id,
                        chunk_type=chunk_type,
                        text=chunk_text,
                        source_reference=source_file.path,
                    )
                    self.db.add(chunk)
                    inserted += 1

        self.db.commit()
        return inserted

    async def embed_chunks(self, job_id: str) -> int:
        chunks = list(
            self.db.scalars(
                select(ContentChunk).join(SourceFile, SourceFile.id == ContentChunk.source_file_id).where(SourceFile.job_id == job_id)
            ).all()
        )
        updated = 0
        for chunk in chunks:
            if chunk.embedding_json and chunk.embedding_json != "[]":
                continue
            embedding = await self.router.embeddings(chunk.text)
            chunk.embedding_json = json.dumps(embedding)
            self.db.add(chunk)
            updated += 1
        self.db.commit()
        return updated

    def retrieve_relevant_chunks_with_scores(self, query: str, limit: int = 6) -> list[RetrievedChunk]:
        chunks = list(self.db.scalars(select(ContentChunk)).all())
        if not chunks:
            return []

        query_tokens = self._tokenize(query)
        scored: list[RetrievedChunk] = []
        for chunk in chunks:
            lexical_score = self._lexical_score(query_tokens, self._tokenize(chunk.text))
            boosted_score = lexical_score
            if chunk.chunk_type in {"concept_definition", "concept_bundle", "checkpoint_question", "video_learning_node"}:
                boosted_score += 0.08
            if chunk.chunk_type in {"edge_case", "workflow_step"}:
                boosted_score += 0.04
            scored.append(RetrievedChunk(chunk=chunk, score=boosted_score))
        scored.sort(key=lambda item: item.score, reverse=True)
        return [item for item in scored[:limit] if item.score > 0.0]

    def retrieve_relevant_chunks(self, query: str, limit: int = 6) -> list[ContentChunk]:
        return [item.chunk for item in self.retrieve_relevant_chunks_with_scores(query, limit)]

    def _chunk_video_segment(
        self,
        source_file: SourceFile,
        segment: TranscriptSegment,
        previous: TranscriptSegment | None,
    ) -> list[tuple[str, str]]:
        items: list[tuple[str, str]] = []
        for chunk_type, chunk_text in self._build_concept_bundle_chunks(segment.text):
            items.append((chunk_type, chunk_text))

        learning_node = self._build_video_learning_node(source_file, segment, previous)
        items.append(("video_learning_node", json.dumps(learning_node, ensure_ascii=True)))
        items.append(("checkpoint_question", learning_node["checkpoint_question"]))
        return items

    def _build_video_learning_node(
        self,
        source_file: SourceFile,
        segment: TranscriptSegment,
        previous: TranscriptSegment | None,
    ) -> dict[str, str]:
        current_tokens = self._tokenize(segment.text)
        previous_tokens = self._tokenize(previous.text) if previous else set()
        novel = sorted(current_tokens - previous_tokens)

        if novel:
            change_focus = ", ".join(novel[:8])
            what_changed = f"New focus emerged around: {change_focus}."
        else:
            what_changed = "This segment reinforces the previous execution pattern without major topic drift."

        why_important = (
            f"This segment is a day-level learning anchor ({source_file.recording_day or 'Unknown'}), "
            "and misunderstanding it will cascade into downstream workflow mistakes."
        )

        if segment.importance >= 4:
            what_breaks = "If misunderstood, mapping outputs and process triggers can fail under real data flow."
        else:
            what_breaks = "If misunderstood, handoff quality drops and troubleshooting time increases."

        checkpoint = (
            f"In {source_file.path}, {int(segment.start_sec)}-{int(segment.end_sec)}s: "
            "what changed, why does it matter, and what breaks if you misapply it?"
        )
        return {
            "what_changed": what_changed,
            "why_important": why_important,
            "what_breaks_if_misunderstood": what_breaks,
            "checkpoint_question": checkpoint,
            "source": f"{source_file.path}@{int(segment.start_sec)}-{int(segment.end_sec)}s",
        }

    def _build_concept_bundle_chunks(self, text: str) -> list[tuple[str, str]]:
        semantic_chunks = list(self._split_semantic(text))
        output: list[tuple[str, str]] = []

        for chunk in semantic_chunks:
            role_buckets = {
                "concept_definition": [],
                "concept_example": [],
                "edge_case": [],
                "workflow_step": [],
            }
            sentences = re.split(r"(?<=[.!?])\s+", chunk)
            for sentence in sentences:
                candidate = sentence.strip()
                if not candidate:
                    continue
                role = self._classify_sentence_role(candidate)
                role_buckets[role].append(candidate)

            any_role_written = False
            for role, lines in role_buckets.items():
                if not lines:
                    continue
                role_text = " ".join(lines)
                output.append((role, role_text))
                any_role_written = True

            if not any_role_written:
                output.append(("document", chunk))

            bundle = {
                "explanation": " ".join(role_buckets["concept_definition"]) or chunk,
                "example": " ".join(role_buckets["concept_example"]) or "",
                "mistake": " ".join(role_buckets["edge_case"]) or "Missing edge-case handling.",
            }
            output.append(("concept_bundle", json.dumps(bundle, ensure_ascii=True)))

        return output

    @staticmethod
    def _classify_sentence_role(sentence: str) -> str:
        lower = sentence.lower()
        if any(marker in lower for marker in ["for example", "for instance", "e.g.", "sample"]):
            return "concept_example"
        if any(marker in lower for marker in ["if ", "unless", "edge case", "failure", "error", "break"]):
            return "edge_case"
        if re.match(r"^(step\s*\d+|first|then|next|finally)\b", lower):
            return "workflow_step"
        if any(marker in lower for marker in [" is ", " means ", " defined as ", " refers to "]):
            return "concept_definition"
        return "workflow_step"

    @staticmethod
    def _split_semantic(text: str) -> Iterable[str]:
        normalized = re.sub(r"\s+", " ", text).strip()
        if not normalized:
            return []

        sentences = re.split(r"(?<=[.!?])\s+", normalized)
        chunks: list[str] = []
        current = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            candidate = f"{current} {sentence}".strip()
            if len(candidate) <= settings.max_chunk_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                if len(sentence) <= settings.max_chunk_chars:
                    current = sentence
                else:
                    chunks.extend(ChunkingService._hard_split(sentence, settings.max_chunk_chars))
                    current = ""

        if current:
            chunks.append(current)

        if settings.chunk_overlap_chars <= 0:
            return chunks

        overlapped: list[str] = []
        for index, chunk in enumerate(chunks):
            if index == 0:
                overlapped.append(chunk)
                continue
            tail = chunks[index - 1][-settings.chunk_overlap_chars :]
            overlapped.append(f"{tail} {chunk}".strip())
        return overlapped

    @staticmethod
    def _hard_split(text: str, size: int) -> list[str]:
        return [text[index : index + size] for index in range(0, len(text), size)]

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))

    @staticmethod
    def _lexical_score(query_tokens: set[str], chunk_tokens: set[str]) -> float:
        if not query_tokens or not chunk_tokens:
            return 0.0
        overlap = len(query_tokens & chunk_tokens)
        return overlap / len(query_tokens)
