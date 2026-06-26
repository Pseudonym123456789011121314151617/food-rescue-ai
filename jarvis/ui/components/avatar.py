"""Animated AI avatar with pulsing ring and voice visualization."""

from __future__ import annotations

import math

from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QConicalGradient, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget


class AIAvatar(QWidget):
    """Animated circular AI avatar with pulsing glow ring."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        size: int = 120,
        color: str = "#00d4ff",
    ) -> None:
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._color = QColor(color)
        self._time = 0.0
        self._speaking = False
        self._voice_level = 0.0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def _tick(self) -> None:
        self._time += 0.03
        self.update()

    def set_speaking(self, speaking: bool) -> None:
        self._speaking = speaking

    def set_voice_level(self, level: float) -> None:
        self._voice_level = max(0.0, min(1.0, level))

    def paintEvent(self, event: object) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = self.width() / 2, self.height() / 2
        base_radius = min(cx, cy) * 0.65

        # Outer pulsing glow
        pulse = 0.5 + 0.5 * math.sin(self._time * 2)
        if self._speaking:
            pulse = 0.5 + 0.5 * self._voice_level
        glow_radius = base_radius * (1.2 + pulse * 0.15)

        glow_gradient = QRadialGradient(cx, cy, glow_radius)
        glow_color = QColor(self._color)
        glow_color.setAlpha(int(30 + pulse * 25))
        glow_gradient.setColorAt(0.6, glow_color)
        glow_transparent = QColor(glow_color)
        glow_transparent.setAlpha(0)
        glow_gradient.setColorAt(1.0, glow_transparent)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow_gradient)
        painter.drawEllipse(
            QRectF(
                cx - glow_radius,
                cy - glow_radius,
                glow_radius * 2,
                glow_radius * 2,
            )
        )

        # Rotating ring
        ring_rect = QRectF(
            cx - base_radius,
            cy - base_radius,
            base_radius * 2,
            base_radius * 2,
        )
        conical = QConicalGradient(cx, cy, math.degrees(self._time * 60) % 360)
        ring_color = QColor(self._color)
        ring_color.setAlpha(180)
        ring_transparent = QColor(self._color)
        ring_transparent.setAlpha(20)
        conical.setColorAt(0.0, ring_color)
        conical.setColorAt(0.5, ring_transparent)
        conical.setColorAt(1.0, ring_color)

        pen = QPen(conical, 3.0)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(ring_rect)

        # Inner core
        core_radius = base_radius * 0.75
        core_gradient = QRadialGradient(cx, cy, core_radius)
        core_inner = QColor(self._color)
        core_inner.setAlpha(int(60 + pulse * 30))
        core_gradient.setColorAt(0, core_inner)
        core_outer = QColor(self._color)
        core_outer.setAlpha(15)
        core_gradient.setColorAt(1, core_outer)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(core_gradient)
        painter.drawEllipse(
            QRectF(
                cx - core_radius,
                cy - core_radius,
                core_radius * 2,
                core_radius * 2,
            )
        )

        # Center text
        painter.setPen(QColor(self._color))
        font = painter.font()
        font.setPixelSize(int(base_radius * 0.5))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "J")

        painter.end()

    def set_color(self, color: str) -> None:
        self._color = QColor(color)
