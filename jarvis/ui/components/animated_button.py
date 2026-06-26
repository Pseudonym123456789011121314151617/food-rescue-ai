"""Animated button with hover glow and press feedback."""

from __future__ import annotations

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPropertyAnimation,
    QSize,
    Qt,
)
from PySide6.QtGui import QColor, QCursor, QIcon
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget


class AnimatedButton(QPushButton):
    """Button with smooth hover glow animation."""

    def __init__(
        self,
        text: str = "",
        parent: QWidget | None = None,
        *,
        icon: QIcon | None = None,
        accent: str = "#00d4ff",
        primary: bool = False,
    ) -> None:
        super().__init__(text, parent)
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        if primary:
            self.setObjectName("primaryButton")

        self._glow_strength = 0.0
        self._accent = QColor(accent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(0)
        self._shadow.setOffset(0, 0)
        glow_color = QColor(accent)
        glow_color.setAlpha(0)
        self._shadow.setColor(glow_color)
        self.setGraphicsEffect(self._shadow)

        self._anim = QPropertyAnimation(self, b"glowStrength")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _get_glow(self) -> float:
        return self._glow_strength

    def _set_glow(self, value: float) -> None:
        self._glow_strength = value
        glow_color = QColor(self._accent)
        glow_color.setAlpha(int(value * 80))
        self._shadow.setBlurRadius(value * 25)
        self._shadow.setColor(glow_color)

    glowStrength = Property(float, _get_glow, _set_glow)

    def enterEvent(self, event: object) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._glow_strength)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)  # type: ignore[arg-type]

    def leaveEvent(self, event: object) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._glow_strength)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)  # type: ignore[arg-type]
