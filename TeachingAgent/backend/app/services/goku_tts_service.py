"""
Goku TTS Service - Voice cloning using Coqui TTS with GokuClips.mp3
Generates energetic, encouraging audio for teaching sessions
"""
import asyncio
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from app.core.settings import settings


class GokuTTSService:
    """
    Text-to-Speech service with Goku voice cloning.
    Uses Coqui TTS XTTS model with voice sample from GokuClips.mp3
    """

    def __init__(self):
        self.voice_sample_path = settings.goku_voice_sample
        self.cache_dir = settings.data_root / "tts"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.model = None  # Lazy load
        self._cache_cleanup_task: Optional[asyncio.Task] = None

    def _ensure_model_loaded(self):
        """Lazy load TTS model only when needed"""
        if self.model is not None:
            return

        try:
            from TTS.api import TTS
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        except ImportError:
            raise RuntimeError(
                "Coqui TTS not installed. Run: pip install TTS"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load TTS model: {e}")

    async def speak(
        self,
        text: str,
        speed: float = 1.0,
        cache: bool = True,
    ) -> str:
        """
        Generate speech audio for text using Goku's voice.
        
        Args:
            text: Text to synthesize
            speed: Speech speed multiplier (0.8-1.3 recommended)
            cache: Whether to cache the result
        
        Returns:
            Path to generated audio file (.wav)
        """
        # Check cache first
        if cache:
            cached_path = self._get_cached_audio(text)
            if cached_path and cached_path.exists():
                return str(cached_path)

        # Ensure model is loaded
        self._ensure_model_loaded()

        # Verify voice sample exists
        if not self.voice_sample_path.exists():
            raise FileNotFoundError(
                f"Goku voice sample not found: {self.voice_sample_path}\n"
                f"Please ensure GokuClips.mp3 is at the specified location."
            )

        # Generate output path
        output_path = self._generate_output_path(text)

        # Run TTS in thread pool (blocking operation)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._synthesize_blocking,
            text,
            output_path,
            speed,
        )

        # Start cache cleanup if not running
        if self._cache_cleanup_task is None or self._cache_cleanup_task.done():
            self._cache_cleanup_task = asyncio.create_task(self._cleanup_old_cache())

        return str(output_path)

    def _synthesize_blocking(
        self,
        text: str,
        output_path: Path,
        speed: float,
    ) -> None:
        """
        Blocking TTS synthesis (runs in thread pool).
        """
        if self.model is None:
            raise RuntimeError("TTS model not loaded")
        
        try:
            self.model.tts_to_file(
                text=text,
                speaker_wav=str(self.voice_sample_path),
                language="en",
                file_path=str(output_path),
                speed=speed,
            )
        except Exception as e:
            raise RuntimeError(f"TTS synthesis failed: {e}")

    def _get_cached_audio(self, text: str) -> Optional[Path]:
        """Check if audio for this text is already cached"""
        cache_key = self._text_hash(text)
        cached_file = self.cache_dir / f"{cache_key}.wav"
        
        if cached_file.exists():
            # Check if cache is still valid (within TTL)
            age_hours = (datetime.now() - datetime.fromtimestamp(cached_file.stat().st_mtime)).total_seconds() / 3600
            if age_hours < settings.tts_cache_hours:
                return cached_file
        
        return None

    def _generate_output_path(self, text: str) -> Path:
        """Generate output path for audio file"""
        cache_key = self._text_hash(text)
        return self.cache_dir / f"{cache_key}.wav"

    @staticmethod
    def _text_hash(text: str) -> str:
        """Generate hash for text (for caching)"""
        return hashlib.md5(text.encode()).hexdigest()

    async def _cleanup_old_cache(self) -> None:
        """Remove cached audio files older than TTL"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=settings.tts_cache_hours)
            
            for audio_file in self.cache_dir.glob("*.wav"):
                try:
                    file_time = datetime.fromtimestamp(audio_file.stat().st_mtime)
                    if file_time < cutoff_time:
                        audio_file.unlink()
                except Exception:
                    continue  # Skip files we can't delete
        
        except Exception:
            pass  # Cleanup is best-effort

    async def speak_sections(
        self,
        sections: dict[str, str],
        speed: float = 1.0,
    ) -> dict[str, str]:
        """
        Generate audio for multiple teaching sections.
        Returns mapping of section_name -> audio_path
        
        Args:
            sections: Dict of section_name -> text
            speed: Speech speed multiplier
        
        Returns:
            Dict of section_name -> audio_file_path
        """
        audio_paths = {}
        
        for section_name, text in sections.items():
            if not text or not text.strip():
                continue
            
            try:
                audio_path = await self.speak(text, speed=speed, cache=True)
                audio_paths[section_name] = audio_path
            except Exception as e:
                print(f"Failed to generate audio for {section_name}: {e}")
                continue
        
        return audio_paths

    async def pre_generate_next_section(
        self,
        text: str,
        speed: float = 1.0,
    ) -> None:
        """
        Pre-generate audio for next section while user reads current one.
        Fire-and-forget - errors are silently ignored.
        """
        try:
            await self.speak(text, speed=speed, cache=True)
        except Exception:
            pass  # Pre-generation is best-effort

    def get_audio_url(self, audio_path: str) -> str:
        """
        Convert local audio path to API URL for frontend.
        
        Args:
            audio_path: Local file path
        
        Returns:
            API URL path
        """
        path = Path(audio_path)
        if path.parent.name != "tts":
            return ""
        
        return f"/api/audio/{path.name}"

    async def speak_with_emphasis(
        self,
        text: str,
        emphasis_words: list[str],
        speed: float = 1.0,
    ) -> str:
        """
        Generate speech with emphasis on specific words.
        
        Args:
            text: Text to synthesize
            emphasis_words: Words to emphasize
            speed: Speech speed
        
        Returns:
            Path to audio file
        """
        # Add SSML-style emphasis markers
        emphasized_text = text
        for word in emphasis_words:
            # Simple emphasis: repeat slightly or add pause
            emphasized_text = emphasized_text.replace(
                word,
                f"{word}... {word}"  # Repeat for emphasis
            )
        
        return await self.speak(emphasized_text, speed=speed, cache=True)

    def add_pacing_pauses(self, text: str) -> str:
        """
        Add natural pauses to text for better speech pacing.
        
        Args:
            text: Original text
        
        Returns:
            Text with pause markers
        """
        # Add pauses after questions and key points
        paced = text.strip()
        paced = paced.replace("?", "? ... ")
        paced = paced.replace(":", ": ... ")
        paced = paced.replace("!", "! ... ")
        
        return paced

# Made with Bob
