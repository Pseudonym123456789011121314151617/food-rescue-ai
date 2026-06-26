"""Calendar page with events, reminders, and scheduling."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCalendarWidget,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton
from jarvis.ui.components.glass_panel import GlassPanel


class CalendarPage(QWidget):
    """Calendar with event management and reminders."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Calendar")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()

        add_btn = AnimatedButton("+ New Event", primary=True)
        header.addWidget(add_btn)

        reminder_btn = AnimatedButton("Reminders")
        header.addWidget(reminder_btn)
        layout.addLayout(header)

        # Content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Calendar widget
        cal_panel = GlassPanel(radius=12, bg_opacity=160)
        self._calendar = QCalendarWidget()
        self._calendar.setGridVisible(True)
        self._calendar.setStyleSheet("background-color: transparent; color: #e0e6f0;")
        cal_panel.content_layout.addWidget(self._calendar)
        splitter.addWidget(cal_panel)

        # Events list
        events_panel = QWidget()
        events_layout = QVBoxLayout(events_panel)
        events_layout.setContentsMargins(0, 0, 0, 0)

        events_header = QLabel("UPCOMING EVENTS")
        events_header.setObjectName("statLabel")
        events_header.setStyleSheet("font-size: 11px; letter-spacing: 2px; color: #8892a8;")
        events_layout.addWidget(events_header)

        self._events_list = QListWidget()
        self._events_list.setStyleSheet(
            "background-color: rgba(15, 20, 40, 0.7); "
            "border: 1px solid rgba(0, 212, 255, 0.1); border-radius: 8px;"
        )
        self._events_list.addItems(
            [
                "📅 Team Meeting — 10:00 AM",
                "📞 Client Call — 2:00 PM",
                "🎂 Birthday Reminder — Tomorrow",
                "🏃 Gym Session — 6:00 PM",
            ]
        )
        events_layout.addWidget(self._events_list)

        splitter.addWidget(events_panel)
        splitter.setSizes([500, 300])

        layout.addWidget(splitter, 1)
