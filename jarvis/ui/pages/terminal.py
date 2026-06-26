"""Built-in terminal with multiple tabs and syntax highlighting."""

from __future__ import annotations

import subprocess
from pathlib import Path
from threading import Thread

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton


class TerminalTab(QWidget):
    """Single terminal tab with output area and command input."""

    output_received = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.output_received.connect(self._append_output)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Output area
        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setFont(QFont("Consolas", 12))
        self._output.setStyleSheet(
            "background-color: rgba(10, 15, 30, 0.95); color: #00ff88; border: none; padding: 8px;"
        )
        layout.addWidget(self._output, 1)

        # Input line
        input_row = QHBoxLayout()
        prompt = QLabel("❯")
        prompt.setStyleSheet("color: #00d4ff; font-size: 16px; font-weight: bold; padding: 0 8px;")
        input_row.addWidget(prompt)

        self._input = QPlainTextEdit()
        self._input.setMaximumHeight(36)
        self._input.setFont(QFont("Consolas", 12))
        self._input.setStyleSheet(
            "background-color: rgba(10, 15, 30, 0.8); "
            "color: #e0e6f0; border: 1px solid rgba(0,212,255,0.2); "
            "border-radius: 4px; padding: 4px 8px;"
        )
        input_row.addWidget(self._input, 1)

        run_btn = AnimatedButton("Run", primary=True)
        run_btn.setFixedWidth(60)
        run_btn.clicked.connect(self._execute)
        input_row.addWidget(run_btn)

        layout.addLayout(input_row)
        self._cwd = str(Path.home())

    def _execute(self) -> None:
        cmd = self._input.toPlainText().strip()
        if not cmd:
            return
        self._input.clear()
        self._append_output(f"❯ {cmd}\n")

        thread = Thread(target=self._run_command, args=(cmd,), daemon=True)
        thread.start()

    def _run_command(self, cmd: str) -> None:
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self._cwd,
                timeout=30,
            )
            output = result.stdout
            if result.stderr:
                output += result.stderr
            self.output_received.emit(output + "\n")
        except subprocess.TimeoutExpired:
            self.output_received.emit("[Timeout after 30 seconds]\n")
        except Exception as e:
            self.output_received.emit(f"[Error: {e}]\n")

    def _append_output(self, text: str) -> None:
        self._output.moveCursor(QTextCursor.MoveOperation.End)
        self._output.insertPlainText(text)
        self._output.moveCursor(QTextCursor.MoveOperation.End)


class Terminal(QWidget):
    """Multi-tab terminal widget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("Terminal")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()

        new_tab_btn = AnimatedButton("+ New Tab")
        new_tab_btn.clicked.connect(self._add_tab)
        header.addWidget(new_tab_btn)
        layout.addLayout(header)

        self._tabs = QTabWidget()
        self._tabs.setTabsClosable(True)
        self._tabs.tabCloseRequested.connect(self._close_tab)
        layout.addWidget(self._tabs)

        self._add_tab()

    def _add_tab(self) -> None:
        tab = TerminalTab()
        idx = self._tabs.addTab(tab, f"Terminal {self._tabs.count() + 1}")
        self._tabs.setCurrentIndex(idx)

    def _close_tab(self, index: int) -> None:
        if self._tabs.count() > 1:
            self._tabs.removeTab(index)
