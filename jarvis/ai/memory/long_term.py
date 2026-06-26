"""Long-term memory persistence and retrieval."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from jarvis.core.logging import get_logger
from jarvis.models.memory import MemoryEntry

if TYPE_CHECKING:
    from jarvis.core.database import DatabaseManager

log = get_logger(__name__)


class LongTermMemory:
    """Stores and retrieves persistent memories per user."""

    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    def store(
        self,
        user_id: int,
        content: str,
        category: str = "general",
        importance: float = 0.5,
    ) -> MemoryEntry:
        session = self._db.session()
        try:
            entry = MemoryEntry(
                user_id=user_id,
                content=content,
                category=category,
                importance=importance,
            )
            session.add(entry)
            session.commit()
            session.refresh(entry)
            log.debug("memory_stored", user_id=user_id, category=category)
            return entry
        finally:
            session.close()

    def search(
        self,
        user_id: int,
        query: str,
        category: str | None = None,
        limit: int = 10,
    ) -> list[MemoryEntry]:
        """Keyword search over memories (semantic search when embeddings are available)."""
        session = self._db.session()
        try:
            q = session.query(MemoryEntry).filter(MemoryEntry.user_id == user_id)
            if category:
                q = q.filter(MemoryEntry.category == category)
            q = q.filter(MemoryEntry.content.ilike(f"%{query}%"))
            q = q.order_by(MemoryEntry.importance.desc(), MemoryEntry.created_at.desc())
            results = list(q.limit(limit).all())
            for r in results:
                r.access_count += 1
                r.last_accessed = datetime.utcnow()
            session.commit()
            return results
        finally:
            session.close()

    def get_recent(self, user_id: int, limit: int = 20) -> list[MemoryEntry]:
        session = self._db.session()
        try:
            return list(
                session.query(MemoryEntry)
                .filter(MemoryEntry.user_id == user_id)
                .order_by(MemoryEntry.created_at.desc())
                .limit(limit)
                .all()
            )
        finally:
            session.close()

    def delete(self, memory_id: int) -> None:
        session = self._db.session()
        try:
            entry = session.get(MemoryEntry, memory_id)
            if entry:
                session.delete(entry)
                session.commit()
        finally:
            session.close()
