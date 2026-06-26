# JARVIS AI — Developer Guide

## Development Setup

```bash
git clone https://github.com/your-org/jarvis-ai.git
cd jarvis-ai
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Project Structure

```
jarvis/
├── __init__.py          # Package metadata
├── __main__.py          # Entry point
├── app.py               # Application orchestrator
├── core/                # Core infrastructure
│   ├── config.py        # Configuration (Pydantic + TOML)
│   ├── constants.py     # App-wide constants
│   ├── database.py      # SQLAlchemy database manager
│   ├── events.py        # EventBus pub/sub system
│   ├── exceptions.py    # Exception hierarchy
│   ├── logging.py       # Structured logging setup
│   └── security.py      # Encryption, hashing, vault
├── models/              # SQLAlchemy ORM models
├── services/            # Business logic services
├── ai/                  # AI providers, memory, functions
├── speech/              # STT, TTS, wake word
├── vision/              # Face recognition, OCR, QR
├── computer/            # System control, file ops
├── plugins/             # Plugin SDK, loader, manager
├── ui/                  # PySide6 UI layer
│   ├── components/      # Reusable widgets
│   ├── themes/          # Theme engine + stylesheets
│   ├── login/           # Login screen
│   ├── dashboard/       # Dashboard + widgets
│   ├── chat/            # AI chat panel
│   ├── settings/        # Settings page
│   └── pages/           # File manager, terminal, etc.
└── utils/               # Utilities
```

## Code Style

- Python 3.13+ with type hints everywhere
- Ruff for linting and formatting
- MyPy for type checking
- Docstrings for all public APIs

## Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=jarvis --cov-report=html
```

## Linting

```bash
ruff check jarvis/ tests/
ruff format jarvis/ tests/
mypy jarvis/ --ignore-missing-imports
```

## Adding a New Page

1. Create `jarvis/ui/pages/my_page.py`
2. Import in `jarvis/ui/main_window.py`
3. Add to sidebar items in `jarvis/ui/components/sidebar.py`
4. Register in `MainWindow._build_pages()`

## Adding an AI Provider

1. Create `jarvis/ai/providers/my_provider.py`
2. Extend `AIProvider` base class
3. Implement `chat()` and `chat_stream()` methods
4. Register in `ChatEngine`
