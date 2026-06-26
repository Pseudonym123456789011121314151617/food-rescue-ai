"""High-level chat engine that ties providers, memory, and functions together."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from jarvis.ai.functions import FunctionRegistry
from jarvis.ai.memory.conversation import ConversationMemory
from jarvis.ai.providers.base import AIProvider, ChatMessage, ProviderConfig
from jarvis.ai.providers.lmstudio_provider import LMStudioProvider
from jarvis.ai.providers.ollama_provider import OllamaProvider
from jarvis.ai.providers.openai_provider import OpenAIProvider
from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

if TYPE_CHECKING:
    from jarvis.ai.memory.long_term import LongTermMemory

log = get_logger(__name__)

_PROVIDER_MAP: dict[str, type[AIProvider]] = {
    "openai": OpenAIProvider,
    "ollama": OllamaProvider,
    "lmstudio": LMStudioProvider,
}


class ChatEngine:
    """Orchestrates conversations with context, memory, and tool use."""

    def __init__(
        self,
        event_bus: EventBus,
        provider_config: ProviderConfig,
        long_term_memory: LongTermMemory | None = None,
        user_id: int | None = None,
    ) -> None:
        self._bus = event_bus
        self._user_id = user_id
        self._ltm = long_term_memory
        self._conversation = ConversationMemory()
        self._functions = FunctionRegistry()
        self._provider = self._create_provider(provider_config)

    @property
    def provider(self) -> AIProvider:
        return self._provider

    @property
    def conversation(self) -> ConversationMemory:
        return self._conversation

    def switch_provider(self, config: ProviderConfig) -> None:
        """Hot-swap the underlying AI provider."""
        self._provider = self._create_provider(config)
        log.info("provider_switched", provider=config.name)

    async def send(self, user_input: str) -> str:
        """Send a message and return the full response."""
        self._conversation.add_user_message(user_input)
        self._bus.emit(Event.AI_RESPONSE_START)

        context = self._build_context()
        response = await self._provider.chat(
            context,
            functions=self._functions.to_openai_schema() or None,
        )

        self._conversation.add_assistant_message(response.content)
        self._bus.emit(Event.AI_RESPONSE_END, content=response.content)

        # Auto-store important memories
        if self._ltm and self._user_id:
            await self._maybe_store_memory(user_input, response.content)

        return response.content

    async def send_stream(self, user_input: str) -> AsyncIterator[str]:
        """Send a message and yield tokens as they arrive."""
        self._conversation.add_user_message(user_input)
        self._bus.emit(Event.AI_RESPONSE_START)

        context = self._build_context()
        full_response = ""
        async for token in self._provider.chat_stream(context):
            full_response += token
            self._bus.emit(Event.AI_RESPONSE_CHUNK, token=token)
            yield token

        self._conversation.add_assistant_message(full_response)
        self._bus.emit(Event.AI_RESPONSE_END, content=full_response)

    def new_conversation(self) -> None:
        """Reset the conversation memory."""
        self._conversation.clear()

    def set_system_prompt(self, prompt: str) -> None:
        self._conversation.system_prompt = prompt

    # -- private helpers --

    @staticmethod
    def _create_provider(config: ProviderConfig) -> AIProvider:
        cls = _PROVIDER_MAP.get(config.name, OpenAIProvider)
        return cls(config)

    def _build_context(self) -> list[ChatMessage]:
        """Build the full context: system prompt + memory augmentation + conversation."""
        return self._conversation.messages

    async def _maybe_store_memory(self, user_input: str, response: str) -> None:
        """Heuristic: store interactions that seem important."""
        important_keywords = ["remember", "don't forget", "important", "always", "never"]
        if (
            any(kw in user_input.lower() for kw in important_keywords)
            and self._ltm
            and self._user_id
        ):
            self._ltm.store(
                self._user_id,
                f"User: {user_input}\nAssistant: {response}",
                category="conversation",
                importance=0.8,
            )
