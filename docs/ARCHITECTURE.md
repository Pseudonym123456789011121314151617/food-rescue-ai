# JARVIS AI — Architecture Guide

## Overview

JARVIS AI is built with clean architecture principles: separation of concerns,
dependency inversion, and event-driven communication between subsystems.

## Layer Diagram

```
┌─────────────────────────────────────────────────┐
│                    UI Layer                      │
│  PySide6 widgets, themes, pages, animations      │
├─────────────────────────────────────────────────┤
│                 Service Layer                    │
│  UserService, AuthService, NotificationService   │
├─────────────────────────────────────────────────┤
│                   Core Layer                     │
│  Config, Database, EventBus, Security, Logging   │
├─────────────────────────────────────────────────┤
│                 Domain Models                    │
│  User, Conversation, ChatMessage, Memory, Plugin │
├─────────────────────────────────────────────────┤
│               AI / Speech / Vision               │
│  Providers, Memory, Functions, Recognition, TTS  │
├─────────────────────────────────────────────────┤
│             Computer Control / Plugins           │
│  App control, file ops, system, browser, media   │
└─────────────────────────────────────────────────┘
```

## Module Map

| Module | Purpose |
|--------|---------|
| `jarvis/core/` | Config, database, events, security, logging, constants |
| `jarvis/models/` | SQLAlchemy ORM models for users, chat, memory, plugins |
| `jarvis/services/` | Business logic: user CRUD, authentication, notifications |
| `jarvis/ai/` | Multi-provider AI, conversation memory, semantic search, function calling |
| `jarvis/speech/` | Wake-word detection, speech recognition, text-to-speech, voice profiles |
| `jarvis/vision/` | Face recognition, object detection, QR/barcode scanning, OCR |
| `jarvis/computer/` | App launching, file ops, system control, browser, media |
| `jarvis/plugins/` | Plugin SDK, loader, manager with hot-reload |
| `jarvis/ui/` | PySide6 UI: themes, components, pages |
| `jarvis/utils/` | Async runner, crypto, GPU detection, platform info |

## Event-Driven Architecture

All subsystems communicate via `EventBus` (pub/sub). Events are defined in
`jarvis/core/events.py` with 200+ event types covering login, AI, speech,
UI, plugins, and system events.

## Database

SQLite by default; optional PostgreSQL via config. All models use SQLAlchemy
ORM with automatic table creation.

## Security

- PIN/password hashing with PBKDF2 + salt
- Database encryption with Fernet (AES-128-CBC)
- Face recognition encoding comparison
- Account lockout after failed attempts
- Role-based access control (Admin, User, Family, Guest)
