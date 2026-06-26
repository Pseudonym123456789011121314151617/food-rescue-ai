"""Short-term conversation memory with sliding window."""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.ai.providers.base import ChatMessage
from jarvis.core.constants import MAX_CONTEXT_MESSAGES


@dataclass
class ConversationMemory:
    """Maintains a rolling window of messages for context."""

    max_messages: int = MAX_CONTEXT_MESSAGES
    system_prompt: str = (
        "You are JARVIS, an advanced AI desktop assistant. "
        "You are helpful, witty, and capable. Respond concisely and accurately."
    )
    _messages: list[ChatMessage] = field(default_factory=list)

    @property
    def messages(self) -> list[ChatMessage]:
        """Return the system prompt + sliding window of recent messages."""
        system = [ChatMessage(role="system", content=self.system_prompt)]
        return system + self._messages[-self.max_messages :]

    def add_user_message(self, content: str) -> None:
        self._messages.append(ChatMessage(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self._messages.append(ChatMessage(role="assistant", content=content))

    def add_function_result(self, name: str, content: str) -> None:
        self._messages.append(ChatMessage(role="function", content=content, name=name))

    def clear(self) -> None:
        self._messages.clear()

    def to_dicts(self) -> list[dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def __len__(self) -> int:
        return len(self._messages)
