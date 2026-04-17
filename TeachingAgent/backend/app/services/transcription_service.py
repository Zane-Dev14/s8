from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from app.core.settings import settings
from app.models.db import SourceFile, TranscriptSegment


@dataclass
class SegmentData:
    start_sec: float
    end_sec: float
    text: str
    topic: str
    importance: int
    keyframe_path: str


class TranscriptionService:
    def __init__(self) -> None:
        self.ffmpeg_bin = settings.ffmpeg_bin
        self.ffprobe_bin = settings.ffprobe_bin
        self.whisper_bin = settings.whisper_bin

    def transcribe_video(self, source_file: SourceFile, absolute_path: Path, job_id: str) -> list[SegmentData]:
        transcript_dir = settings.data_root / "transcripts" / job_id
        transcript_dir.mkdir(parents=True, exist_ok=True)
        output_prefix = transcript_dir / f"{Path(source_file.path).stem}_{source_file.id}"

        args = [self.whisper_bin]
        if settings.whisper_model_path:
            args.extend(["-m", settings.whisper_model_path])
        args.extend(["-f", str(absolute_path), "-oj", "-of", str(output_prefix)])

        try:
            subprocess.run(args, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return self._fallback_segments(source_file, absolute_path, job_id)

        transcript_json = output_prefix.with_suffix(".json")
        if not transcript_json.exists():
            return self._fallback_segments(source_file, absolute_path, job_id)

        data = json.loads(transcript_json.read_text(encoding="utf-8"))
        segments = data.get("transcription", [])
        if not isinstance(segments, list) or not segments:
            return self._fallback_segments(source_file, absolute_path, job_id)

        normalized: list[SegmentData] = []
        previous_text = ""
        for segment in segments:
            start = float(segment.get("offsets", {}).get("from", 0)) / 1000.0
            end = float(segment.get("offsets", {}).get("to", 0)) / 1000.0
            text = str(segment.get("text", "")).strip()
            topic = self._infer_topic(text)
            importance = self._importance_from_shift(previous_text, text)
            keyframe_path = self.extract_keyframe(absolute_path, job_id, source_file.id, start)
            normalized.append(
                SegmentData(
                    start_sec=start,
                    end_sec=end,
                    text=text,
                    topic=topic,
                    importance=importance,
                    keyframe_path=keyframe_path,
                )
            )
            previous_text = text
        return normalized

    def extract_keyframe(self, video_path: Path, job_id: str, source_file_id: str, second: float) -> str:
        frame_dir = settings.data_root / "keyframes" / job_id / source_file_id
        frame_dir.mkdir(parents=True, exist_ok=True)
        frame_path = frame_dir / f"{int(second):06d}.jpg"
        args = [
            self.ffmpeg_bin,
            "-y",
            "-ss",
            f"{second:.3f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            str(frame_path),
        ]
        try:
            subprocess.run(args, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""
        return str(frame_path)

    def _fallback_segments(self, source_file: SourceFile, absolute_path: Path, job_id: str) -> list[SegmentData]:
        duration = self._probe_duration(absolute_path)
        if duration <= 0:
            duration = 60.0

        step = 45.0
        segments: list[SegmentData] = []
        cursor = 0.0
        while cursor < duration:
            end = min(cursor + step, duration)
            keyframe_path = self.extract_keyframe(absolute_path, job_id, source_file.id, cursor)
            text = f"Raw segment {int(cursor)}-{int(end)} seconds. Whisper transcription unavailable."
            segments.append(
                SegmentData(
                    start_sec=cursor,
                    end_sec=end,
                    text=text,
                    topic="Unlabeled Segment",
                    importance=2,
                    keyframe_path=keyframe_path,
                )
            )
            cursor = end
        return segments

    def _probe_duration(self, path: Path) -> float:
        args = [
            self.ffprobe_bin,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
        try:
            out = subprocess.check_output(args, stderr=subprocess.STDOUT).decode("utf-8").strip()
            return float(out)
        except Exception:
            return 0.0

    @staticmethod
    def _infer_topic(text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return "Unlabeled Topic"
        words = stripped.split()
        return " ".join(words[:8])

    @staticmethod
    def _importance_from_shift(previous: str, current: str) -> int:
        prev_tokens = set(previous.lower().split())
        cur_tokens = set(current.lower().split())
        if not prev_tokens or not cur_tokens:
            return 3
        overlap = len(prev_tokens & cur_tokens)
        union = len(prev_tokens | cur_tokens)
        similarity = overlap / max(union, 1)
        if similarity < 0.1:
            return 5
        if similarity < 0.25:
            return 4
        if similarity < 0.45:
            return 3
        return 2


def to_db_segment(source_file_id: str, segment: SegmentData) -> TranscriptSegment:
    return TranscriptSegment(
        source_file_id=source_file_id,
        start_sec=segment.start_sec,
        end_sec=segment.end_sec,
        text=segment.text,
        topic=segment.topic,
        importance=segment.importance,
        keyframe_path=segment.keyframe_path,
    )
