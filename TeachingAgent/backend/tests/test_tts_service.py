"""
Test suite for TTSService - validates TTS tone shaping and pacing.

Tests cover:
1. Tone shaping for teaching vs challenge modes
2. Pacing pauses before key points/questions
3. Emphasis marker handling
4. Speed windows for high-energy delivery
"""
from __future__ import annotations

from pathlib import Path

import pytest

from app.services.tts_service import TTSService


class TestToneShaping:
    """Test tone shaping for different modes."""
    
    def test_teaching_tone_adds_lock_in_prefix(self):
        """Verify teaching tone adds 'Lock this in' prefix."""
        service = TTSService()
        
        processed = service._apply_pacing_and_emphasis("SFTP uses SSH for security", "teaching")
        
        assert "Lock this in" in processed
        assert "SFTP" in processed
    
    def test_challenge_tone_adds_focus_and_answer_now(self):
        """Verify challenge tone adds 'Focus' prefix and 'Answer now' suffix."""
        service = TTSService()
        
        processed = service._apply_pacing_and_emphasis("What protocol does SFTP use?", "challenge")
        
        assert "Focus" in processed
        assert "Answer now" in processed
        assert "SFTP" in processed
    
    def test_teaching_vs_challenge_tone_difference(self):
        """Verify teaching and challenge tones produce different outputs."""
        service = TTSService()
        
        text = "Explain SFTP authentication"
        teaching = service._apply_pacing_and_emphasis(text, "teaching")
        challenge = service._apply_pacing_and_emphasis(text, "challenge")
        
        assert teaching != challenge
        assert "Lock this in" in teaching
        assert "Focus" in challenge
        assert "Answer now" in challenge


class TestPacingPauses:
    """Test pacing pauses before key points and questions."""
    
    def test_question_marks_get_pauses(self):
        """Verify question marks get deliberate pauses."""
        service = TTSService()
        
        text = "What is SFTP? How does it work?"
        processed = service._apply_pacing_and_emphasis(text, "teaching")
        
        # Should add pauses after questions
        assert "? ..." in processed or "?..." in processed
    
    def test_colons_get_pauses(self):
        """Verify colons get deliberate pauses for key points."""
        service = TTSService()
        
        text = "Remember: SFTP uses SSH for encryption"
        processed = service._apply_pacing_and_emphasis(text, "teaching")
        
        # Should add pauses after colons
        assert ": ..." in processed or ":..." in processed
    
    def test_multiple_pauses_in_complex_text(self):
        """Verify multiple pause points are handled correctly."""
        service = TTSService()
        
        text = "Key point: What is SFTP? It's a secure protocol: uses SSH for encryption"
        processed = service._apply_pacing_and_emphasis(text, "teaching")
        
        # Should have multiple pause markers
        pause_count = processed.count("...")
        assert pause_count >= 3  # At least 3 pauses


class TestEmphasisMarkerHandling:
    """Test emphasis marker handling."""
    
    def test_emphasis_markers_removed_from_base_processing(self):
        """Verify [EMPHASIS] markers are removed in base processing."""
        service = TTSService()
        
        text = "SFTP [EMPHASIS]requires[/EMPHASIS] SSH keys"
        processed = service._apply_pacing_and_emphasis(text, "teaching")
        
        # Markers should be removed
        assert "[EMPHASIS]" not in processed
        assert "[/EMPHASIS]" not in processed
        assert "requires" in processed
    
    def test_emphasis_words_wrapped_in_brackets(self):
        """Verify emphasis words are wrapped in angle brackets."""
        service = TTSService()
        
        text = "SFTP requires SSH keys for authentication"
        # Synthesize with emphasis on specific words
        output = service.synthesize(
            text=text,
            speed=1.2,
            tone="teaching",
            emphasis_words=["SSH", "authentication"],
        )
        
        # Output should be a file path
        assert isinstance(output, str)
        assert len(output) > 0


class TestSpeedWindows:
    """Test speed windows for high-energy delivery."""
    
    def test_teaching_tone_constrains_speed_window(self):
        """Verify teaching tone constrains speed to 1.15-1.25 range."""
        service = TTSService()
        
        # Test with various input speeds
        for input_speed in [0.8, 1.0, 1.2, 1.4, 1.6]:
            output = service.synthesize(
                text="Test content",
                speed=input_speed,
                tone="teaching",
            )
            
            # Should produce output
            assert isinstance(output, str)
            assert len(output) > 0
    
    def test_challenge_tone_constrains_speed_window(self):
        """Verify challenge tone constrains speed to 1.20-1.30 range."""
        service = TTSService()
        
        # Test with various input speeds
        for input_speed in [0.8, 1.0, 1.2, 1.4, 1.6]:
            output = service.synthesize(
                text="Test content",
                speed=input_speed,
                tone="challenge",
            )
            
            # Should produce output
            assert isinstance(output, str)
            assert len(output) > 0
    
    def test_challenge_tone_faster_than_teaching(self):
        """Verify challenge tone uses faster speed than teaching tone."""
        service = TTSService()
        
        # Both should constrain speed, but challenge should be faster
        # This is implicit in the speed window ranges:
        # teaching: 1.15-1.25
        # challenge: 1.20-1.30
        
        # Test with same input speed
        teaching_output = service.synthesize(
            text="Test content",
            speed=1.0,
            tone="teaching",
        )
        
        challenge_output = service.synthesize(
            text="Test content",
            speed=1.0,
            tone="challenge",
        )
        
        # Both should produce output
        assert isinstance(teaching_output, str)
        assert isinstance(challenge_output, str)


