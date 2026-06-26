"""Tests for AppConfig loading and validation."""

from __future__ import annotations

from pathlib import Path

from jarvis.core.config import AppConfig


class TestAppConfig:
    def test_load_defaults(self, config: AppConfig) -> None:
        assert config.ai.model == "gpt-4o"
        assert config.ai.temperature == 0.7
        assert config.ai.streaming is True
        assert config.security.max_login_attempts == 5

    def test_directories_created(self, config: AppConfig) -> None:
        assert Path(config.data_dir).exists()
        assert Path(config.config_dir).exists()
        assert Path(config.log_dir).exists()

    def test_ui_defaults(self, config: AppConfig) -> None:
        assert config.ui.accent_color == "#00d4ff"
        assert config.ui.animations_enabled is True
        assert config.ui.particle_effects is True

    def test_speech_defaults(self, config: AppConfig) -> None:
        assert config.speech.wake_word == "hey jarvis"
        assert config.speech.tts_rate == 175
        assert config.speech.tts_volume == 0.9
