from __future__ import annotations

import asyncio
from pathlib import Path

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.db import Concept, ConceptEdge, SourceFile
from app.services.chunking_service import ChunkingService
from app.services.document_parser import DocumentParserService
from app.services.ingestion_service import IngestionService
from app.services.knowledge_graph_service import KnowledgeGraphService
from app.services.learning_service import LearningService
from app.services.ollama_router import OllamaRouter
from app.services.quiz_service import QuizService
from app.services.transcription_service import TranscriptionService, to_db_segment


class PipelineService:
    def __init__(self) -> None:
        self.router = OllamaRouter()
        self.transcription = TranscriptionService()

    def run(self, job_id: str, zip_path: str) -> None:
        with SessionLocal() as db:
            ingestion = IngestionService(db)
            parser = DocumentParserService(db)
            chunking = ChunkingService(db, self.router)
            graph = KnowledgeGraphService(db, self.router)
            quiz = QuizService(db, self.router)
            learning = LearningService(db)

            try:
                ingestion.update_job(job_id, status="running", stage="extracting", message="Extracting ZIP")
                root = ingestion.extract_zip(Path(zip_path), job_id)

                ingestion.update_job(job_id, stage="indexing", message="Indexing files")
                indexed_count = ingestion.index_files(job_id, root)

                files = ingestion.files_for_job(job_id)

                ingestion.update_job(job_id, stage="transcription", message="Processing videos")
                for source_file in files:
                    absolute = root / source_file.path
                    if not source_file.is_video:
                        continue
                    segments = self.transcription.transcribe_video(source_file, absolute, job_id)
                    for segment in segments:
                        db.add(to_db_segment(source_file.id, segment))
                db.commit()

                ingestion.update_job(job_id, stage="parsing", message="Parsing documents and mappings")
                for source_file in files:
                    if source_file.is_video:
                        continue
                    absolute = root / source_file.path
                    full_text = parser.parse_file(source_file, absolute)
                    if full_text.strip():
                        parser.persist(source_file, full_text)

                ingestion.update_job(job_id, stage="chunking", message="Building semantic chunks")
                chunk_count = chunking.chunk_all(job_id)

                ingestion.update_job(job_id, stage="embedding", message="Embedding chunks")
                embedded_count = asyncio.run(chunking.embed_chunks(job_id))

                ingestion.update_job(job_id, stage="knowledge_graph", message="Building concept graph")
                concept_count, edge_count = asyncio.run(graph.build_graph())

                ingestion.update_job(job_id, stage="quiz", message="Generating quiz bank")
                quiz_count = asyncio.run(quiz.ensure_questions())

                learning.ensure_profiles(user_id="local-user")

                summary = (
                    f"Indexed {indexed_count} files, {chunk_count} chunks, {embedded_count} embeddings, "
                    f"{concept_count} concepts, {edge_count} edges, {quiz_count} quiz items."
                )
                ingestion.update_job(job_id, status="completed", stage="completed", message=summary)
            except Exception as exc:
                ingestion.update_job(job_id, status="failed", stage="failed", message=str(exc))

    @staticmethod
    def timeline(db, job_id: str) -> dict[str, list[dict[str, object]]]:
        files = list(
            db.scalars(
                select(SourceFile).where(SourceFile.job_id == job_id, SourceFile.is_video.is_(True)).order_by(SourceFile.path.asc())
            ).all()
        )
        grouped: dict[str, list[dict[str, object]]] = {"Day1": [], "Day2": [], "Day3": [], "Day4": [], "Unknown": []}
        for item in files:
            bucket = item.recording_day if item.recording_day else "Unknown"
            grouped.setdefault(bucket, [])
            grouped[bucket].append(
                {
                    "source_file_id": item.id,
                    "path": item.path,
                    "folder": item.folder,
                    "size_bytes": item.size_bytes,
                }
            )
        return grouped

    @staticmethod
    def course_map(db) -> dict[str, list[dict[str, str]]]:
        concepts = list(db.scalars(select(Concept)).all())
        concept_edges = list(db.scalars(select(ConceptEdge)).all())
        nodes = [
            {
                "id": concept.id,
                "name": concept.name,
                "source_reference": concept.source_reference,
            }
            for concept in concepts
        ]
        edges: list[dict[str, str]] = [
            {
                "source_id": edge.source_concept_id,
                "target_id": edge.target_concept_id,
                "type": edge.edge_type,
            }
            for edge in concept_edges
        ]
        return {"nodes": nodes, "edges": edges}
