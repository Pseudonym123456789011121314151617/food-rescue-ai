"""Semantic search over memory using embedding similarity."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import numpy as np

from jarvis.core.logging import get_logger
from jarvis.models.memory import MemoryEntry

if TYPE_CHECKING:
    from jarvis.ai.providers.base import AIProvider
    from jarvis.core.database import DatabaseManager

log = get_logger(__name__)


class SemanticSearch:
    """Vector-similarity search over stored memories."""

    def __init__(self, db: DatabaseManager, provider: AIProvider) -> None:
        self._db = db
        self._provider = provider

    async def index_memory(self, memory: MemoryEntry) -> None:
        """Generate and store an embedding for a memory entry."""
        try:
            embedding = await self._provider.get_embedding(memory.content)
            session = self._db.session()
            try:
                entry = session.get(MemoryEntry, memory.id)
                if entry:
                    entry.embedding = json.dumps(embedding)
                    session.commit()
            finally:
                session.close()
        except NotImplementedError:
            log.debug("embeddings_not_supported", provider=self._provider.name)
        except Exception:
            log.exception("embedding_error")

    async def search(
        self,
        user_id: int,
        query: str,
        limit: int = 5,
    ) -> list[tuple[MemoryEntry, float]]:
        """Return memories ranked by cosine similarity to *query*."""
        try:
            query_embedding = np.array(await self._provider.get_embedding(query), dtype=np.float32)
        except NotImplementedError:
            return []

        session = self._db.session()
        try:
            entries = (
                session.query(MemoryEntry)
                .filter(
                    MemoryEntry.user_id == user_id,
                    MemoryEntry.embedding.isnot(None),
                )
                .all()
            )
            scored: list[tuple[MemoryEntry, float]] = []
            for entry in entries:
                if not entry.embedding:
                    continue
                vec = np.array(json.loads(entry.embedding), dtype=np.float32)
                similarity = float(
                    np.dot(query_embedding, vec)
                    / (np.linalg.norm(query_embedding) * np.linalg.norm(vec) + 1e-10)
                )
                scored.append((entry, similarity))
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[:limit]
        finally:
            session.close()
