"""Main application window assembling sidebar, dock, content pages, and particle background."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.chat.chat_panel import ChatPanel
from jarvis.ui.components.dock import Dock
from jarvis.ui.components.particle_system import ParticleBackground
from jarvis.ui.components.sidebar import Sidebar
from jarvis.ui.dashboard.dashboard import Dashboard
from jarvis.ui.pages.browser import Browser
from jarvis.ui.pages.calendar_page import CalendarPage
from jarvis.ui.pages.camera import CameraPage
from jarvis.ui.pages.file_manager import FileManager
from jarvis.ui.pages.music import MusicPlayer
from jarvis.ui.pages.notes import NotesPage
from jarvis.ui.pages.terminal import Terminal

if TYPE_CHECKING:
    from jarvis.core.config import AppConfig
    from jarvis.core.database import DatabaseManager
    from jarvis.core.events import EventBus
    from jarvis.plugins.manager import PluginManager
    from jarvis.services.auth_service import AuthService
    from jarvis.services.notification_service import NotificationService
    from jarvis.services.user_service import UserService
    from jarvis.ui.themes.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    """Primary application window with sidebar navigation and stacked content."""

    def __init__(
        self,
        config: AppConfig,
        theme_manager: ThemeManager,
        event_bus: EventBus,
        auth_service: AuthService | None = None,
        user_service: UserService | None = None,
        db: DatabaseManager | None = None,
        notification_service: NotificationService | None = None,
        plugin_manager: PluginManager | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._theme = theme_manager
        self._bus = event_bus
        self._auth_svc = auth_service
        self._user_svc = user_service
        self._db = db
        self._notification_svc = notification_service
        self._plugin_mgr = plugin_manager

        self.setWindowTitle("JARVIS AI")
        self.setMinimumSize(1200, 800)
        self.resize(1440, 900)

        central = QWidget()
        self.setCentralWidget(central)

        # Root layout with particle background overlay
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Main content area: sidebar + stacked pages
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        self._sidebar = Sidebar()
        self._sidebar.navigation_changed.connect(self._on_nav)
        content_layout.addWidget(self._sidebar)

        # Stacked content
        self._stack = QStackedWidget()
        content_layout.addWidget(self._stack, 1)

        # Build pages
        self._pages: dict[str, QWidget] = {}
        self._build_pages()

        root.addWidget(content_area, 1)

        # Dock bar
        self._dock = Dock()
        root.addWidget(self._dock)

        # Particle background behind everything
        self._particles = ParticleBackground(central)
        self._particles.lower()

        # Navigate to dashboard
        self._sidebar.set_active("dashboard")

    def _build_pages(self) -> None:
        """Create all content pages and add to stack."""
        self._dashboard = Dashboard()
        self._add_page("Dashboard", self._dashboard)

        self._chat = ChatPanel(self._bus)
        self._add_page("Chat", self._chat)

        self._file_manager = FileManager()
        self._add_page("Files", self._file_manager)

        self._terminal = Terminal()
        self._add_page("Terminal", self._terminal)

        self._notes = NotesPage()
        self._add_page("Notes", self._notes)

        self._calendar = CalendarPage()
        self._add_page("Calendar", self._calendar)

        self._browser = Browser()
        self._add_page("Browser", self._browser)

        self._music = MusicPlayer()
        self._add_page("Music", self._music)

        self._camera = CameraPage()
        self._add_page("Camera", self._camera)

        # Settings built lazily (needs config/theme refs)
        from jarvis.ui.settings.settings_page import SettingsPage

        self._settings = SettingsPage(self._config, self._theme, self._bus)
        self._add_page("Settings", self._settings)

    def _add_page(self, name: str, widget: QWidget) -> None:
        self._pages[name] = widget
        self._stack.addWidget(widget)

    def _on_nav(self, page_name: str) -> None:
        widget = self._pages.get(page_name)
        if widget:
            self._stack.setCurrentWidget(widget)

    def set_user(self, user_name: str) -> None:
        """Update UI after successful login."""
        self._dashboard.set_user_name(user_name)

    def resizeEvent(self, event: object) -> None:
        super().resizeEvent(event)  # type: ignore[arg-type]
        self._particles.setGeometry(self.centralWidget().rect())

    def toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
