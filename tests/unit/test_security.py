"""Tests for security and encryption utilities."""

from __future__ import annotations

from jarvis.core.exceptions import EncryptionError
from jarvis.core.security import Vault, generate_salt, hash_pin, verify_pin


class TestSecurity:
    def test_generate_salt_unique(self) -> None:
        s1 = generate_salt()
        s2 = generate_salt()
        assert s1 != s2
        assert len(s1) == 32

    def test_hash_and_verify_pin(self) -> None:
        hashed, salt = hash_pin("1234")
        assert verify_pin("1234", hashed, salt)
        assert not verify_pin("0000", hashed, salt)

    def test_vault_encrypt_decrypt(self) -> None:
        vault = Vault("test-passphrase")
        plaintext = b"Secret data to protect"
        encrypted = vault.encrypt(plaintext)
        assert encrypted != plaintext
        decrypted = vault.decrypt(encrypted)
        assert decrypted == plaintext

    def test_vault_different_passwords(self) -> None:
        import pytest

        v1 = Vault("password1")
        v2 = Vault("password2")
        encrypted = v1.encrypt(b"hello")
        with pytest.raises(EncryptionError):
            v2.decrypt(encrypted)
