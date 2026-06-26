"""Tests for conversation memory."""

from __future__ import annotations

from jarvis.ai.memory.conversation import ConversationMemory


class TestConversationMemory:
    def test_add_messages(self) -> None:
        mem = ConversationMemory(system_prompt="You are JARVIS.", max_messages=10)
        mem.add_user_message("Hello")
        mem.add_assistant_message("Hi there!")

        msgs = mem.messages
        assert len(msgs) == 3  # system + user + assistant
        assert msgs[0].role == "system"
        assert msgs[1].role == "user"
        assert msgs[2].role == "assistant"

    def test_sliding_window(self) -> None:
        mem = ConversationMemory(system_prompt="Test", max_messages=4)
        for i in range(10):
            mem.add_user_message(f"msg {i}")

        msgs = mem.messages
        # system + last 4
        assert len(msgs) == 5

    def test_clear(self) -> None:
        mem = ConversationMemory(system_prompt="Test")
        mem.add_user_message("Hello")
        mem.clear()
        assert len(mem.messages) == 1  # only system remains
