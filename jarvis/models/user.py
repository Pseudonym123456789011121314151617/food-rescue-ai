"""User account and permission models."""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jarvis.core.database import Base


class UserRole(enum.StrEnum):
    ADMIN = "admin"
    USER = "user"
    FAMILY = "family"
    GUEST = "guest"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    avatar_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    pin_hash: Mapped[str | None] = mapped_column(String(256), nullable=True)
    pin_salt: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(256), nullable=True)
    password_salt: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    face_encoding: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    voice_profile: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    permissions: Mapped[list[UserPermission]] = relationship(
        "UserPermission", back_populates="user", cascade="all, delete-orphan"
    )
    settings: Mapped[UserSettings | None] = relationship(
        "UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    conversations: Mapped[list[Conversation]] = relationship(
        "Conversation", back_populates="user", cascade="all, delete-orphan"
    )
    memories: Mapped[list[MemoryEntry]] = relationship(
        "MemoryEntry", back_populates="user", cascade="all, delete-orphan"
    )


class UserPermission(Base):
    __tablename__ = "user_permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    permission: Mapped[str] = mapped_column(String(128), nullable=False)
    granted: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped[User] = relationship("User", back_populates="permissions")


# Avoid circular import — referenced by string in relationship()
from jarvis.models.chat import Conversation  # noqa: E402, F811
from jarvis.models.memory import MemoryEntry  # noqa: E402, F811
from jarvis.models.settings import UserSettings  # noqa: E402, F811
