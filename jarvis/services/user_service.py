"""User account management service."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger
from jarvis.core.security import hash_pin, verify_pin
from jarvis.models.settings import UserSettings
from jarvis.models.user import User, UserRole

if TYPE_CHECKING:
    from jarvis.core.database import DatabaseManager

log = get_logger(__name__)


class UserService:
    """CRUD and query operations for user accounts."""

    def __init__(self, db: DatabaseManager, event_bus: EventBus) -> None:
        self._db = db
        self._bus = event_bus

    def create_user(
        self,
        username: str,
        display_name: str,
        role: UserRole = UserRole.USER,
        pin: str | None = None,
        password: str | None = None,
    ) -> User:
        """Create a new user account with optional PIN / password."""
        session = self._db.session()
        try:
            user = User(username=username, display_name=display_name, role=role)
            if pin:
                pin_hash, salt = hash_pin(pin)
                user.pin_hash = pin_hash
                user.pin_salt = salt
            if password:
                pw_hash, salt = hash_pin(password)
                user.password_hash = pw_hash
                user.password_salt = salt

            user.settings = UserSettings(data_json="{}")
            session.add(user)
            session.commit()
            session.refresh(user)
            log.info("user_created", username=username, role=role.value)
            return user
        finally:
            session.close()

    def get_all_users(self) -> list[User]:
        """Return all active user accounts."""
        session = self._db.session()
        try:
            return list(session.query(User).filter(User.is_active.is_(True)).all())
        finally:
            session.close()

    def get_user_by_id(self, user_id: int) -> User | None:
        session = self._db.session()
        try:
            return session.get(User, user_id)
        finally:
            session.close()

    def get_user_by_username(self, username: str) -> User | None:
        session = self._db.session()
        try:
            return session.query(User).filter(User.username == username).first()
        finally:
            session.close()

    def verify_pin(self, user: User, pin: str) -> bool:
        """Check a user's PIN."""
        if not user.pin_hash or not user.pin_salt:
            return False
        return verify_pin(pin, user.pin_hash, user.pin_salt)

    def verify_password(self, user: User, password: str) -> bool:
        """Check a user's password."""
        if not user.password_hash or not user.password_salt:
            return False
        return verify_pin(password, user.password_hash, user.password_salt)

    def update_face_encoding(self, user_id: int, encoding: bytes) -> None:
        """Store a face encoding for a user."""
        session = self._db.session()
        try:
            user = session.get(User, user_id)
            if user:
                user.face_encoding = encoding
                session.commit()
                log.info("face_encoding_updated", user_id=user_id)
        finally:
            session.close()

    def record_failed_login(self, user: User) -> bool:
        """Increment failed login counter. Returns True if account is now locked."""
        session = self._db.session()
        try:
            db_user = session.get(User, user.id)
            if not db_user:
                return False
            db_user.login_attempts += 1
            from datetime import timedelta

            from jarvis.core.constants import LOCKOUT_DURATION_SECONDS, MAX_LOGIN_ATTEMPTS

            locked = db_user.login_attempts >= MAX_LOGIN_ATTEMPTS
            if locked:
                db_user.locked_until = datetime.utcnow() + timedelta(
                    seconds=LOCKOUT_DURATION_SECONDS
                )
                self._bus.emit(Event.ACCOUNT_LOCKED, user_id=db_user.id)
            session.commit()
            return locked
        finally:
            session.close()

    def reset_login_attempts(self, user_id: int) -> None:
        session = self._db.session()
        try:
            user = session.get(User, user_id)
            if user:
                user.login_attempts = 0
                user.locked_until = None
                session.commit()
        finally:
            session.close()

    def is_locked(self, user: User) -> bool:
        """Check whether the account is currently locked out."""
        if user.locked_until is None:
            return False
        return datetime.utcnow() < user.locked_until

    def seed_defaults(self) -> None:
        """Create default accounts if the database is empty."""
        if self.get_all_users():
            return
        defaults = [
            ("andreas", "Andreas", UserRole.ADMIN, "1234"),
            ("guest", "Guest", UserRole.GUEST, "0000"),
            ("family", "Family", UserRole.FAMILY, "5678"),
            ("admin", "Admin", UserRole.ADMIN, "9999"),
        ]
        for uname, dname, role, pin in defaults:
            self.create_user(uname, dname, role, pin=pin)
        log.info("default_users_seeded", count=len(defaults))
