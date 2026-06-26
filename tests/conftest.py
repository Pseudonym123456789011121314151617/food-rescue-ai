"""Shared pytest fixtures for JARVIS AI tests."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from jarvis.core.config import AppConfig
from jarvis.core.database import DatabaseManager
from jarvis.core.events import EventBus


@pytest.fixture()
def tmp_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture()
def event_bus() -> EventBus:
    bus = EventBus()
    yield bus
    bus.clear()


@pytest.fixture()
def config(tmp_dir: Path) -> AppConfig:
    os.environ["JARVIS_DATA_DIR"] = str(tmp_dir / "data")
    os.environ["JARVIS_CONFIG_DIR"] = str(tmp_dir / "config")
    os.environ["JARVIS_LOG_DIR"] = str(tmp_dir / "logs")
    cfg = AppConfig.load()
    yield cfg
    for key in ("JARVIS_DATA_DIR", "JARVIS_CONFIG_DIR", "JARVIS_LOG_DIR"):
        os.environ.pop(key, None)


@pytest.fixture()
def db(tmp_dir: Path) -> Generator[DatabaseManager, None, None]:
    db_path = tmp_dir / "test.db"
    manager = DatabaseManager(f"sqlite:///{db_path}")
    manager.initialize()
    yield manager
    manager.close()
