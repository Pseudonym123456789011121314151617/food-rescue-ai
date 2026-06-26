"""Abstract base class for AI providers."""

from __future__ import annotations

import abc
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from enum import Flag, auto


class ProviderCapability(Flag):
    CHAT = auto()
    STREAMING = auto()
    FUNCTION_CALLING = auto()
    VISION = auto()
    EMBEDDINGS = auto()


@dataclass
class ChatMessage:
    role: str
    content: str
    name: str | None = None
    function_call: dict[str, str] | None = None


@dataclass
class ChatResponse:
    content: str
    model: str = ""
    tokens_prompt: int = 0
    tokens_completion: int = 0
    finish_reason: str = "stop"
    function_call: dict[str, str] | None = None


@dataclass
class ProviderConfig:
    name: str = ""
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 4096
    extra: dict[str, str] = field(default_factory=dict)


class AIProvider(abc.ABC):
    """Contract every AI provider must implement."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @property
    @abc.abstractmethod
    def capabilities(self) -> ProviderCapability: ...

    @abc.abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        functions: list[dict[str, object]] | None = None,
    ) -> ChatResponse:
        """Send a chat completion request and return the full response."""

    @abc.abstractmethod
    def chat_stream(
        self,
        messages: list[ChatMessage],
        *,
        functions: list[dict[str, object]] | None = None,
    ) -> AsyncIterator[str]:
        """Yield response tokens as they arrive."""
        ...

    async def get_embedding(self, text: str) -> list[float]:
        """Return an embedding vector. Override if supported."""
        raise NotImplementedError(f"{self.name} does not support embeddings")

    async def health_check(self) -> bool:
        """Return True if the provider is reachable."""
        return True
