"""Ollama local LLM provider."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from jarvis.ai.providers.base import (
    AIProvider,
    ChatMessage,
    ChatResponse,
    ProviderCapability,
    ProviderConfig,
)
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class OllamaProvider(AIProvider):
    """Provider for locally running Ollama server."""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        if not config.base_url:
            config.base_url = "http://localhost:11434"
        self._client: httpx.AsyncClient | None = None

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def capabilities(self) -> ProviderCapability:
        return ProviderCapability.CHAT | ProviderCapability.STREAMING

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.config.base_url,
                timeout=120.0,
            )
        return self._client

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        functions: list[dict[str, object]] | None = None,
    ) -> ChatResponse:
        client = self._get_client()
        payload = {
            "model": self.config.model or "llama3",
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {"temperature": self.config.temperature},
        }
        resp = await client.post("/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return ChatResponse(
            content=data.get("message", {}).get("content", ""),
            model=data.get("model", ""),
            tokens_prompt=data.get("prompt_eval_count", 0),
            tokens_completion=data.get("eval_count", 0),
        )

    async def chat_stream(
        self,
        messages: list[ChatMessage],
        *,
        functions: list[dict[str, object]] | None = None,
    ) -> AsyncIterator[str]:
        client = self._get_client()
        payload = {
            "model": self.config.model or "llama3",
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
            "options": {"temperature": self.config.temperature},
        }
        async with client.stream("POST", "/api/chat", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                token = data.get("message", {}).get("content", "")
                if token:
                    yield token
                if data.get("done"):
                    break

    async def health_check(self) -> bool:
        try:
            client = self._get_client()
            resp = await client.get("/api/tags")
            return resp.status_code == 200
        except Exception:
            return False
