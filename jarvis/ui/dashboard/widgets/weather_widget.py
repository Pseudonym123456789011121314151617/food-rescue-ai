"""Weather widget (mock data — ready for API integration)."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from jarvis.ui.components.glass_panel import GlassPanel


class WeatherWidget(GlassPanel):
    """Current weather conditions display."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=16, bg_opacity=180)
        self.setFixedHeight(130)

        layout = self.content_layout

        header = QLabel("WEATHER")
        header.setObjectName("statLabel")
        header.setStyleSheet("font-size: 11px; letter-spacing: 2px; color: #8892a8;")
        layout.addWidget(header)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Temperature
        temp_layout = QVBoxLayout()
        self._temp = QLabel("22°C")
        self._temp.setObjectName("statValue")
        self._temp.setStyleSheet("font-size: 36px;")
        temp_layout.addWidget(self._temp)

        self._condition = QLabel("Partly Cloudy")
        self._condition.setObjectName("subtitleLabel")
        temp_layout.addWidget(self._condition)

        content_layout.addLayout(temp_layout)
        content_layout.addStretch()

        # Details
        details_layout = QVBoxLayout()
        self._humidity = QLabel("Humidity: 65%")
        self._humidity.setObjectName("subtitleLabel")
        details_layout.addWidget(self._humidity)

        self._wind = QLabel("Wind: 12 km/h")
        self._wind.setObjectName("subtitleLabel")
        details_layout.addWidget(self._wind)

        content_layout.addLayout(details_layout)
        layout.addWidget(content)

    def update_weather(
        self,
        temp: str,
        condition: str,
        humidity: str,
        wind: str,
    ) -> None:
        self._temp.setText(temp)
        self._condition.setText(condition)
        self._humidity.setText(f"Humidity: {humidity}")
        self._wind.setText(f"Wind: {wind}")
