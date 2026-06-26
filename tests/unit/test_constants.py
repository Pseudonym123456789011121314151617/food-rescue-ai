"""Tests for constants module."""

from __future__ import annotations

from jarvis.core.constants import (
    ACCESS_DENIED_RESPONSES,
    ANIMATION_DURATION_MS,
    APP_NAME,
    FACE_CONFIDENCE_THRESHOLD,
    MAX_LOGIN_ATTEMPTS,
    PARTICLE_COUNT,
)


class TestConstants:
    def test_app_name(self) -> None:
        assert APP_NAME == "JARVIS AI"

    def test_access_denied_responses(self) -> None:
        assert len(ACCESS_DENIED_RESPONSES) >= 20
        assert all(isinstance(r, str) for r in ACCESS_DENIED_RESPONSES)

    def test_thresholds(self) -> None:
        assert MAX_LOGIN_ATTEMPTS == 5
        assert FACE_CONFIDENCE_THRESHOLD == 0.6
        assert PARTICLE_COUNT == 80
        assert ANIMATION_DURATION_MS == 300
