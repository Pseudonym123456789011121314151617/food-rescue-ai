"""High-level cryptographic convenience functions."""

from __future__ import annotations

import hashlib
import secrets
import string


def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_hex(length)


def generate_pin(length: int = 4) -> str:
    """Generate a random numeric PIN."""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def sha256(data: str | bytes) -> str:
    """Return the SHA-256 hex digest of *data*."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()
