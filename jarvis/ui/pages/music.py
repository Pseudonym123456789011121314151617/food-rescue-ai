"""Music player page with playlist, visualizer, and controls."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QProgressBar,
    QSlider,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton
from jarvis.ui.components.glass_panel import GlassPanel


class MusicPlayer(QWidget):
    """Music player with playlist and visualizer."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        title = QLabel("Music Player")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Now playing
        now_playing = GlassPanel(radius=16, bg_opacity=180)
        np_layout = now_playing.content_layout
        np_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Album art placeholder
        art = QLabel("♫")
        art.setAlignment(Qt.AlignmentFlag.AlignCenter)
        art.setStyleSheet(
            "font-size: 64px; color: #00d4ff; "
            "background-color: rgba(0, 212, 255, 0.05); "
            "border-radius: 16px; padding: 32px;"
        )
        art.setFixedSize(200, 200)
        np_layout.addWidget(art, alignment=Qt.AlignmentFlag.AlignCenter)

        song_title = QLabel("No Track Playing")
        song_title.setObjectName("titleLabel")
        song_title.setStyleSheet("font-size: 18px;")
        song_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        np_layout.addWidget(song_title)

        artist = QLabel("Unknown Artist")
        artist.setObjectName("subtitleLabel")
        artist.setAlignment(Qt.AlignmentFlag.AlignCenter)
        np_layout.addWidget(artist)

        # Progress bar
        progress = QProgressBar()
        progress.setTextVisible(False)
        progress.setFixedHeight(4)
        progress.setValue(35)
        np_layout.addWidget(progress)

        time_row = QHBoxLayout()
        time_row.addWidget(QLabel("1:24"))
        time_row.addStretch()
        time_row.addWidget(QLabel("3:45"))
        np_layout.addLayout(time_row)

        # Controls
        controls = QHBoxLayout()
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls.setSpacing(16)

        for icon in ["⏮", "⏪", "▶", "⏩", "⏭"]:
            btn = AnimatedButton(icon)
            btn.setFixedSize(48, 48)
            controls.addWidget(btn)

        np_layout.addLayout(controls)

        # Volume
        vol_row = QHBoxLayout()
        vol_row.addWidget(QLabel("🔊"))
        vol_slider = QSlider(Qt.Orientation.Horizontal)
        vol_slider.setRange(0, 100)
        vol_slider.setValue(75)
        vol_row.addWidget(vol_slider)
        np_layout.addLayout(vol_row)

        splitter.addWidget(now_playing)

        # Playlist
        playlist_panel = QWidget()
        pl_layout = QVBoxLayout(playlist_panel)
        pl_layout.setContentsMargins(0, 0, 0, 0)

        pl_header = QLabel("PLAYLIST")
        pl_header.setObjectName("statLabel")
        pl_header.setStyleSheet("font-size: 11px; letter-spacing: 2px; color: #8892a8;")
        pl_layout.addWidget(pl_header)

        self._playlist = QListWidget()
        self._playlist.setStyleSheet(
            "background-color: rgba(15, 20, 40, 0.7); "
            "border: 1px solid rgba(0, 212, 255, 0.1); border-radius: 8px;"
        )
        self._playlist.addItems(
            [
                "Interstellar — Hans Zimmer",
                "Time — Hans Zimmer",
                "Experience — Ludovico Einaudi",
                "Nuvole Bianche — Ludovico Einaudi",
                "Comptine d'un autre été — Yann Tiersen",
                "River Flows in You — Yiruma",
            ]
        )
        pl_layout.addWidget(self._playlist)

        splitter.addWidget(playlist_panel)
        splitter.setSizes([400, 300])

        layout.addWidget(splitter, 1)
