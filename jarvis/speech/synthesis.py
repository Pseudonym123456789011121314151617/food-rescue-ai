"""Text-to-speech synthesis engine."""

from __future__ import annotations

import threading
from typing import Any

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class SpeechSynthesizer:
    """Text → audible speech using configurable TTS backends."""

    def __init__(
        self,
        event_bus: EventBus,
        engine: str = "pyttsx3",
        rate: int = 175,
        volume: float = 0.9,
        voice_id: str = "",
    ) -> None:
        self._bus = event_bus
        self._engine_name = engine
        self._rate = rate
        self._volume = volume
        self._voice_id = voice_id
        self._speaking = False
        self._engine_instance: object | None = None
        self._lock = threading.Lock()

    @property
    def is_speaking(self) -> bool:
        return self._speaking

    def speak(self, text: str) -> None:
        """Speak text in a background thread (non-blocking)."""
        t = threading.Thread(target=self._speak_blocking, args=(text,), daemon=True)
        t.start()

    def stop(self) -> None:
        """Interrupt current speech."""
        self._speaking = False
        try:
            if self._engine_instance is not None:
                import pyttsx3

                assert isinstance(self._engine_instance, pyttsx3.Engine)
                self._engine_instance.stop()
        except Exception:
            pass

    def get_available_voices(self) -> list[dict[str, str]]:
        """List available TTS voices."""
        try:
            engine = self._get_engine()
            if engine is None:
                return []
            voices = engine.getProperty("voices")
            return [
                {"id": v.id, "name": v.name, "languages": str(getattr(v, "languages", []))}
                for v in voices
            ]
        except Exception:
            return []

    def set_voice(self, voice_id: str) -> None:
        self._voice_id = voice_id

    def set_rate(self, rate: int) -> None:
        self._rate = rate

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))

    def _get_engine(self) -> Any:
        try:
            import pyttsx3

            if self._engine_instance is None:
                self._engine_instance = pyttsx3.init()
            engine = self._engine_instance
            assert isinstance(engine, pyttsx3.Engine)
            engine.setProperty("rate", self._rate)
            engine.setProperty("volume", self._volume)
            if self._voice_id:
                engine.setProperty("voice", self._voice_id)
            return engine  # noqa: TRY300
        except ImportError:
            log.warning("pyttsx3_not_installed")
            return None

    def _speak_blocking(self, text: str) -> None:
        with self._lock:
            self._speaking = True
            self._bus.emit(Event.TTS_START, text=text)
            try:
                engine = self._get_engine()
                if engine is None:
                    return
                import pyttsx3

                assert isinstance(engine, pyttsx3.Engine)
                engine.say(text)
                engine.runAndWait()
            except Exception:
                log.exception("tts_error")
            finally:
                self._speaking = False
                self._bus.emit(Event.TTS_END)
