"""Desktop and in-app notification service."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class NotificationLevel(Enum):
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass
class Notification:
    title: str
    message: str
    level: NotificationLevel = NotificationLevel.INFO
    timestamp: datetime = field(default_factory=datetime.utcnow)
    read: bool = False
    action_label: str | None = None
    action_callback: str | None = None


class NotificationService:
    """Manages the notification queue and dispatches UI updates."""

    def __init__(self, event_bus: EventBus) -> None:
        self._bus = event_bus
        self._notifications: list[Notification] = []
        self._max_stored = 200

    @property
    def unread_count(self) -> int:
        return sum(1 for n in self._notifications if not n.read)

    @property
    def all_notifications(self) -> list[Notification]:
        return list(self._notifications)

    def notify(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
    ) -> Notification:
        """Create a notification and emit it on the event bus."""
        n = Notification(title=title, message=message, level=level)
        self._notifications.append(n)
        if len(self._notifications) > self._max_stored:
            self._notifications = self._notifications[-self._max_stored :]
        self._bus.emit(Event.NOTIFICATION, notification=n)
        log.debug("notification", title=title, level=level.name)
        return n

    def mark_read(self, index: int) -> None:
        if 0 <= index < len(self._notifications):
            self._notifications[index].read = True

    def mark_all_read(self) -> None:
        for n in self._notifications:
            n.read = True

    def clear(self) -> None:
        self._notifications.clear()
