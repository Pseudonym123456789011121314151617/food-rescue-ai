"""Bottom dock bar with quick-access icons and status indicators."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from jarvis.core.constants import DOCK_HEIGHT


class Dock(QFrame):
    """Bottom dock with status indicators and quick actions."""

    action_triggered = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("dock")
        self.setFixedHeight(DOCK_HEIGHT)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 4, 16, 4)
        layout.setSpacing(8)

        # Status indicators
        self._status_label = QLabel("JARVIS AI v1.0")
        self._status_label.setObjectName("subtitleLabel")
        layout.addWidget(self._status_label)

        layout.addStretch()

        # Quick action buttons
        actions = [
            ("mic", "Microphone"),
            ("cam", "Camera"),
            ("screenshot", "Screenshot"),
            ("fullscreen", "Fullscreen"),
        ]
        for key, tooltip in actions:
            btn = QPushButton(key[0].upper())
            btn.setToolTip(tooltip)
            btn.setFixedSize(QSize(40, 40))
            btn.setStyleSheet("border-radius: 20px; font-weight: bold;")
            btn.clicked.connect(lambda checked, k=key: self.action_triggered.emit(k))
            layout.addWidget(btn)

        # Notification badge
        self._notif_badge = QLabel("0")
        self._notif_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._notif_badge.setFixedSize(QSize(28, 28))
        self._notif_badge.setStyleSheet(
            "background: #ff3b30; color: white; border-radius: 14px; "
            "font-size: 11px; font-weight: bold;"
        )
        self._notif_badge.hide()
        layout.addWidget(self._notif_badge)

    def set_status(self, text: str) -> None:
        self._status_label.setText(text)

    def set_notification_count(self, count: int) -> None:
        if count > 0:
            self._notif_badge.setText(str(min(count, 99)))
            self._notif_badge.show()
        else:
            self._notif_badge.hide()
