"""Custom exception hierarchy for JARVIS AI."""

from __future__ import annotations


class JarvisError(Exception):
    """Base exception for all JARVIS errors."""


class ConfigError(JarvisError):
    """Configuration loading or validation error."""


class DatabaseError(JarvisError):
    """Database operation error."""


class AuthenticationError(JarvisError):
    """Login / face-recognition failure."""


class AuthorizationError(JarvisError):
    """User lacks required permissions."""


class ProviderError(JarvisError):
    """AI provider communication error."""


class PluginError(JarvisError):
    """Plugin loading or execution error."""


class SpeechError(JarvisError):
    """Speech recognition or synthesis error."""


class VisionError(JarvisError):
    """Camera or vision processing error."""


class EncryptionError(JarvisError):
    """Encryption or decryption failure."""


class ComputerControlError(JarvisError):
    """System-control operation error."""
