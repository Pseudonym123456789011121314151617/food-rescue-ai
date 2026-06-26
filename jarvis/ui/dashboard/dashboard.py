"""Main dashboard page assembling all widgets."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.glass_panel import GlassPanel
from jarvis.ui.dashboard.widgets.clock_widget import ClockWidget
from jarvis.ui.dashboard.widgets.system_widget import SystemWidget
from jarvis.ui.dashboard.widgets.tasks_widget import TasksWidget
from jarvis.ui.dashboard.widgets.weather_widget import WeatherWidget


class QuickStatCard(GlassPanel):
    """Small stat card for the dashboard header row."""

    def __init__(
        self,
        label: str,
        value: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent, radius=12, bg_opacity=160)
        self.setFixedHeight(90)

        layout = self.content_layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        val = QLabel(value)
        val.setObjectName("statValue")
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(val)

        lbl = QLabel(label)
        lbl.setObjectName("statLabel")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        self._value_label = val

    def set_value(self, value: str) -> None:
        self._value_label.setText(value)


class Dashboard(QWidget):
    """Main dashboard with grid-arranged widgets."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        greeting = QLabel("Good morning, User")
        greeting.setObjectName("titleLabel")
        greeting.setStyleSheet("font-size: 28px;")
        header_layout.addWidget(greeting)

        subtitle = QLabel("Here's your daily briefing")
        subtitle.setObjectName("subtitleLabel")
        header_layout.addWidget(subtitle)

        layout.addWidget(header_widget)

        # Widget grid
        grid = QGridLayout()
        grid.setSpacing(16)

        # Row 0: Clock + Weather + AI Avatar
        self._clock = ClockWidget()
        grid.addWidget(self._clock, 0, 0, 1, 2)

        self._weather = WeatherWidget()
        grid.addWidget(self._weather, 0, 2, 1, 2)

        # Row 1: System Monitor + Tasks
        self._system = SystemWidget()
        grid.addWidget(self._system, 1, 0, 2, 2)

        self._tasks = TasksWidget()
        grid.addWidget(self._tasks, 1, 2, 2, 2)

        # Row 3: Quick stats
        stats = [
            ("42", "NOTIFICATIONS"),
            ("7", "REMINDERS"),
            ("128", "FILES"),
            ("3", "PLUGINS"),
        ]
        for i, (val, lbl) in enumerate(stats):
            card = QuickStatCard(lbl, val)
            grid.addWidget(card, 3, i)

        layout.addLayout(grid)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def set_user_name(self, name: str) -> None:
        """Update the greeting text."""
        # Find and update greeting label
        pass
