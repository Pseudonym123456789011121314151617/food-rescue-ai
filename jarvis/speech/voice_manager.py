"""Voice profile management: per-user voice settings and emotion system."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from jarvis.core.logging import get_logger

log = get_logger(__name__)


class Emotion(Enum):
    NEUTRAL = auto()
    HAPPY = auto()
    CONCERNED = auto()
    EXCITED = auto()
    SARCASTIC = auto()
    CALM = auto()


@dataclass
class VoiceProfile:
    voice_id: str = ""
    rate: int = 175
    volume: float = 0.9
    pitch: float = 1.0
    emotion: Emotion = Emotion.NEUTRAL


class VoiceManager:
    """Manages per-user voice profiles and emotion-based TTS adjustments."""

    def __init__(self) -> None:
        self._profiles: dict[int, VoiceProfile] = {}
        self._current_emotion = Emotion.NEUTRAL

    def get_profile(self, user_id: int) -> VoiceProfile:
        if user_id not in self._profiles:
            self._profiles[user_id] = VoiceProfile()
        return self._profiles[user_id]

    def set_profile(self, user_id: int, profile: VoiceProfile) -> None:
        self._profiles[user_id] = profile

    def set_emotion(self, emotion: Emotion) -> None:
        self._current_emotion = emotion

    @property
    def current_emotion(self) -> Emotion:
        return self._current_emotion

    def adjust_for_emotion(self, profile: VoiceProfile) -> VoiceProfile:
        """Return a modified profile reflecting the current emotion."""
        adjusted = VoiceProfile(
            voice_id=profile.voice_id,
            rate=profile.rate,
            volume=profile.volume,
            pitch=profile.pitch,
            emotion=self._current_emotion,
        )
        if self._current_emotion == Emotion.HAPPY:
            adjusted.rate = int(profile.rate * 1.1)
            adjusted.pitch = profile.pitch * 1.15
        elif self._current_emotion == Emotion.CONCERNED:
            adjusted.rate = int(profile.rate * 0.9)
            adjusted.pitch = profile.pitch * 0.95
        elif self._current_emotion == Emotion.EXCITED:
            adjusted.rate = int(profile.rate * 1.2)
            adjusted.volume = min(1.0, profile.volume * 1.1)
        elif self._current_emotion == Emotion.CALM:
            adjusted.rate = int(profile.rate * 0.85)
            adjusted.volume = profile.volume * 0.9
        return adjusted
