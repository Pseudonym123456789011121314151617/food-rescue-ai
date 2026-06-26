"""AI chat panel with streaming responses and voice visualization."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton
from jarvis.ui.components.avatar import AIAvatar
from jarvis.ui.components.glass_panel import GlassPanel

if TYPE_CHECKING:
    from jarvis.core.events import EventBus


class ChatBubble(GlassPanel):
    """Single chat message bubble."""

    def __init__(
        self,
        text: str,
        is_user: bool,
        parent: QWidget | None = None,
    ) -> None:
        border = "#00d4ff" if not is_user else "#4a5568"
        super().__init__(parent, radius=12, bg_opacity=160 if is_user else 180, border_color=border)

        layout = self.content_layout
        layout.setContentsMargins(12, 8, 12, 8)

        role_label = QLabel("You" if is_user else "JARVIS")
        role_label.setStyleSheet(
            f"font-size: 11px; font-weight: 600; color: {'#8892a8' if is_user else '#00d4ff'};"
        )
        layout.addWidget(role_label)

        msg = QLabel(text)
        msg.setWordWrap(True)
        msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        msg.setStyleSheet("font-size: 14px; color: #e0e6f0;")
        layout.addWidget(msg)


class ChatPanel(QWidget):
    """Complete chat interface with message history and input."""

    message_sent = Signal(str)

    def __init__(self, event_bus: EventBus, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._bus = event_bus

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = GlassPanel(radius=0, bg_opacity=200, glow=False)
        header_layout = header.content_layout
        header_layout.setContentsMargins(16, 8, 16, 8)
        h_inner = QHBoxLayout()

        self._avatar = AIAvatar(size=48)
        h_inner.addWidget(self._avatar)

        title_area = QVBoxLayout()
        title = QLabel("JARVIS AI")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #00d4ff;")
        title_area.addWidget(title)
        status = QLabel("Online • Ready")
        status.setObjectName("subtitleLabel")
        title_area.addWidget(status)
        h_inner.addLayout(title_area)
        h_inner.addStretch()

        new_chat_btn = AnimatedButton("New Chat")
        new_chat_btn.clicked.connect(self._new_chat)
        h_inner.addWidget(new_chat_btn)

        header_layout.addLayout(h_inner)
        layout.addWidget(header)

        # Message area
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self._scroll.setStyleSheet("background: transparent;")

        self._messages_container = QWidget()
        self._messages_layout = QVBoxLayout(self._messages_container)
        self._messages_layout.setContentsMargins(16, 16, 16, 16)
        self._messages_layout.setSpacing(12)
        self._messages_layout.addStretch()

        self._scroll.setWidget(self._messages_container)
        layout.addWidget(self._scroll, 1)

        # Input area
        input_panel = GlassPanel(radius=0, bg_opacity=220, glow=False)
        input_layout = input_panel.content_layout
        input_layout.setContentsMargins(16, 8, 16, 8)

        input_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Type a message or say 'Hey Jarvis'...")
        self._input.setStyleSheet("padding: 14px; font-size: 15px;")
        self._input.returnPressed.connect(self._send)
        input_row.addWidget(self._input, 1)

        self._send_btn = AnimatedButton("Send", primary=True)
        self._send_btn.clicked.connect(self._send)
        input_row.addWidget(self._send_btn)

        self._voice_btn = AnimatedButton("🎤")
        self._voice_btn.setFixedWidth(48)
        input_row.addWidget(self._voice_btn)

        input_layout.addLayout(input_row)
        layout.addWidget(input_panel)

    def add_user_message(self, text: str) -> None:
        bubble = ChatBubble(text, is_user=True)
        self._messages_layout.insertWidget(self._messages_layout.count() - 1, bubble)
        self._scroll_to_bottom()

    def add_assistant_message(self, text: str) -> None:
        bubble = ChatBubble(text, is_user=False)
        self._messages_layout.insertWidget(self._messages_layout.count() - 1, bubble)
        self._scroll_to_bottom()

    def _send(self) -> None:
        text = self._input.text().strip()
        if not text:
            return
        self.add_user_message(text)
        self._input.clear()
        self.message_sent.emit(text)

    def _new_chat(self) -> None:
        # Remove all bubbles
        while self._messages_layout.count() > 1:
            item = self._messages_layout.takeAt(0)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.deleteLater()

    def _scroll_to_bottom(self) -> None:
        vbar = self._scroll.verticalScrollBar()
        vbar.setValue(vbar.maximum())
