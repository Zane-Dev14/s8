from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.db import IngestionJob, SourceFile
from app.services.file_classifier import classify_file, detect_recording_day


class IngestionService:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, zip_name: str) -> IngestionJob:
        job = IngestionJob(zip_name=zip_name, status="queued", stage="queued")
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job(self, job_id: str) -> IngestionJob | None:
        return self.db.get(IngestionJob, job_id)

    def update_job(self, job_id: str, *, status: str | None = None, stage: str | None = None, message: str | None = None) -> None:
        job = self.db.get(IngestionJob, job_id)
        if not job:
            return
        if status is not None:
            job.status = status
        if stage is not None:
            job.stage = stage
        if message is not None:
            job.message = message
        self.db.add(job)
        self.db.commit()

    def extract_zip(self, zip_path: Path, job_id: str) -> Path:
        destination = settings.data_root / "ingested" / job_id
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as archive:
            for member in archive.infolist():
                member_path = Path(member.filename)
                if member_path.is_absolute() or ".." in member_path.parts:
                    continue
                target_path = destination / member_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if member.is_dir():
                    continue
                with archive.open(member) as source_file, open(target_path, "wb") as target_file:
                    shutil.copyfileobj(source_file, target_file)

        return destination

    def index_files(self, job_id: str, root: Path) -> int:
        inserted = 0
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue

            file_type, is_video = classify_file(file_path)
            if file_type == "ignored":
                continue

            relative = file_path.relative_to(root)
            source_file = SourceFile(
                job_id=job_id,
                path=str(relative),
                folder=str(relative.parent),
                extension=file_path.suffix.lower(),
                file_type=file_type,
                is_video=is_video,
                recording_day=detect_recording_day(relative),
                size_bytes=file_path.stat().st_size,
            )
            self.db.add(source_file)
            inserted += 1

        self.db.commit()
        return inserted

    def files_for_job(self, job_id: str) -> list[SourceFile]:
        statement = select(SourceFile).where(SourceFile.job_id == job_id)
        return list(self.db.scalars(statement).all())

    def files_count(self, job_id: str) -> int:
        statement = select(func.count()).select_from(SourceFile).where(SourceFile.job_id == job_id)
        return int(self.db.scalar(statement) or 0)
