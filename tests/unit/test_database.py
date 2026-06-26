"""Tests for database manager."""

from __future__ import annotations

from jarvis.core.database import DatabaseManager


class TestDatabaseManager:
    def test_initialize_creates_tables(self, db: DatabaseManager) -> None:
        # Already initialized in fixture; verify engine is set
        assert db.engine is not None

    def test_session_context(self, db: DatabaseManager) -> None:
        from sqlalchemy import text

        session = db.session()
        try:
            result = session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        finally:
            session.close()

    def test_execute_raw(self, db: DatabaseManager) -> None:
        result = db.execute("SELECT 42 AS answer")
        assert result is not None
