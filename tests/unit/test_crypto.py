"""Tests for crypto utilities."""

from __future__ import annotations

from jarvis.utils.crypto import generate_pin, generate_token, sha256


class TestCrypto:
    def test_generate_token_length(self) -> None:
        token = generate_token(32)
        assert len(token) == 64  # hex encoding doubles length

    def test_generate_pin(self) -> None:
        pin = generate_pin(6)
        assert len(pin) == 6
        assert pin.isdigit()

    def test_sha256(self) -> None:
        h1 = sha256("hello")
        h2 = sha256("hello")
        h3 = sha256("world")
        assert h1 == h2
        assert h1 != h3
        assert len(h1) == 64
