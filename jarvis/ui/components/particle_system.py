"""Animated particle background for the futuristic UI."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget

from jarvis.core.constants import PARTICLE_COUNT


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    alpha: float
    pulse_phase: float = field(default_factory=lambda: random.uniform(0, 2 * math.pi))


class ParticleBackground(QWidget):
    """Animated floating particle background with connection lines."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        count: int = PARTICLE_COUNT,
        color: str = "#00d4ff",
        connection_distance: float = 120.0,
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._color = QColor(color)
        self._connection_dist = connection_distance
        self._particles: list[Particle] = []
        self._time = 0.0

        for _ in range(count):
            self._particles.append(self._spawn_particle())

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)  # ~60 FPS

    def _spawn_particle(self) -> Particle:
        w = max(self.width(), 800)
        h = max(self.height(), 600)
        return Particle(
            x=random.uniform(0, w),
            y=random.uniform(0, h),
            vx=random.uniform(-0.3, 0.3),
            vy=random.uniform(-0.3, 0.3),
            radius=random.uniform(1.5, 3.5),
            alpha=random.uniform(0.2, 0.6),
        )

    def _tick(self) -> None:
        self._time += 0.02
        w, h = self.width(), self.height()
        for p in self._particles:
            p.x += p.vx
            p.y += p.vy
            # Wrap around
            if p.x < 0:
                p.x = w
            elif p.x > w:
                p.x = 0
            if p.y < 0:
                p.y = h
            elif p.y > h:
                p.y = 0
            # Pulse alpha
            p.alpha = 0.3 + 0.2 * math.sin(self._time + p.pulse_phase)
        self.update()

    def paintEvent(self, event: object) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw connection lines
        pen = QPen()
        for i, p1 in enumerate(self._particles):
            for p2 in self._particles[i + 1 :]:
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < self._connection_dist:
                    alpha = int((1 - dist / self._connection_dist) * 40)
                    line_color = QColor(self._color)
                    line_color.setAlpha(alpha)
                    pen.setColor(line_color)
                    pen.setWidthF(0.5)
                    painter.setPen(pen)
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

        # Draw particles
        for p in self._particles:
            color = QColor(self._color)
            color.setAlphaF(p.alpha)

            gradient = QRadialGradient(p.x, p.y, p.radius * 3)
            gradient.setColorAt(0, color)
            transparent = QColor(color)
            transparent.setAlpha(0)
            gradient.setColorAt(1, transparent)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            painter.drawEllipse(
                QRectF(
                    p.x - p.radius * 3,
                    p.y - p.radius * 3,
                    p.radius * 6,
                    p.radius * 6,
                )
            )

            # Core dot
            painter.setBrush(color)
            painter.drawEllipse(
                QRectF(
                    p.x - p.radius,
                    p.y - p.radius,
                    p.radius * 2,
                    p.radius * 2,
                )
            )

        painter.end()

    def set_color(self, color: str) -> None:
        self._color = QColor(color)

    def set_enabled(self, enabled: bool) -> None:
        if enabled:
            self._timer.start(16)
        else:
            self._timer.stop()
