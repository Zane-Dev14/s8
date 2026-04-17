"""Regression tests for interactive teaching quality and resilient audio behavior."""
from __future__ import annotations

import pytest

from app.services.interactive_teacher_service import InteractiveTeacherService
from app.services.tts_service import TTSService


class TestInteractiveTeacherQuality:
    def test_normalize_sections_keeps_specific_visuals_and_examples(self):
        service = InteractiveTeacherService()

        normalized = service._normalize_sections(
            concept_name="SFTP",
            concept_explanation="Secure file transfer over SSH.",
            source_chunks=["Day2/SFTPOutbound.bpml: Validate mailbox route before transfer."],
            sections={
                "hook": "Alright, let us lock this down.",
                "visual_description": "Sender mailbox pushes to secure gateway then to receiver inbox.",
                "real_example": "A purchase order file moves from partner mailbox to internal processing.",
                "common_mistake": "Teams skip key validation and transfer fails at handshake.",
            },
        )

        assert "sender mailbox" in normalized["visual_description"].lower()
        assert "purchase order" in normalized["real_example"].lower()
        assert "skip key validation" in normalized["common_mistake"].lower()
        assert normalized["visual_description"] != service.DEFAULT_VISUAL_DESCRIPTION
        assert normalized["real_example"] != service.DEFAULT_REAL_EXAMPLE

    def test_generate_flashcards_includes_non_generic_transfer_checks(self):
        cards = InteractiveTeacherService._generate_flashcards(
            {
                "hook": "SFTP secures movement.",
                "core_concept": "Validate, authenticate, transfer, and verify integrity.",
                "common_mistake": "Skipping identity checks causes transfer rejection.",
            }
        )

        ids = {card["id"] for card in cards}
        assert "common_mistake" in ids
        assert "transfer-path-check" in ids


class TestInteractiveTeacherAudio:
    @pytest.mark.asyncio
    async def test_generate_audio_teaching_builds_specific_subtitle_lines(self, monkeypatch):
        service = InteractiveTeacherService()

        def fake_synthesize(self, text, speed, tone, emphasis_words=None, voice_profile=None):
            assert "Hook." in text
            assert "Core Concept." in text
            return "/tmp/coach.wav"

        monkeypatch.setattr(TTSService, "synthesize", fake_synthesize)

        teaching_content = {
            "sections": {
                "hook": "Alright! Today we secure partner delivery.",
                "core_concept": "First authenticate with SSH keys. Then transfer over encrypted channel.",
                "practice_scenario": "You have one hour to deliver an order file safely.",
            }
        }

        result = await service.generate_audio_teaching(teaching_content, voice_profile="goku")

        assert result["segments"]
        subtitles = " ".join(segment["text"] for segment in result["segments"])
        assert "Core Concept." in subtitles
        assert "authenticate with SSH keys" in subtitles
        assert all(segment["audio_path"].endswith(".wav") for segment in result["segments"])


class TestTTSFallbackBehavior:
    def test_voice_profile_failure_still_returns_audio_when_fallback_available(self, monkeypatch):
        service = TTSService()

        monkeypatch.setattr(TTSService, "_synthesize_xtts", lambda *args, **kwargs: None)
        monkeypatch.setattr(TTSService, "_synthesize_macos_say", lambda *args, **kwargs: "/tmp/fallback.wav")

        result = service.synthesize(
            text="Secure transfer explanation",
            speed=1.2,
            tone="teaching",
            voice_profile="goku",
        )

        assert result.endswith(".wav")
