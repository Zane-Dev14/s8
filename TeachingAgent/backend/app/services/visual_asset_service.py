from __future__ import annotations

import re
from pathlib import Path

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.db import IngestionJob, SourceFile


class VisualAssetService:
    def __init__(self, db: Session):
        self.db = db

    def find_diagrams_for_concept(self, concept_name: str, limit: int = 3) -> list[dict[str, str]]:
        job_id = self._latest_completed_job_id()
        if not job_id:
            return []

        visuals = list(
            self.db.scalars(
                select(SourceFile)
                .where(SourceFile.job_id == job_id, SourceFile.file_type == "visual")
                .order_by(SourceFile.path.asc())
            ).all()
        )
        if not visuals:
            return []

        query_tokens = self._tokenize(concept_name)
        scored: list[tuple[float, SourceFile]] = []
        for visual in visuals:
            file_tokens = self._tokenize(visual.path)
            overlap = len(query_tokens & file_tokens)
            score = overlap / max(len(query_tokens), 1)
            if any(word in visual.path.lower() for word in ["architecture", "flow", "diagram", "sftp", "ssh"]):
                score += 0.15
            scored.append((score, visual))

        scored.sort(key=lambda item: item[0], reverse=True)

        # Fall back to the first few visuals when token overlap is too weak.
        picks = [item[1] for item in scored if item[0] > 0.0][:limit]
        if not picks:
            picks = [item[1] for item in scored[:limit]]

        return [
            {
                "title": self._title_from_path(file.path),
                "description": f"Visual reference from {file.folder}",
                "image_url": f"/api/assets/visual/{job_id}/{file.id}",
                "source_path": file.path,
            }
            for file in picks
        ]

    def _latest_completed_job_id(self) -> str | None:
        return self.db.scalar(
            select(IngestionJob.id)
            .where(IngestionJob.status == "completed")
            .order_by(desc(IngestionJob.updated_at))
            .limit(1)
        )

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))

    @staticmethod
    def _title_from_path(path: str) -> str:
        stem = Path(path).stem.replace("_", " ").replace("-", " ").strip()
        return stem.title() if stem else "Diagram"
