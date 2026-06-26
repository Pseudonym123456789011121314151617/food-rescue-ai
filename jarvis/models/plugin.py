"""Plugin registry model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from jarvis.core.database import Base


class PluginRecord(Base):
    __tablename__ = "plugins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    version: Mapped[str] = mapped_column(String(32), default="0.0.1")
    description: Mapped[str] = mapped_column(Text, default="")
    author: Mapped[str] = mapped_column(String(128), default="")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    entry_point: Mapped[str] = mapped_column(String(256), nullable=False)
    installed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
