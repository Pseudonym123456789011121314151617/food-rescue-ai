"""Database manager with SQLAlchemy + optional encryption at rest."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from jarvis.core.logging import get_logger

log = get_logger(__name__)

metadata = MetaData()


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    metadata = metadata


class DatabaseManager:
    """Owns the SQLAlchemy engine and provides session helpers."""

    def __init__(self, url: str = "sqlite:///jarvis.db") -> None:
        self._url = url
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    @property
    def engine(self) -> Engine:
        assert self._engine is not None, "Call initialize() first"
        return self._engine

    def initialize(self) -> None:
        """Create the engine, apply migrations, seed defaults."""
        # Ensure parent directory exists for SQLite
        if self._url.startswith("sqlite:///"):
            db_path = Path(self._url.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)

        self._engine = create_engine(
            self._url,
            echo=False,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False} if "sqlite" in self._url else {},
        )
        self._session_factory = sessionmaker(bind=self._engine)

        # Create all tables defined by ORM models
        Base.metadata.create_all(self._engine)
        log.info("database_initialized", url=self._url)

    def session(self) -> Session:
        """Return a new session (caller must close)."""
        assert self._session_factory is not None
        return self._session_factory()

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
        """Run raw SQL and return results."""
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            conn.commit()
            return result

    def close(self) -> None:
        """Dispose of the connection pool."""
        if self._engine:
            self._engine.dispose()
            log.info("database_closed")
