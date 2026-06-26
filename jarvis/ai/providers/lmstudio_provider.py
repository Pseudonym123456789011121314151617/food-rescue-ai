"""LM Studio local provider (OpenAI-compatible API)."""

from __future__ import annotations

from jarvis.ai.providers.base import ProviderCapability, ProviderConfig
from jarvis.ai.providers.openai_provider import OpenAIProvider


class LMStudioProvider(OpenAIProvider):
    """LM Studio exposes an OpenAI-compatible API on localhost."""

    def __init__(self, config: ProviderConfig) -> None:
        if not config.base_url:
            config.base_url = "http://localhost:1234/v1"
        if not config.api_key:
            config.api_key = "lm-studio"
        super().__init__(config)

    @property
    def name(self) -> str:
        return "lmstudio"

    @property
    def capabilities(self) -> ProviderCapability:
        return ProviderCapability.CHAT | ProviderCapability.STREAMING
