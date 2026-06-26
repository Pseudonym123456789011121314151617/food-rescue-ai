"""Integrated file manager with search, preview, tags, and drag-drop."""

from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import (
    QFileSystemModel,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSplitter,
    QTextBrowser,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton
from jarvis.ui.components.glass_panel import GlassPanel


class FilePreviewPanel(GlassPanel):
    """Preview panel for selected files."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=12, bg_opacity=160)
        layout = self.content_layout

        self._title = QLabel("No file selected")
        self._title.setObjectName("statLabel")
        self._title.setStyleSheet("font-size: 11px; letter-spacing: 2px; color: #8892a8;")
        layout.addWidget(self._title)

        self._preview = QTextBrowser()
        self._preview.setStyleSheet("background: transparent; border: none; color: #c0c8d8;")
        layout.addWidget(self._preview)

    def show_file(self, path: str) -> None:
        p = Path(path)
        self._title.setText(p.name)

        text_extensions = {
            ".txt",
            ".py",
            ".md",
            ".json",
            ".toml",
            ".yaml",
            ".yml",
            ".cfg",
            ".ini",
            ".csv",
            ".log",
            ".xml",
            ".html",
            ".css",
            ".js",
        }
        if p.suffix.lower() in text_extensions and p.stat().st_size < 100_000:
            try:
                content = p.read_text(encoding="utf-8", errors="replace")
                self._preview.setPlainText(content[:5000])
            except OSError:
                self._preview.setPlainText("Cannot read file.")
        else:
            info = (
                f"Name: {p.name}\nSize: {p.stat().st_size:,} bytes\nType: {p.suffix or 'Unknown'}"
            )
            self._preview.setPlainText(info)


class FileManager(QWidget):
    """Full file manager with tree view, preview, and actions."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("File Manager")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Search files...")
        self._search.setMaximumWidth(300)
        header.addWidget(self._search)
        layout.addLayout(header)

        # Path bar
        self._path_bar = QLabel(str(Path.home()))
        self._path_bar.setObjectName("subtitleLabel")
        layout.addWidget(self._path_bar)

        # Splitter: tree + preview
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # File tree
        self._model = QFileSystemModel()
        self._model.setRootPath(str(Path.home()))

        self._tree = QTreeView()
        self._tree.setModel(self._model)
        self._tree.setRootIndex(self._model.index(str(Path.home())))
        self._tree.setColumnWidth(0, 300)
        self._tree.setAnimated(True)
        self._tree.setSortingEnabled(True)
        self._tree.setAlternatingRowColors(True)
        self._tree.clicked.connect(self._on_file_selected)
        splitter.addWidget(self._tree)

        # Preview
        self._preview = FilePreviewPanel()
        splitter.addWidget(self._preview)
        splitter.setSizes([500, 300])

        layout.addWidget(splitter, 1)

        # Action bar
        actions = QHBoxLayout()
        for label in ["New Folder", "Copy", "Move", "Delete", "Favorites"]:
            btn = AnimatedButton(label)
            actions.addWidget(btn)
        actions.addStretch()
        layout.addLayout(actions)

    def _on_file_selected(self, index: QModelIndex) -> None:
        path = self._model.filePath(index)
        self._path_bar.setText(path)
        if os.path.isfile(path):
            self._preview.show_file(path)
