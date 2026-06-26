# JARVIS AI — Installation Guide

## Requirements

- Python 3.13+
- PySide6 6.7+
- A supported OS: Windows 10+, macOS 12+, or Linux (Ubuntu 22.04+)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/jarvis-ai.git
cd jarvis-ai

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install core dependencies
pip install -e .

# Run JARVIS
python -m jarvis
```

## Optional Extras

```bash
# Face recognition support
pip install -e ".[face]"

# Speech recognition + TTS
pip install -e ".[speech]"

# GPU acceleration
pip install -e ".[gpu]"

# Development tools (testing, linting)
pip install -e ".[dev]"

# All extras
pip install -e ".[face,speech,gpu,dev]"
```

## Configuration

JARVIS creates its config file automatically at:
- **Windows**: `%APPDATA%/JARVIS AI/jarvis.toml`
- **macOS**: `~/Library/Application Support/JARVIS AI/jarvis.toml`
- **Linux**: `~/.local/share/jarvis-ai/jarvis.toml`

## AI Provider Setup

### OpenAI
Set your API key in the config or environment:
```bash
export JARVIS_AI__API_KEY=sk-your-key-here
```

### Ollama (Local)
Install [Ollama](https://ollama.ai/) and pull a model:
```bash
ollama pull llama3
```

### LM Studio
Start LM Studio's local server on port 1234 (default).

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```
