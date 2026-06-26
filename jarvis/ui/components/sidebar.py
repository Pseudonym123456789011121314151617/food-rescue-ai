"""Animated collapsible sidebar with navigation items."""

from __future__ import annotations

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from jarvis.core.constants import SIDEBAR_COLLAPSED_WIDTH, SIDEBAR_WIDTH


class SidebarItem:
    """Describes a sidebar navigation entry."""

    def __init__(self, key: str, label: str, icon_text: str = "") -> None:
        self.key = key
        self.label = label
        self.icon_text = icon_text or label[0].upper()


class Sidebar(QFrame):
    """Collapsible sidebar with animated width transitions."""

    navigation_changed = Signal(str)

    # Default navigation items
    DEFAULT_ITEMS: list[SidebarItem] = [
        SidebarItem("dashboard", "Dashboard", "D"),
        SidebarItem("chat", "AI Chat", "C"),
        SidebarItem("files", "File Manager", "F"),
        SidebarItem("terminal", "Terminal", "T"),
        SidebarItem("notes", "Notes", "N"),
        SidebarItem("calendar", "Calendar", "E"),
        SidebarItem("browser", "Browser", "B"),
        SidebarItem("music", "Music", "M"),
        SidebarItem("camera", "Camera", "V"),
        SidebarItem("settings", "Settings", "S"),
    ]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        self.setMinimumHeight(400)

        self._expanded = True
        self._active_key = "dashboard"
        self._buttons: dict[str, QPushButton] = {}

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 16, 8, 16)
        self._layout.setSpacing(4)

        # Brand header
        self._brand = QLabel("JARVIS AI")
        self._brand.setObjectName("titleLabel")
        self._brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._brand.setStyleSheet("font-size: 18px; padding: 12px 0;")
        self._layout.addWidget(self._brand)

        # Navigation buttons
        for item in self.DEFAULT_ITEMS:
            btn = QPushButton(f"  {item.icon_text}   {item.label}")
            btn.setCheckable(True)
            btn.setChecked(item.key == self._active_key)
            btn.clicked.connect(lambda checked, k=item.key: self._on_nav_click(k))
            self._buttons[item.key] = btn
            self._layout.addWidget(btn)

        self._layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # Collapse button
        self._collapse_btn = QPushButton("  ◀  Collapse")
        self._collapse_btn.clicked.connect(self.toggle_collapse)
        self._layout.addWidget(self._collapse_btn)

        # Width animation
        self._width_anim = QPropertyAnimation(self, b"fixedWidth")
        self._width_anim.setDuration(300)
        self._width_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _on_nav_click(self, key: str) -> None:
        self._active_key = key
        for k, btn in self._buttons.items():
            btn.setChecked(k == key)
            btn.setProperty("active", k == key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.navigation_changed.emit(key)

    def toggle_collapse(self) -> None:
        self._expanded = not self._expanded
        target = SIDEBAR_WIDTH if self._expanded else SIDEBAR_COLLAPSED_WIDTH
        self._width_anim.setStartValue(self.width())
        self._width_anim.setEndValue(target)
        self._width_anim.start()

        if self._expanded:
            self._brand.setText("JARVIS AI")
            self._collapse_btn.setText("  ◀  Collapse")
            for item in self.DEFAULT_ITEMS:
                self._buttons[item.key].setText(f"  {item.icon_text}   {item.label}")
        else:
            self._brand.setText("J")
            self._collapse_btn.setText("  ▶")
            for item in self.DEFAULT_ITEMS:
                self._buttons[item.key].setText(f"  {item.icon_text}")

    @property
    def active_key(self) -> str:
        return self._active_key

    def set_active(self, key: str) -> None:
        self._on_nav_click(key)
