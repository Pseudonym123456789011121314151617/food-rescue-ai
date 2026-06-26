"""Main JARVIS AI application orchestrator."""

from __future__ import annotations

import signal

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from jarvis.core.config import AppConfig
from jarvis.core.constants import APP_NAME
from jarvis.core.database import DatabaseManager
from jarvis.core.events import EventBus
from jarvis.core.logging import setup_logging
from jarvis.plugins.manager import PluginManager
from jarvis.services.auth_service import AuthService
from jarvis.services.notification_service import NotificationService
from jarvis.services.user_service import UserService
from jarvis.ui.main_window import MainWindow
from jarvis.ui.themes.theme_manager import ThemeManager


class JarvisApplication:
    """Top-level application controller that wires together all subsystems."""

    def __init__(self, argv: list[str] | None = None) -> None:
        self._argv = argv or []
        self._qt_app: QApplication | None = None
        self._main_window: MainWindow | None = None
        self._config: AppConfig | None = None
        self._db: DatabaseManager | None = None
        self._event_bus: EventBus | None = None
        self._theme_manager: ThemeManager | None = None
        self._plugin_manager: PluginManager | None = None
        self._user_service: UserService | None = None
        self._auth_service: AuthService | None = None
        self._notification_service: NotificationService | None = None

    # -- public API ----------------------------------------------------------

    def run(self) -> int:
        """Initialize subsystems and start the Qt event loop."""
        self._init_qt()
        self._init_core()
        self._init_services()
        self._init_plugins()
        self._init_ui()
        self._connect_signals()

        assert self._qt_app is not None
        return self._qt_app.exec()

    def shutdown(self) -> None:
        """Gracefully tear down all subsystems."""
        if self._plugin_manager:
            self._plugin_manager.unload_all()
        if self._db:
            self._db.close()
        if self._qt_app:
            self._qt_app.quit()

    # -- private helpers -----------------------------------------------------

    def _init_qt(self) -> None:
        self._qt_app = QApplication(self._argv)
        self._qt_app.setApplicationName(APP_NAME)
        self._qt_app.setApplicationVersion("1.0.0")
        self._qt_app.setStyle("Fusion")

        signal.signal(signal.SIGINT, lambda *_: self.shutdown())
        timer = QTimer(self._qt_app)
        timer.start(500)
        timer.timeout.connect(lambda: None)

    def _init_core(self) -> None:
        self._config = AppConfig.load()
        setup_logging(self._config.log_level, self._config.log_file)
        self._event_bus = EventBus()
        self._db = DatabaseManager(self._config.database_url)
        self._db.initialize()

    def _init_services(self) -> None:
        assert self._db is not None
        assert self._event_bus is not None
        assert self._config is not None

        self._user_service = UserService(self._db, self._event_bus)
        self._auth_service = AuthService(self._db, self._user_service, self._event_bus)
        self._notification_service = NotificationService(self._event_bus)
        self._theme_manager = ThemeManager(self._config)

    def _init_plugins(self) -> None:
        assert self._config is not None
        assert self._event_bus is not None
        self._plugin_manager = PluginManager(self._config, self._event_bus)
        self._plugin_manager.discover()

    def _init_ui(self) -> None:
        assert self._qt_app is not None
        assert self._config is not None
        assert self._event_bus is not None
        assert self._theme_manager is not None
        assert self._auth_service is not None
        assert self._user_service is not None
        assert self._db is not None
        assert self._notification_service is not None
        assert self._plugin_manager is not None

        self._theme_manager.apply(self._qt_app)

        self._main_window = MainWindow(
            config=self._config,
            event_bus=self._event_bus,
            theme_manager=self._theme_manager,
            auth_service=self._auth_service,
            user_service=self._user_service,
            db=self._db,
            notification_service=self._notification_service,
            plugin_manager=self._plugin_manager,
        )
        self._main_window.show()

    def _connect_signals(self) -> None:
        assert self._qt_app is not None
        self._qt_app.aboutToQuit.connect(self.shutdown)
