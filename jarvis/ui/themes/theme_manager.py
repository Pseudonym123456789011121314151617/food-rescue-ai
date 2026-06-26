"""Theme manager: loads and applies visual themes application-wide."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

from jarvis.ui.themes.cyberpunk import CYBERPUNK_PALETTE, CYBERPUNK_QSS
from jarvis.ui.themes.dark_futuristic import DARK_FUTURISTIC_PALETTE, DARK_FUTURISTIC_QSS

if TYPE_CHECKING:
    from jarvis.core.config import AppConfig


THEMES: dict[str, tuple[str, dict[str, str]]] = {
    "dark_futuristic": (DARK_FUTURISTIC_QSS, DARK_FUTURISTIC_PALETTE),
    "cyberpunk": (CYBERPUNK_QSS, CYBERPUNK_PALETTE),
}


class ThemeManager:
    """Manages application themes and dynamic style switching."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._current_theme = config.ui.theme
        self._accent_color = config.ui.accent_color

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @property
    def accent_color(self) -> str:
        return self._accent_color

    @property
    def available_themes(self) -> list[str]:
        return list(THEMES.keys())

    def apply(self, app: QApplication) -> None:
        """Apply the current theme to the entire application."""
        qss, palette_dict = THEMES.get(self._current_theme, THEMES["dark_futuristic"])

        # Replace accent color placeholder
        qss = qss.replace("{{ACCENT}}", self._accent_color)

        app.setStyleSheet(qss)
        self._apply_palette(app, palette_dict)

        font = QFont("Segoe UI", self._config.ui.font_size)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        app.setFont(font)

    def switch_theme(self, theme_name: str, app: QApplication | None = None) -> None:
        """Switch to a different theme."""
        if theme_name not in THEMES:
            return
        self._current_theme = theme_name
        if app:
            self.apply(app)

    def set_accent_color(self, color: str, app: QApplication | None = None) -> None:
        self._accent_color = color
        if app:
            self.apply(app)

    @staticmethod
    def _apply_palette(app: QApplication, palette_dict: dict[str, str]) -> None:
        palette = QPalette()
        role_map = {
            "window": QPalette.ColorRole.Window,
            "window_text": QPalette.ColorRole.WindowText,
            "base": QPalette.ColorRole.Base,
            "alternate_base": QPalette.ColorRole.AlternateBase,
            "text": QPalette.ColorRole.Text,
            "button": QPalette.ColorRole.Button,
            "button_text": QPalette.ColorRole.ButtonText,
            "highlight": QPalette.ColorRole.Highlight,
            "highlight_text": QPalette.ColorRole.HighlightedText,
            "tooltip_base": QPalette.ColorRole.ToolTipBase,
            "tooltip_text": QPalette.ColorRole.ToolTipText,
        }
        for key, role in role_map.items():
            if key in palette_dict:
                palette.setColor(role, QColor(palette_dict[key]))
        app.setPalette(palette)
