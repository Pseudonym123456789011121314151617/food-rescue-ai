"""Application-wide constants."""

from __future__ import annotations

APP_NAME = "JARVIS AI"
APP_VERSION = "1.0.0"
ORG_NAME = "JarvisAI"
CONFIG_FILE = "jarvis.toml"
DB_FILE = "jarvis.db"
LOG_FILE = "jarvis.log"

# UI constants
WINDOW_MIN_WIDTH = 1280
WINDOW_MIN_HEIGHT = 800
SIDEBAR_WIDTH = 260
SIDEBAR_COLLAPSED_WIDTH = 64
DOCK_HEIGHT = 56
ANIMATION_DURATION_MS = 300
PARTICLE_COUNT = 80

# Face recognition
MAX_LOGIN_ATTEMPTS = 5
FACE_CONFIDENCE_THRESHOLD = 0.6
LOCKOUT_DURATION_SECONDS = 300

# AI defaults
DEFAULT_MODEL = "gpt-4o"
MAX_CONTEXT_MESSAGES = 50
STREAMING_CHUNK_SIZE = 64

# Speech
WAKE_WORD = "hey jarvis"
DEFAULT_TTS_RATE = 175
DEFAULT_TTS_VOLUME = 0.9

# Security
ENCRYPTION_ALGORITHM = "AES-256-GCM"
KEY_DERIVATION_ITERATIONS = 480_000

# Denied-access humorous responses
ACCESS_DENIED_RESPONSES: list[str] = [
    "Nice try.",
    "I almost believed that.",
    "Wrong human detected.",
    "Identity rejected.",
    "You are not who you claim to be.",
    "Access denied. Better luck next time.",
    "Impersonation level: amateur.",
    "My sensors say... nope.",
    "Face not recognized. Are you a ghost?",
    "Error 403: Wrong face detected.",
    "I don't remember creating you.",
    "That face is not in my database. Suspicious.",
    "Authentication failed. Try being someone else.",
    "Biometric mismatch. Initiating sass protocol.",
    "Sorry, I only open for the cool humans.",
    "You shall not pass!",
    "Scan complete. Result: intruder.",
    "Face recognition says: who are you?",
    "Your face doesn't ring a bell.",
    "Identity verification failed. Dramatically.",
    "Not today, stranger.",
    "The face scanner has spoken. It said no.",
    "Alert: unauthorized human detected.",
    "Nice face, but it's not the right one.",
    "I've seen better disguises.",
    "Facial recognition: 0% match. Impressive.",
    "My AI brain says you're not on the list.",
    "Denied. But thanks for the entertainment.",
    "Your face does not spark joy.",
    "Scanning... scanning... nah.",
    "Plot twist: you're not the main character.",
    "This is not a face I was trained to trust.",
    "I appreciate the effort, but no.",
    "Face not found. Have you tried rebooting yours?",
    "Sorry, the VIP list doesn't include you.",
    "Your face triggered my humor module instead.",
    "Attempting to match face... LOL no.",
    "The algorithm has trust issues with your face.",
    "Unauthorized access. Releasing virtual guard dogs.",
    "Face scan complete: stranger danger.",
]