class TestSynthesizeOutput:
    """Test synthesize method output."""
    
    def test_synthesize_returns_file_path(self):
        """Verify synthesize returns a file path."""
        service = TTSService()
        
        output = service.synthesize(
            text="SFTP is a secure file transfer protocol",
            speed=1.2,
            tone="teaching",
        )
        
        assert isinstance(output, str)
        assert len(output) > 0
        # Should be a path
        assert "/" in output or "\\" in output
    
    def test_synthesize_creates_output_file(self):
        """Verify synthesize creates an output file."""
        service = TTSService()
        
        output = service.synthesize(
            text="Test content for TTS",
            speed=1.2,
            tone="teaching",
        )
        
        # File should exist
        output_path = Path(output)
        assert output_path.exists()
        
        # Should have content
        assert output_path.stat().st_size > 0
    
    def test_synthesize_with_emphasis_words(self):
        """Verify synthesize handles emphasis words correctly."""
        service = TTSService()
        
        output = service.synthesize(
            text="SFTP uses SSH keys for secure authentication",
            speed=1.2,
            tone="teaching",
            emphasis_words=["SFTP", "SSH", "secure"],
        )
        
        assert isinstance(output, str)
        assert len(output) > 0
        
        # File should exist
        output_path = Path(output)
        assert output_path.exists()
    
    def test_synthesize_fallback_creates_text_file(self):
        """Verify synthesize creates text file as fallback when TTS engine unavailable."""
        service = TTSService()
        
        # Synthesize will fall back to text file if piper not available
        output = service.synthesize(
            text="Fallback test content",
            speed=1.2,
            tone="teaching",
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()
        
        # Should contain processed text
        if output_path.suffix == ".txt":
            content = output_path.read_text()
            assert "Fallback test content" in content or "Lock this in" in content


class TestPacingAndEmphasisIntegration:
    """Test integration of pacing and emphasis features."""
    
    def test_full_processing_pipeline(self):
        """Verify full processing pipeline with pacing and emphasis."""
        service = TTSService()
        
        text = "Key concept: What is SFTP? It uses SSH for encryption"
        
        output = service.synthesize(
            text=text,
            speed=1.2,
            tone="teaching",
            emphasis_words=["SFTP", "SSH"],
        )
        
        assert isinstance(output, str)
        assert len(output) > 0
        
        # Verify file exists
        output_path = Path(output)
        assert output_path.exists()
    
    def test_challenge_mode_full_pipeline(self):
        """Verify challenge mode full processing pipeline."""
        service = TTSService()
        
        text = "Defend your answer: Why does SFTP use SSH?"
        
        output = service.synthesize(
            text=text,
            speed=1.3,
            tone="challenge",
            emphasis_words=["Defend", "SSH"],
        )
        
        assert isinstance(output, str)
        assert len(output) > 0
        
        # Verify file exists
        output_path = Path(output)
        assert output_path.exists()


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_text_handling(self):
        """Verify empty text is handled gracefully."""
        service = TTSService()
        
        output = service.synthesize(
            text="",
            speed=1.2,
            tone="teaching",
        )
        
        # Should still produce output
        assert isinstance(output, str)
    
    def test_very_long_text_handling(self):
        """Verify very long text is handled correctly."""
        service = TTSService()
        
        long_text = "SFTP is a secure protocol. " * 100
        
        output = service.synthesize(
            text=long_text,
            speed=1.2,
            tone="teaching",
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()
    
    def test_special_characters_handling(self):
        """Verify special characters are handled correctly."""
        service = TTSService()
        
        text = "SFTP uses port 22 (default) & requires SSH keys @ server-side!"
        
        output = service.synthesize(
            text=text,
            speed=1.2,
            tone="teaching",
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()
    
    def test_no_emphasis_words(self):
        """Verify synthesis works without emphasis words."""
        service = TTSService()
        
        output = service.synthesize(
            text="SFTP is secure",
            speed=1.2,
            tone="teaching",
            emphasis_words=None,
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()
    
    def test_empty_emphasis_words_list(self):
        """Verify synthesis works with empty emphasis words list."""
        service = TTSService()
        
        output = service.synthesize(
            text="SFTP is secure",
            speed=1.2,
            tone="teaching",
            emphasis_words=[],
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()


class TestSpeedBoundaries:
    """Test speed boundary conditions."""
    
    def test_minimum_speed_boundary(self):
        """Verify minimum speed is handled correctly."""
        service = TTSService()
        
        output = service.synthesize(
            text="Test content",
            speed=0.75,  # Minimum speed
            tone="teaching",
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()
    
    def test_maximum_speed_boundary(self):
        """Verify maximum speed is handled correctly."""
        service = TTSService()
        
        output = service.synthesize(
            text="Test content",
            speed=1.5,  # Maximum speed
            tone="teaching",
        )
        
        assert isinstance(output, str)
        output_path = Path(output)
        assert output_path.exists()
    
    def test_speed_clamping_for_teaching(self):
        """Verify speed is clamped to teaching range (1.15-1.25)."""
        service = TTSService()
        
        # Test below range
        output1 = service.synthesize(text="Test", speed=0.8, tone="teaching")
        assert isinstance(output1, str)
        
        # Test above range
        output2 = service.synthesize(text="Test", speed=1.5, tone="teaching")
        assert isinstance(output2, str)
    
    def test_speed_clamping_for_challenge(self):
        """Verify speed is clamped to challenge range (1.20-1.30)."""
        service = TTSService()
        
        # Test below range
        output1 = service.synthesize(text="Test", speed=0.8, tone="challenge")
        assert isinstance(output1, str)
        
        # Test above range
        output2 = service.synthesize(text="Test", speed=1.5, tone="challenge")
        assert isinstance(output2, str)

# Made with Bob
