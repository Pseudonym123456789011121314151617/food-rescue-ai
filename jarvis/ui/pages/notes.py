"""Notes page with markdown editing, voice notes, and AI summaries."""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton


class NotesPage(QWidget):
    """Notes editor with list and markdown preview."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Notes")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()

        new_btn = AnimatedButton("+ New Note", primary=True)
        new_btn.clicked.connect(self._new_note)
        header.addWidget(new_btn)

        ai_btn = AnimatedButton("AI Summary")
        header.addWidget(ai_btn)

        voice_btn = AnimatedButton("🎤 Voice Note")
        header.addWidget(voice_btn)

        layout.addLayout(header)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Note list
        list_panel = QWidget()
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(0, 0, 0, 0)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search notes...")
        list_layout.addWidget(self._search)

        self._note_list = QListWidget()
        self._note_list.setStyleSheet(
            "background-color: rgba(15, 20, 40, 0.7); "
            "border: 1px solid rgba(0, 212, 255, 0.1); border-radius: 8px;"
        )
        self._note_list.currentRowChanged.connect(self._on_note_selected)
        list_layout.addWidget(self._note_list)
        splitter.addWidget(list_panel)

        # Editor
        editor_panel = QWidget()
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(0, 0, 0, 0)

        self._title_input = QLineEdit()
        self._title_input.setPlaceholderText("Note title...")
        self._title_input.setStyleSheet("font-size: 18px; font-weight: 600; padding: 8px;")
        editor_layout.addWidget(self._title_input)

        self._editor = QPlainTextEdit()
        self._editor.setPlaceholderText("Write your note here... (Markdown supported)")
        self._editor.setStyleSheet(
            "background-color: rgba(15, 20, 40, 0.5); "
            "border: 1px solid rgba(0, 212, 255, 0.1); "
            "border-radius: 8px; padding: 12px; font-size: 14px;"
        )
        editor_layout.addWidget(self._editor)

        splitter.addWidget(editor_panel)
        splitter.setSizes([250, 600])

        layout.addWidget(splitter, 1)

        # Storage
        self._notes: list[dict[str, str]] = []
        self._current_index: int = -1

        # Default note
        self._new_note()

    def _new_note(self) -> None:
        note = {
            "title": f"Untitled Note ({datetime.now():%H:%M})",
            "content": "",
        }
        self._notes.append(note)
        self._note_list.addItem(note["title"])
        self._note_list.setCurrentRow(len(self._notes) - 1)

    def _on_note_selected(self, index: int) -> None:
        # Save current
        if 0 <= self._current_index < len(self._notes):
            self._notes[self._current_index]["title"] = self._title_input.text()
            self._notes[self._current_index]["content"] = self._editor.toPlainText()

        self._current_index = index
        if 0 <= index < len(self._notes):
            self._title_input.setText(self._notes[index]["title"])
            self._editor.setPlainText(self._notes[index]["content"])
