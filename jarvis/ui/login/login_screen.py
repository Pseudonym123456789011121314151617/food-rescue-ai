"""Professional login screen with account selection and face recognition."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton
from jarvis.ui.components.avatar import AIAvatar
from jarvis.ui.components.glass_panel import GlassPanel
from jarvis.ui.components.particle_system import ParticleBackground

if TYPE_CHECKING:
    from jarvis.models.user import User
    from jarvis.services.auth_service import AuthService
    from jarvis.services.user_service import UserService


class AccountCard(GlassPanel):
    """Clickable user account card."""

    clicked = Signal(int)

    def __init__(self, user: User, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=16, bg_opacity=180)
        self._user = user
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(200, 200)

        layout = self.content_layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Avatar circle
        avatar_label = QLabel(user.display_name[0].upper())
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setFixedSize(80, 80)
        avatar_label.setStyleSheet(
            "background-color: rgba(0, 212, 255, 0.15); "
            "border: 2px solid rgba(0, 212, 255, 0.3); "
            "border-radius: 40px; "
            "font-size: 32px; font-weight: bold; color: #00d4ff;"
        )
        layout.addWidget(avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Name
        name_label = QLabel(user.display_name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #e0e6f0;")
        layout.addWidget(name_label)

        # Role
        role_label = QLabel(user.role.value.title())
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_label.setObjectName("subtitleLabel")
        layout.addWidget(role_label)

    def mousePressEvent(self, event: object) -> None:
        self.clicked.emit(self._user.id)


class LoginScreen(QWidget):
    """Full login screen with account selection and authentication."""

    login_success = Signal(int)

    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._auth = auth_service
        self._users = user_service
        self._selected_user: User | None = None

        self._setup_ui()
        self._load_users()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Particle background
        self._particles = ParticleBackground(self)

        # Stacked widget: account selection → authentication
        self._stack = QStackedWidget(self)
        main_layout.addWidget(self._stack)

        # Page 0: Account selection
        self._account_page = QWidget()
        self._setup_account_page()
        self._stack.addWidget(self._account_page)

        # Page 1: PIN / password entry
        self._auth_page = QWidget()
        self._setup_auth_page()
        self._stack.addWidget(self._auth_page)

    def _setup_account_page(self) -> None:
        layout = QVBoxLayout(self._account_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(32)

        # Title
        title = QLabel("Welcome to JARVIS AI")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Select your account to continue")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # AI Avatar
        self._avatar = AIAvatar(size=100)
        layout.addWidget(self._avatar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Account grid
        self._account_grid_widget = QWidget()
        self._account_grid = QGridLayout(self._account_grid_widget)
        self._account_grid.setSpacing(20)
        layout.addWidget(self._account_grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def _setup_auth_page(self) -> None:
        layout = QVBoxLayout(self._auth_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Back button
        back_btn = AnimatedButton("← Back")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # User info
        self._auth_username = QLabel("")
        self._auth_username.setObjectName("titleLabel")
        self._auth_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._auth_username.setStyleSheet("font-size: 22px;")
        layout.addWidget(self._auth_username)

        # Status message
        self._status_label = QLabel("Enter PIN to continue")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setObjectName("subtitleLabel")
        layout.addWidget(self._status_label)

        # PIN entry
        pin_panel = GlassPanel(radius=12, bg_opacity=160)
        pin_layout = QVBoxLayout()

        self._pin_input = QLineEdit()
        self._pin_input.setPlaceholderText("Enter PIN")
        self._pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._pin_input.setMaximumWidth(300)
        self._pin_input.setStyleSheet("font-size: 24px; letter-spacing: 8px; padding: 16px;")
        self._pin_input.returnPressed.connect(self._attempt_pin_login)
        pin_layout.addWidget(self._pin_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self._login_btn = AnimatedButton("Unlock", primary=True)
        self._login_btn.setMaximumWidth(300)
        self._login_btn.clicked.connect(self._attempt_pin_login)
        pin_layout.addWidget(self._login_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        pin_panel.content_layout.addLayout(pin_layout)
        layout.addWidget(pin_panel, alignment=Qt.AlignmentFlag.AlignCenter)

        # Denied message display
        self._denied_label = QLabel("")
        self._denied_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._denied_label.setStyleSheet("color: #ff3b30; font-size: 14px; font-weight: 500;")
        self._denied_label.hide()
        layout.addWidget(self._denied_label)

    def _load_users(self) -> None:
        """Seed defaults and populate account cards."""
        self._users.seed_defaults()
        users = self._users.get_all_users()

        # Clear existing cards
        while self._account_grid.count():
            item = self._account_grid.takeAt(0)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

        # Add account cards in a grid
        cols = min(4, max(2, len(users)))
        for i, user in enumerate(users):
            card = AccountCard(user)
            card.clicked.connect(self._on_account_selected)
            self._account_grid.addWidget(card, i // cols, i % cols)

    def _on_account_selected(self, user_id: int) -> None:
        user = self._users.get_user_by_id(user_id)
        if user is None:
            return
        self._selected_user = user
        self._auth_username.setText(user.display_name)
        self._pin_input.clear()
        self._denied_label.hide()
        self._status_label.setText("Enter PIN to continue")
        self._stack.setCurrentIndex(1)
        self._pin_input.setFocus()

    def _attempt_pin_login(self) -> None:
        if self._selected_user is None:
            return
        pin = self._pin_input.text()
        if not pin:
            return

        if self._auth.authenticate_pin(self._selected_user, pin):
            self._status_label.setText("Access granted!")
            self._status_label.setStyleSheet("color: #00ff88; font-size: 16px; font-weight: 600;")
            self.login_success.emit(self._selected_user.id)
        else:
            msg = self._auth.random_denied_message()
            self._denied_label.setText(msg)
            self._denied_label.show()
            self._pin_input.clear()
            self._pin_input.setFocus()

            if self._users.is_locked(self._selected_user):
                self._status_label.setText("Account locked. Try again later.")
                self._login_btn.setEnabled(False)

    def resizeEvent(self, event: object) -> None:
        super().resizeEvent(event)  # type: ignore[arg-type]
        self._particles.setGeometry(self.rect())
