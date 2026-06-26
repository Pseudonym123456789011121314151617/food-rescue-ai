"""Application configuration with layered loading (defaults → file → env)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import toml
from platformdirs import user_config_dir, user_data_dir, user_log_dir
from pydantic import Field
from pydantic_settings import BaseSettings

from jarvis.core.constants import APP_NAME, CONFIG_FILE, DB_FILE, LOG_FILE, ORG_NAME


def _config_dir() -> Path:
    return Path(user_config_dir(APP_NAME, ORG_NAME))


def _data_dir() -> Path:
    return Path(user_data_dir(APP_NAME, ORG_NAME))


def _log_dir() -> Path:
    return Path(user_log_dir(APP_NAME, ORG_NAME))


class AIProviderConfig(BaseSettings):
    """Settings for a single AI provider."""

    name: str = "openai"
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    streaming: bool = True


class SpeechConfig(BaseSettings):
    """Speech subsystem settings."""

    enabled: bool = True
    wake_word: str = "hey jarvis"
    tts_engine: str = "pyttsx3"
    tts_rate: int = 175
    tts_volume: float = 0.9
    stt_engine: str = "google"
    voice_id: str = ""


class UIConfig(BaseSettings):
    """UI / theme settings."""

    theme: str = "dark_futuristic"
    animations_enabled: bool = True
    particle_effects: bool = True
    blur_enabled: bool = True
    glassmorphism: bool = True
    fullscreen: bool = False
    font_size: int = 14
    accent_color: str = "#00d4ff"
    language: str = "en"


class SecurityConfig(BaseSettings):
    """Security and encryption settings."""

    encryption_enabled: bool = True
    face_recognition_enabled: bool = True
    pin_fallback: bool = True
    password_fallback: bool = True
    max_login_attempts: int = 5
    lockout_duration_seconds: int = 300
    audit_logging: bool = True


class AppConfig(BaseSettings):
    """Root configuration container."""

    config_dir: Path = Field(default_factory=_config_dir)
    data_dir: Path = Field(default_factory=_data_dir)
    log_dir: Path = Field(default_factory=_log_dir)
    database_url: str = ""
    log_level: str = "INFO"
    log_file: str = ""

    ai: AIProviderConfig = Field(default_factory=AIProviderConfig)
    speech: SpeechConfig = Field(default_factory=SpeechConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    # Extra AI providers keyed by name
    ai_providers: dict[str, AIProviderConfig] = Field(default_factory=dict)

    # Plugin directories
    plugin_dirs: list[str] = Field(default_factory=lambda: ["plugins"])

    def model_post_init(self, __context: Any) -> None:  # noqa: ANN401
        """Ensure directories exist and set derived defaults."""
        for d in (self.config_dir, self.data_dir, self.log_dir):
            d.mkdir(parents=True, exist_ok=True)
        if not self.database_url:
            self.database_url = f"sqlite:///{self.data_dir / DB_FILE}"
        if not self.log_file:
            self.log_file = str(self.log_dir / LOG_FILE)

    @classmethod
    def load(cls, path: Path | None = None) -> AppConfig:
        """Load config from TOML file, then overlay environment variables."""
        config_path = path or (_config_dir() / CONFIG_FILE)
        file_data: dict[str, Any] = {}
        if config_path.exists():
            file_data = toml.load(config_path)

        # Environment variable overrides (JARVIS_ prefix)
        env_overrides: dict[str, Any] = {}
        for key, val in os.environ.items():
            if key.startswith("JARVIS_"):
                env_overrides[key[7:].lower()] = val

        merged = {**file_data, **env_overrides}
        return cls(**merged)

    def save(self, path: Path | None = None) -> None:
        """Persist current config to TOML."""
        config_path = path or (self.config_dir / CONFIG_FILE)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        data = self.model_dump(mode="json", exclude_none=True)
        with open(config_path, "w") as fh:
            toml.dump(data, fh)
