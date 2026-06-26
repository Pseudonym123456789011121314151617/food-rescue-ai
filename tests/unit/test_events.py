"""Tests for the EventBus pub/sub system."""

from __future__ import annotations

from jarvis.core.events import Event, EventBus


class TestEventBus:
    def test_subscribe_and_emit(self, event_bus: EventBus) -> None:
        received: list[dict[str, object]] = []

        def handler(**kwargs: object) -> None:
            received.append(kwargs)

        event_bus.subscribe(Event.APP_STARTED, handler)
        event_bus.emit(Event.APP_STARTED, source="test")

        assert len(received) == 1
        assert received[0]["source"] == "test"

    def test_unsubscribe(self, event_bus: EventBus) -> None:
        calls = []

        def handler(**kwargs: object) -> None:
            calls.append(1)

        event_bus.subscribe(Event.APP_STARTED, handler)
        event_bus.unsubscribe(Event.APP_STARTED, handler)
        event_bus.emit(Event.APP_STARTED)

        assert len(calls) == 0

    def test_multiple_subscribers(self, event_bus: EventBus) -> None:
        results: list[str] = []

        def h1(**kwargs: object) -> None:
            results.append("h1")

        def h2(**kwargs: object) -> None:
            results.append("h2")

        event_bus.subscribe(Event.APP_STARTED, h1)
        event_bus.subscribe(Event.APP_STARTED, h2)
        event_bus.emit(Event.APP_STARTED)

        assert results == ["h1", "h2"]

    def test_clear(self, event_bus: EventBus) -> None:
        calls = []

        def handler(**kwargs: object) -> None:
            calls.append(1)

        event_bus.subscribe(Event.APP_STARTED, handler)
        event_bus.clear()
        event_bus.emit(Event.APP_STARTED)

        assert len(calls) == 0

    def test_emit_unknown_event_no_crash(self, event_bus: EventBus) -> None:
        event_bus.emit(Event.THEME_CHANGED, theme="dark")
