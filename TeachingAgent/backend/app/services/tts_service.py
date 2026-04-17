from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from shutil import which

from app.core.settings import settings


class TTSService:
    def synthesize(
        self,
        text: str,
        speed: float,
        tone: str,
        emphasis_words: list[str] | None = None,
        voice_profile: str | None = None,
    ) -> str:
        emphasis_words = emphasis_words or []
        processed = self._apply_pacing_and_emphasis(text, tone)
        for word in emphasis_words:
            processed = processed.replace(word, f"<{word}>")

        tuned_speed = speed
        if tone == "teaching":
            tuned_speed = min(max(speed, 1.15), 1.25)
        if tone == "challenge":
            tuned_speed = min(max(speed, 1.20), 1.30)

        output_dir = settings.data_root / "tts"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"tts_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.wav"

        # Try requested voice profile first, then degrade to standard engines so users still get audio.
        if voice_profile:
            generated = self._synthesize_xtts(processed, output_path, voice_profile)
            if generated:
                return generated

        if settings.tts_engine.lower() == "xtts" and voice_profile:
            generated = self._synthesize_xtts(processed, output_path, voice_profile)
            if generated:
                return generated

        if settings.tts_engine.lower() == "piper" and settings.piper_model_path:
            args = [
                settings.piper_bin,
                "--model",
                settings.piper_model_path,
                "--output_file",
                str(output_path),
                "--length_scale",
                f"{1.0 / max(tuned_speed, 0.1):.4f}",
            ]
            try:
                subprocess.run(args, input=processed.encode("utf-8"), check=True, capture_output=True, timeout=20)
                return str(output_path)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass

        macos_fallback = self._synthesize_macos_say(processed, output_path)
        if macos_fallback:
            return macos_fallback

        fallback = output_dir / f"tts_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.txt"
        fallback.write_text(processed, encoding="utf-8")
        return str(fallback)

    @staticmethod
    def _synthesize_macos_say(text: str, output_path: Path) -> str | None:
        if sys.platform != "darwin":
            return None

        aiff_path = output_path.with_suffix(".aiff")
        say_bin = which("say")
        if not say_bin:
            return None

        try:
            subprocess.run([say_bin, "-o", str(aiff_path), text], check=True, capture_output=True)
            # Use settings.ffmpeg_bin which has the full path
            ffmpeg_bin = which("ffmpeg") or settings.ffmpeg_bin
            subprocess.run(
                [ffmpeg_bin, "-y", "-i", str(aiff_path), str(output_path)],
                check=True,
                capture_output=True,
            )
            aiff_path.unlink(missing_ok=True)
            return str(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"TTS macOS say error: {e}")  # Debug logging
            aiff_path.unlink(missing_ok=True)
            return None

    def _synthesize_xtts(self, text: str, output_path: Path, voice_profile: str | None) -> str | None:
        if not voice_profile:
            print("XTTS: No voice profile specified")
            return None

        from app.services.voice_profile_service import VoiceProfileService

        profile_service = VoiceProfileService()
        sample_paths = profile_service.sample_paths(voice_profile)
        if not sample_paths:
            print(f"XTTS: No sample paths found for profile '{voice_profile}'")
            return None

        print(f"XTTS: Found {len(sample_paths)} samples for '{voice_profile}'")
        xtts_bin = self._resolve_executable(settings.xtts_bin)
        print(f"XTTS: Using binary: {xtts_bin}")

        args = [
            xtts_bin,
            "--model_name",
            settings.xtts_model_name,
            "--text",
            text,
            "--language_idx",
            "en",
            "--out_path",
            str(output_path),
            "--speaker_wav",
            *[str(path) for path in sample_paths],
        ]
        env = dict(os.environ)
        env.setdefault("COQUI_TOS_AGREED", "1")
        env.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
        try:
            print(f"XTTS: Running command: {' '.join(args[:5])}...")
            result = subprocess.run(args, check=True, capture_output=True, env=env, timeout=60)
            print(f"XTTS: Success! Generated {output_path}")
            return str(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"XTTS: Failed with error: {type(e).__name__}: {e}")
            if isinstance(e, subprocess.CalledProcessError):
                print(f"XTTS stderr: {e.stderr.decode() if e.stderr else 'none'}")
            return None

    @staticmethod
    def _resolve_executable(configured: str) -> str:
        if Path(configured).exists():
            return configured

        resolved = which(configured)
        if resolved:
            return resolved

        venv_candidate = Path(sys.executable).parent / configured
        if venv_candidate.exists():
            return str(venv_candidate)

        return configured

    @staticmethod
    def to_public_url(audio_path: str) -> str:
        path = Path(audio_path)
        if path.parent.name != "tts":
            return ""
        if path.suffix.lower() not in {".wav", ".mp3", ".ogg"}:
            return ""
        return f"/api/assets/tts/{path.name}"

    @staticmethod
    def _apply_pacing_and_emphasis(text: str, tone: str) -> str:
        # Add deliberate pauses around questions and key points for stronger retention.
        processed = text.strip()
        processed = processed.replace("?", "? ... ")
        processed = processed.replace(":", ": ... ")
        processed = processed.replace("[EMPHASIS]", "")
        processed = processed.replace("[/EMPHASIS]", "")

        if tone == "challenge":
            processed = f"Focus. {processed} Answer now."
        else:
            processed = f"Lock this in. {processed}"
        return processed
