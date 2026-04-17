from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

from app.core.settings import settings


class VoiceProfileService:
    def __init__(self) -> None:
        self.base_dir = settings.data_root / "voice_profiles"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_profile_from_clip(self, profile_name: str, clip_path: Path) -> dict[str, object]:
        safe_name = self._sanitize_profile_name(profile_name)
        profile_dir = self.base_dir / safe_name
        profile_dir.mkdir(parents=True, exist_ok=True)

        self._reset_profile_samples(profile_dir)

        normalized = profile_dir / "normalized.wav"
        self._normalize_audio(clip_path, normalized)

        self._split_samples(normalized, profile_dir)
        samples = self._collect_samples(profile_dir)

        if not samples:
            raise RuntimeError("No usable voice samples were generated from the clip.")

        manifest = {
            "profile_name": safe_name,
            "created_at": datetime.utcnow().isoformat(),
            "source_clip": clip_path.name,
            "sample_count": len(samples),
            "samples": [sample.name for sample in samples],
        }
        (profile_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest

    def list_profiles(self) -> list[dict[str, object]]:
        profiles: list[dict[str, object]] = []
        for path in sorted(self.base_dir.iterdir()):
            if not path.is_dir():
                continue
            manifest_path = path / "manifest.json"
            if manifest_path.exists():
                profiles.append(json.loads(manifest_path.read_text(encoding="utf-8")))
                continue

            samples = self._collect_samples(path)
            if samples:
                profiles.append(
                    {
                        "profile_name": path.name,
                        "created_at": "",
                        "source_clip": "",
                        "sample_count": len(samples),
                        "samples": [sample.name for sample in samples],
                    }
                )
        return profiles

    def sample_paths(self, profile_name: str, max_samples: int = 3) -> list[Path]:
        profile_dir = self.base_dir / self._sanitize_profile_name(profile_name)
        if not profile_dir.exists():
            return []
        return self._collect_samples(profile_dir)[:max_samples]

    def _normalize_audio(self, source: Path, destination: Path) -> None:
        args = [
            settings.ffmpeg_bin,
            "-y",
            "-i",
            str(source),
            "-af",
            "highpass=f=120,lowpass=f=7800,loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ac",
            "1",
            "-ar",
            "22050",
            "-c:a",
            "pcm_s16le",
            str(destination),
        ]
        try:
            subprocess.run(args, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise RuntimeError("Unable to normalize voice clip. Ensure ffmpeg is installed.") from exc

    def _split_samples(self, normalized_wav: Path, profile_dir: Path) -> None:
        segment_pattern = profile_dir / "sample_%03d.wav"
        args = [
            settings.ffmpeg_bin,
            "-y",
            "-i",
            str(normalized_wav),
            "-f",
            "segment",
            "-segment_time",
            "6",
            "-c:a",
            "pcm_s16le",
            str(segment_pattern),
        ]
        try:
            subprocess.run(args, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise RuntimeError("Unable to split voice clips into samples.") from exc

    @staticmethod
    def _collect_samples(profile_dir: Path) -> list[Path]:
        samples: list[Path] = []
        for sample in sorted(profile_dir.glob("sample_*.wav")):
            if sample.stat().st_size <= 16_000:
                continue
            duration = VoiceProfileService._duration_seconds(sample)
            if duration < 1.2 or duration > 12.0:
                continue
            samples.append(sample)
        return samples

    @staticmethod
    def _duration_seconds(path: Path) -> float:
        args = [
            settings.ffprobe_bin,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
        try:
            result = subprocess.run(args, check=True, capture_output=True, text=True)
            return float(result.stdout.strip() or 0.0)
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
            return 0.0

    @staticmethod
    def _reset_profile_samples(profile_dir: Path) -> None:
        for pattern in ("sample_*.wav", "normalized.wav"):
            for path in profile_dir.glob(pattern):
                path.unlink(missing_ok=True)

    @staticmethod
    def _sanitize_profile_name(name: str) -> str:
        lowered = name.strip().lower()
        sanitized = re.sub(r"[^a-z0-9_-]+", "-", lowered).strip("-")
        return sanitized or "voice-profile"
