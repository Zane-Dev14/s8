from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Teaching Agent Backend"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    workspace_root: Path = Path(__file__).resolve().parents[3]
    data_root: Path = Field(default=Path(__file__).resolve().parents[2] / "data")
    db_path: Path = Field(default=Path(__file__).resolve().parents[2] / "data" / "learning.db")

    # Ollama Configuration
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_num_parallel: int = 2
    ollama_keep_alive: str = "10m"

    # Model Selection - Fast and Efficient
    model_fast: str = "openchat:latest"  # Fast teaching, flashcards, UI
    model_eval: str = "llama3.1:8b-instruct-q8_0"  # Answer eval, concept extraction
    model_embed: str = "nomic-embed-text"  # Embeddings only

    # Legacy model fields for backward compatibility (will be removed)
    model_parser: str = "llama3.1:8b-instruct-q8_0"
    model_chunker: str = "openchat:latest"
    model_graph: str = "llama3.1:8b-instruct-q8_0"
    model_teacher: str = "openchat:latest"
    model_teacher_fallback: str = "llama3.1:8b-instruct-q8_0"
    model_quiz: str = "llama3.1:8b-instruct-q8_0"
    model_fast_ui: str = "openchat:latest"
    model_coding: str = "llama3.1:8b-instruct-q8_0"

    # Whisper for video/audio transcription
    whisper_bin: str = "whisper"
    whisper_model: str = "base"

    # FFmpeg for media processing
    ffmpeg_bin: str = "/opt/homebrew/bin/ffmpeg"
    ffprobe_bin: str = "/opt/homebrew/bin/ffprobe"

    # TTS Configuration - Goku Voice
    tts_engine: str = "xtts"  # Use XTTS for voice cloning
    xtts_bin: str = "tts"
    xtts_model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    goku_voice_sample: Path = Field(
        default=Path("/Users/eric/IBM/Projects/SDE/Teaching Agent/Bootcamp/GokuClips.mp3")
    )
    default_voice_profile: str = "goku"
    
    # Fallback TTS
    piper_bin: str = "piper"
    piper_model_path: str = ""

    # Chunking Configuration
    max_chunk_tokens: int = 512  # Semantic chunking target
    chunk_overlap_tokens: int = 64  # Overlap for context preservation

    # Cache Configuration
    cache_ttl_seconds: int = 1800  # 30 minutes
    tts_cache_hours: int = 2  # Delete TTS audio after 2 hours


settings = Settings()


def ensure_data_dirs() -> None:
    """Create all required data directories"""
    paths = [
        settings.data_root,
        settings.data_root / "cache",
        settings.data_root / "ingested",
        settings.data_root / "transcripts",
        settings.data_root / "keyframes",
        settings.data_root / "tts",
        settings.data_root / "voice_profiles",
        settings.data_root / "voice_profiles" / "goku",
        settings.data_root / "subjects",  # Per-subject data
        settings.data_root / "embeddings",  # ChromaDB persistence
    ]
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

# Made with Bob
