"""Application-wide event bus (publish / subscribe)."""

from __future__ import annotations

import asyncio
import contextlib
from collections import defaultdict
from collections.abc import Callable
from enum import Enum, auto
from typing import Any

from jarvis.core.logging import get_logger

log = get_logger(__name__)

Callback = Callable[..., Any]


class Event(Enum):
    """Catalogue of application events."""

    # App lifecycle
    APP_STARTED = auto()
    APP_SHUTDOWN = auto()

    # Auth
    USER_LOGIN = auto()
    USER_LOGOUT = auto()
    LOGIN_FAILED = auto()
    ACCOUNT_LOCKED = auto()

    # AI
    AI_RESPONSE_START = auto()
    AI_RESPONSE_CHUNK = auto()
    AI_RESPONSE_END = auto()
    AI_ERROR = auto()

    # Speech
    WAKE_WORD_DETECTED = auto()
    SPEECH_RECOGNIZED = auto()
    TTS_START = auto()
    TTS_END = auto()

    # UI
    THEME_CHANGED = auto()
    VIEW_CHANGED = auto()
    NOTIFICATION = auto()
    FULLSCREEN_TOGGLED = auto()

    # System
    PLUGIN_LOADED = auto()
    PLUGIN_UNLOADED = auto()
    SETTINGS_CHANGED = auto()
    SHUTDOWN_REQUESTED = auto()

    # Computer control
    APP_LAUNCHED = auto()
    SCREENSHOT_TAKEN = auto()

    # Camera
    FACE_DETECTED = auto()
    QR_SCANNED = auto()


class EventBus:
    """Thread-safe, synchronous + async event dispatcher."""

    def __init__(self) -> None:
        self._listeners: dict[Event, list[Callback]] = defaultdict(list)

    def subscribe(self, event: Event, callback: Callback) -> None:
        """Register *callback* for *event*."""
        self._listeners[event].append(callback)

    def unsubscribe(self, event: Event, callback: Callback) -> None:
        """Remove a previously registered callback."""
        with contextlib.suppress(ValueError):
            self._listeners[event].remove(callback)

    def emit(self, event: Event, **kwargs: Any) -> None:  # noqa: ANN401
        """Fire *event* and call every registered listener synchronously."""
        for cb in self._listeners.get(event, []):
            try:
                result = cb(**kwargs)
                if asyncio.iscoroutine(result):
                    # Schedule coroutine on the running loop if available
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(result)
                    except RuntimeError:
                        asyncio.run(result)
            except Exception:
                log.exception("event_handler_error", event_name=event.name)

    def clear(self) -> None:
        """Remove all listeners."""
        self._listeners.clear()
