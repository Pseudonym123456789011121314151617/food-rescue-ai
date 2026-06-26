"""Live digital clock widget."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel, QWidget

from jarvis.ui.components.glass_panel import GlassPanel


class ClockWidget(GlassPanel):
    """Futuristic digital clock with date display."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=16, bg_opacity=180)
        self.setFixedHeight(130)

        layout = self.content_layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._time_label = QLabel("")
        self._time_label.setObjectName("statValue")
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._time_label.setStyleSheet("font-size: 42px; font-weight: 300; letter-spacing: 4px;")
        layout.addWidget(self._time_label)

        self._date_label = QLabel("")
        self._date_label.setObjectName("subtitleLabel")
        self._date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._date_label)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        self._timer.start(1000)
        self._update()

    def _update(self) -> None:
        now = datetime.now()
        self._time_label.setText(now.strftime("%H:%M:%S"))
        self._date_label.setText(now.strftime("%A, %B %d, %Y"))
