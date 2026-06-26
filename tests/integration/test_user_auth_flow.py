"""Integration tests for user creation and authentication flow."""

from __future__ import annotations

from jarvis.core.database import DatabaseManager
from jarvis.core.events import EventBus
from jarvis.models.user import UserRole
from jarvis.services.auth_service import AuthService
from jarvis.services.user_service import UserService


class TestUserAuthFlow:
    def test_create_user_and_auth_pin(self, db: DatabaseManager, event_bus: EventBus) -> None:
        user_svc = UserService(db, event_bus)
        auth_svc = AuthService(db, user_svc, event_bus)

        user = user_svc.create_user(
            username="testuser",
            display_name="Test User",
            role=UserRole.USER,
            pin="5678",
        )
        assert user.id is not None
        assert user.username == "testuser"

        # Authenticate
        result = auth_svc.authenticate_pin(user, "5678")
        assert result is True

        # Wrong PIN
        result = auth_svc.authenticate_pin(user, "0000")
        assert result is False

    def test_seed_defaults(self, db: DatabaseManager, event_bus: EventBus) -> None:
        user_svc = UserService(db, event_bus)
        user_svc.seed_defaults()

        users = user_svc.get_all_users()
        assert len(users) >= 4

        usernames = [u.username for u in users]
        assert "andreas" in usernames
        assert "guest" in usernames

    def test_lockout(self, db: DatabaseManager, event_bus: EventBus) -> None:
        user_svc = UserService(db, event_bus)
        auth_svc = AuthService(db, user_svc, event_bus)

        user = user_svc.create_user(
            username="locktest",
            display_name="Lock Test",
            role=UserRole.USER,
            pin="1111",
        )

        # Fail 5 times
        for _ in range(5):
            auth_svc.authenticate_pin(user, "9999")

        # Refresh user
        refreshed = user_svc.get_user_by_id(user.id)
        assert refreshed is not None
        assert user_svc.is_locked(refreshed)

    def test_denied_message(self, db: DatabaseManager, event_bus: EventBus) -> None:
        user_svc = UserService(db, event_bus)
        auth_svc = AuthService(db, user_svc, event_bus)
        msg = auth_svc.random_denied_message()
        assert isinstance(msg, str)
        assert len(msg) > 0
