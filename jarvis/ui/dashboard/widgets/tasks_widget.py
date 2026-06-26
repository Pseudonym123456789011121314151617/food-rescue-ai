"""Tasks / to-do list widget."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.glass_panel import GlassPanel


class TaskItem(QWidget):
    """Single task row with checkbox and delete button."""

    removed = Signal(object)

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self._checkbox = QCheckBox(text)
        layout.addWidget(self._checkbox, 1)

        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setStyleSheet(
            "border: none; color: #ff3b30; font-size: 14px; border-radius: 12px;"
        )
        delete_btn.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(delete_btn)


class TasksWidget(GlassPanel):
    """To-do list dashboard widget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=16, bg_opacity=180)

        layout = self.content_layout
        layout.setSpacing(8)

        header = QLabel("TASKS")
        header.setObjectName("statLabel")
        header.setStyleSheet("font-size: 11px; letter-spacing: 2px; color: #8892a8;")
        layout.addWidget(header)

        # Add task input
        input_row = QWidget()
        input_layout = QHBoxLayout(input_row)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Add a task...")
        self._input.returnPressed.connect(self._add_task)
        input_layout.addWidget(self._input, 1)

        add_btn = QPushButton("+")
        add_btn.setFixedSize(36, 36)
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self._add_task)
        input_layout.addWidget(add_btn)

        layout.addWidget(input_row)

        # Task list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self._task_container = QWidget()
        self._task_layout = QVBoxLayout(self._task_container)
        self._task_layout.setContentsMargins(0, 0, 0, 0)
        self._task_layout.setSpacing(4)
        self._task_layout.addStretch()

        scroll.setWidget(self._task_container)
        layout.addWidget(scroll)

    def _add_task(self) -> None:
        text = self._input.text().strip()
        if not text:
            return
        item = TaskItem(text)
        item.removed.connect(self._remove_task)
        self._task_layout.insertWidget(self._task_layout.count() - 1, item)
        self._input.clear()

    def _remove_task(self, item: object) -> None:
        assert isinstance(item, QWidget)
        item.deleteLater()
