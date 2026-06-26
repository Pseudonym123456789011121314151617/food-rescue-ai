"""Glassmorphism panel widget with blur and glow effects."""

from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QWidget


class GlassPanel(QFrame):
    """A translucent panel with rounded corners, subtle border glow, and drop shadow."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        radius: int = 16,
        bg_opacity: int = 200,
        border_color: str = "#00d4ff",
        border_opacity: float = 0.15,
        glow: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("glassPanel")
        self._radius = radius
        self._bg_opacity = bg_opacity
        self._border_color = QColor(border_color)
        self._border_opacity = border_opacity

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(12)

        if glow:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 4)
            shadow_color = QColor(border_color)
            shadow_color.setAlpha(40)
            shadow.setColor(shadow_color)
            self.setGraphicsEffect(shadow)

    @property
    def content_layout(self) -> QVBoxLayout:
        return self._layout

    def paintEvent(self, event: object) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)

        # Background fill
        bg = QColor(15, 20, 32, self._bg_opacity)
        painter.fillPath(path, QBrush(bg))

        # Subtle gradient highlight at the top
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0, QColor(255, 255, 255, 8))
        gradient.setColorAt(0.3, QColor(255, 255, 255, 0))
        painter.fillPath(path, QBrush(gradient))

        # Border
        border_col = QColor(self._border_color)
        border_col.setAlphaF(self._border_opacity)
        painter.setPen(QPen(border_col, 1.0))
        painter.drawPath(path)

        painter.end()
