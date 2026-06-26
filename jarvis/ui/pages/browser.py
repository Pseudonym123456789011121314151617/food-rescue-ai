"""Mini browser with bookmarks and downloads."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton

# Optional WebEngine — graceful fallback
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView

    HAS_WEBENGINE = True
except ImportError:
    QWebEngineView = None  # type: ignore[assignment,misc]
    HAS_WEBENGINE = False


class Browser(QWidget):
    """Mini browser with address bar and navigation."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._web_view: Any = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Header
        title = QLabel("Browser")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Navigation bar
        nav = QHBoxLayout()

        self._back_btn = AnimatedButton("←")
        self._back_btn.setFixedWidth(40)
        nav.addWidget(self._back_btn)

        self._forward_btn = AnimatedButton("→")
        self._forward_btn.setFixedWidth(40)
        nav.addWidget(self._forward_btn)

        self._refresh_btn = AnimatedButton("⟳")
        self._refresh_btn.setFixedWidth(40)
        nav.addWidget(self._refresh_btn)

        self._url_bar = QLineEdit("https://www.google.com")
        self._url_bar.setStyleSheet("padding: 10px; font-size: 14px;")
        self._url_bar.returnPressed.connect(self._navigate)
        nav.addWidget(self._url_bar, 1)

        go_btn = AnimatedButton("Go", primary=True)
        go_btn.setFixedWidth(60)
        go_btn.clicked.connect(self._navigate)
        nav.addWidget(go_btn)

        layout.addLayout(nav)

        # Web view or fallback
        if HAS_WEBENGINE:
            self._web_view = QWebEngineView()
            self._web_view.setUrl(QUrl("https://www.google.com"))
            self._back_btn.clicked.connect(self._web_view.back)
            self._forward_btn.clicked.connect(self._web_view.forward)
            self._refresh_btn.clicked.connect(self._web_view.reload)
            self._web_view.urlChanged.connect(lambda url: self._url_bar.setText(url.toString()))
            layout.addWidget(self._web_view, 1)
        else:
            fallback = QLabel(
                "Web browser requires PySide6-WebEngine.\n\n"
                "Install with: pip install PySide6-WebEngine"
            )
            fallback.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback.setObjectName("subtitleLabel")
            layout.addWidget(fallback, 1)
            self._web_view = None

    def _navigate(self) -> None:
        url = self._url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if self._web_view:
            self._web_view.setUrl(QUrl(url))
