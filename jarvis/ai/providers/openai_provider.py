"""OpenAI-compatible provider (works with OpenAI API and compatible endpoints)."""

from __future__ import annotations

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


class OpenAIProvider(AIProvider):
    """Provider for OpenAI API and compatible endpoints."""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        if not config.base_url:
            config.base_url = "https://api.openai.com/v1"
        self._client: httpx.AsyncClient | None = None

    @property
    def name(self) -> str:
        return "openai"

    @property
    def capabilities(self) -> ProviderCapability:
        return (
            ProviderCapability.CHAT
            | ProviderCapability.STREAMING
            | ProviderCapability.FUNCTION_CALLING
            | ProviderCapability.VISION
            | ProviderCapability.EMBEDDINGS
        )

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.config.base_url,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    def _build_payload(
        self,
        messages: list[ChatMessage],
        *,
        stream: bool = False,
        functions: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.config.model or "gpt-4o",
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": stream,
        }
        if functions:
            payload["functions"] = functions
        return payload

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        functions: list[dict[str, object]] | None = None,
    ) -> ChatResponse:
        client = self._get_client()
        payload = self._build_payload(messages, functions=functions)
        resp = await client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})
        fc = choice.get("message", {}).get("function_call")
        return ChatResponse(
            content=choice["message"]["content"] or "",
            model=data.get("model", ""),
            tokens_prompt=usage.get("prompt_tokens", 0),
            tokens_completion=usage.get("completion_tokens", 0),
            finish_reason=choice.get("finish_reason", "stop"),
            function_call=fc,
        )

    async def chat_stream(
        self,
        messages: list[ChatMessage],
        *,
        functions: list[dict[str, object]] | None = None,
    ) -> AsyncIterator[str]:
        client = self._get_client()
        payload = self._build_payload(messages, stream=True, functions=functions)
        async with client.stream("POST", "/chat/completions", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                chunk = line[6:]
                if chunk.strip() == "[DONE]":
                    break
                import json

                parsed = json.loads(chunk)
                delta = parsed["choices"][0].get("delta", {})
                token = delta.get("content")
                if token:
                    yield token

    async def get_embedding(self, text: str) -> list[float]:
        client = self._get_client()
        resp = await client.post(
            "/embeddings",
            json={"model": "text-embedding-3-small", "input": text},
        )
        resp.raise_for_status()
        data: list[float] = resp.json()["data"][0]["embedding"]
        return data

    async def health_check(self) -> bool:
        try:
            client = self._get_client()
            resp = await client.get("/models")
            return resp.status_code == 200
        except Exception:
            return False
