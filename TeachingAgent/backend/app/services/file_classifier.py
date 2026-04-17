from __future__ import annotations

from pathlib import Path

VIDEO_EXTENSIONS = {".mp4"}
WORKFLOW_EXTENSIONS = {".bpml", ".xml"}
MAPPING_EXTENSIONS = {".ddf", ".mxl", ".txo"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx"}
VISUAL_EXTENSIONS = {".png", ".jpg", ".jpeg"}
IGNORED_EXTENSIONS = {".exe"}


def classify_file(path: Path) -> tuple[str, bool]:
    ext = path.suffix.lower()

    if ext in IGNORED_EXTENSIONS:
        return "ignored", False
    if ext in VIDEO_EXTENSIONS:
        return "video", True
    if ext in WORKFLOW_EXTENSIONS:
        return "workflow", False
    if ext in MAPPING_EXTENSIONS:
        return "mapping", False
    if ext in DOCUMENT_EXTENSIONS:
        return "document", False
    if ext in VISUAL_EXTENSIONS:
        return "visual", False

    return "other", False


def detect_recording_day(path: Path) -> str:
    parts = [part.lower() for part in path.parts]
    for day in ("day1", "day2", "day3", "day4"):
        if day in parts:
            return day.capitalize()
    return ""
