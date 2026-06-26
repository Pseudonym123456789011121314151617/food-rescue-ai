"""Authentication service: face recognition, PIN, password fallbacks."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from jarvis.core.constants import ACCESS_DENIED_RESPONSES
from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

if TYPE_CHECKING:
    from jarvis.core.database import DatabaseManager
    from jarvis.models.user import User
    from jarvis.services.user_service import UserService

log = get_logger(__name__)


class AuthService:
    """Handles multi-factor authentication flow."""

    def __init__(
        self,
        db: DatabaseManager,
        user_service: UserService,
        event_bus: EventBus,
    ) -> None:
        self._db = db
        self._users = user_service
        self._bus = event_bus
        self._current_user: User | None = None

    @property
    def current_user(self) -> User | None:
        return self._current_user

    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None

    def authenticate_face(self, user: User, face_encoding: bytes) -> bool:
        """Compare *face_encoding* against the stored template for *user*."""
        if self._users.is_locked(user):
            log.warning("login_blocked_locked", user=user.username)
            return False

        if user.face_encoding is None:
            log.info("no_face_enrolled", user=user.username)
            return False

        try:
            import numpy as np

            stored = np.frombuffer(user.face_encoding, dtype=np.float32)
            incoming = np.frombuffer(face_encoding, dtype=np.float32)
            if stored.shape != incoming.shape:
                return self._fail(user)
            distance = float(np.linalg.norm(stored - incoming))
            from jarvis.core.constants import FACE_CONFIDENCE_THRESHOLD

            if distance < FACE_CONFIDENCE_THRESHOLD:
                return self._success(user)
            return self._fail(user)
        except Exception:
            log.exception("face_auth_error")
            return self._fail(user)

    def authenticate_pin(self, user: User, pin: str) -> bool:
        """Authenticate via PIN code."""
        if self._users.is_locked(user):
            return False
        if self._users.verify_pin(user, pin):
            return self._success(user)
        return self._fail(user)

    def authenticate_password(self, user: User, password: str) -> bool:
        """Authenticate via password."""
        if self._users.is_locked(user):
            return False
        if self._users.verify_password(user, password):
            return self._success(user)
        return self._fail(user)

    def logout(self) -> None:
        if self._current_user:
            log.info("user_logout", user=self._current_user.username)
            self._bus.emit(Event.USER_LOGOUT, user_id=self._current_user.id)
            self._current_user = None

    @staticmethod
    def random_denied_message() -> str:
        """Return a humorous access-denied quip."""
        return random.choice(ACCESS_DENIED_RESPONSES)

    # -- internal helpers ---

    def _success(self, user: User) -> bool:
        self._current_user = user
        self._users.reset_login_attempts(user.id)
        self._bus.emit(Event.USER_LOGIN, user_id=user.id, username=user.username)
        log.info("login_success", user=user.username)
        return True

    def _fail(self, user: User) -> bool:
        locked = self._users.record_failed_login(user)
        msg = self.random_denied_message()
        self._bus.emit(
            Event.LOGIN_FAILED,
            user_id=user.id,
            message=msg,
            locked=locked,
        )
        log.warning("login_failed", user=user.username, message=msg)
        return False
