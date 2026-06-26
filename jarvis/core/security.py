"""Encryption, hashing, and key management utilities."""

from __future__ import annotations

import hashlib
import os
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from jarvis.core.constants import KEY_DERIVATION_ITERATIONS
from jarvis.core.exceptions import EncryptionError
from jarvis.core.logging import get_logger

log = get_logger(__name__)


def generate_salt(length: int = 32) -> bytes:
    """Return cryptographically secure random salt."""
    return os.urandom(length)


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password + salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KEY_DERIVATION_ITERATIONS,
    )
    import base64

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def hash_pin(pin: str, salt: bytes | None = None) -> tuple[str, bytes]:
    """Hash a PIN with PBKDF2-SHA256; returns (hex_hash, salt)."""
    if salt is None:
        salt = generate_salt(16)
    dk = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, KEY_DERIVATION_ITERATIONS)
    return dk.hex(), salt


def verify_pin(pin: str, stored_hash: str, salt: bytes) -> bool:
    """Verify a PIN against a stored hash."""
    computed, _ = hash_pin(pin, salt)
    return secrets.compare_digest(computed, stored_hash)


class Vault:
    """Encrypt / decrypt arbitrary data with a master key."""

    def __init__(self, master_password: str, salt: bytes | None = None) -> None:
        self._salt = salt or generate_salt()
        key = derive_key(master_password, self._salt)
        self._fernet = Fernet(key)

    @property
    def salt(self) -> bytes:
        return self._salt

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt *data* and return cipher-text."""
        try:
            return self._fernet.encrypt(data)
        except Exception as exc:
            raise EncryptionError(f"Encryption failed: {exc}") from exc

    def decrypt(self, token: bytes) -> bytes:
        """Decrypt *token* and return plain-text."""
        try:
            return self._fernet.decrypt(token)
        except Exception as exc:
            raise EncryptionError(f"Decryption failed: {exc}") from exc

    def encrypt_text(self, text: str) -> str:
        """Encrypt a string; return base64 cipher-text string."""
        import base64

        ct = self.encrypt(text.encode("utf-8"))
        return base64.urlsafe_b64encode(ct).decode("ascii")

    def decrypt_text(self, token_str: str) -> str:
        """Decrypt a base64 cipher-text string."""
        import base64

        ct = base64.urlsafe_b64decode(token_str.encode("ascii"))
        return self.decrypt(ct).decode("utf-8")
