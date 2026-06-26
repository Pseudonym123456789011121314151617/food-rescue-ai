"""Wake word detection (\"Hey Jarvis\")."""

from __future__ import annotations

import threading
from collections.abc import Callable

from jarvis.core.constants import WAKE_WORD
from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class WakeWordDetector:
    """Continuously listens for the wake phrase in a background thread."""

    def __init__(
        self,
        event_bus: EventBus,
        wake_word: str = WAKE_WORD,
        on_detected: Callable[[], None] | None = None,
    ) -> None:
        self._bus = event_bus
        self._wake_word = wake_word.lower()
        self._on_detected = on_detected
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._detect_loop, daemon=True)
        self._thread.start()
        log.info("wake_word_detector_started", wake_word=self._wake_word)

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _detect_loop(self) -> None:
        """Simple STT-based wake word detection."""
        try:
            import speech_recognition as sr

            recognizer = sr.Recognizer()
            mic = sr.Microphone()

            while self._running:
                with mic as source:
                    try:
                        audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    except sr.WaitTimeoutError:
                        continue

                try:
                    text = recognizer.recognize_google(audio).lower()
                    if self._wake_word in text:
                        log.info("wake_word_detected")
                        self._bus.emit(Event.WAKE_WORD_DETECTED)
                        if self._on_detected:
                            self._on_detected()
                except sr.UnknownValueError:
                    pass
                except Exception:
                    log.exception("wake_word_error")
        except ImportError:
            log.warning("speech_recognition_not_available")
            self._running = False
