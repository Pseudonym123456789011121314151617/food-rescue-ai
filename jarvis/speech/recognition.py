"""Speech-to-text recognition engine."""

from __future__ import annotations

import threading
from collections.abc import Callable

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class SpeechRecognizer:
    """Microphone → text using configurable STT backends."""

    def __init__(self, event_bus: EventBus, engine: str = "google") -> None:
        self._bus = event_bus
        self._engine = engine
        self._running = False
        self._thread: threading.Thread | None = None
        self._callback: Callable[[str], None] | None = None

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self, callback: Callable[[str], None] | None = None) -> None:
        """Begin continuous listening in a background thread."""
        if self._running:
            return
        self._callback = callback
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        log.info("speech_recognition_started", engine=self._engine)

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        log.info("speech_recognition_stopped")

    def _listen_loop(self) -> None:
        """Blocking loop that captures audio and transcribes."""
        try:
            import speech_recognition as sr

            recognizer = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)

            while self._running:
                with mic as source:
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                    except sr.WaitTimeoutError:
                        continue

                try:
                    text = self._transcribe(recognizer, audio)
                    if text:
                        self._bus.emit(Event.SPEECH_RECOGNIZED, text=text)
                        if self._callback:
                            self._callback(text)
                except Exception:
                    log.exception("transcription_error")
        except ImportError:
            log.warning("speech_recognition_not_installed")
            self._running = False

    def _transcribe(self, recognizer: object, audio: object) -> str:
        """Dispatch to the configured engine."""
        import speech_recognition as sr

        assert isinstance(recognizer, sr.Recognizer)
        if self._engine == "google":
            return str(recognizer.recognize_google(audio))
        return ""
