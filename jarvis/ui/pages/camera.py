"""Camera page with live webcam, face detection, QR scanning, OCR."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from jarvis.ui.components.animated_button import AnimatedButton
from jarvis.ui.components.glass_panel import GlassPanel

try:
    import cv2

    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class CameraPage(QWidget):
    """Camera page with live feed and detection overlays."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._capture: Any = None
        self._timer: QTimer | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Camera")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()

        self._toggle_btn = AnimatedButton("Start Camera", primary=True)
        self._toggle_btn.clicked.connect(self._toggle_camera)
        header.addWidget(self._toggle_btn)

        self._snap_btn = AnimatedButton("📷 Snapshot")
        header.addWidget(self._snap_btn)

        self._qr_btn = AnimatedButton("QR Scan")
        header.addWidget(self._qr_btn)

        self._ocr_btn = AnimatedButton("OCR")
        header.addWidget(self._ocr_btn)

        layout.addLayout(header)

        # Video display
        self._video_label = QLabel("Camera feed will appear here")
        self._video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._video_label.setMinimumSize(640, 480)
        self._video_label.setStyleSheet(
            "background-color: rgba(10, 15, 30, 0.8); "
            "border: 1px solid rgba(0, 212, 255, 0.2); "
            "border-radius: 12px; color: #8892a8; font-size: 16px;"
        )
        layout.addWidget(self._video_label, 1)

        # Status bar
        status_panel = GlassPanel(radius=8, bg_opacity=160, glow=False)
        status_layout = status_panel.content_layout
        s_inner = QHBoxLayout()

        self._status = QLabel("Camera: Stopped")
        self._status.setObjectName("subtitleLabel")
        s_inner.addWidget(self._status)

        s_inner.addStretch()

        self._face_count = QLabel("Faces: 0")
        self._face_count.setStyleSheet("color: #00d4ff;")
        s_inner.addWidget(self._face_count)

        status_layout.addLayout(s_inner)
        layout.addWidget(status_panel)

    def _toggle_camera(self) -> None:
        if not HAS_CV2:
            self._status.setText("OpenCV not installed. pip install opencv-python")
            return

        if self._capture is not None:
            self._stop_camera()
        else:
            self._start_camera()

    def _start_camera(self) -> None:
        if not HAS_CV2:
            return
        self._capture = cv2.VideoCapture(0)
        if not self._capture.isOpened():
            self._status.setText("No camera found")
            self._capture = None
            return

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)
        self._timer.start(33)  # ~30 FPS
        self._toggle_btn.setText("Stop Camera")
        self._status.setText("Camera: Running")

    def _stop_camera(self) -> None:
        if self._timer:
            self._timer.stop()
            self._timer = None
        if self._capture:
            self._capture.release()
            self._capture = None
        self._toggle_btn.setText("Start Camera")
        self._status.setText("Camera: Stopped")
        self._video_label.setText("Camera feed will appear here")

    def _update_frame(self) -> None:
        if self._capture is None:
            return
        ret, frame = self._capture.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        scaled = pixmap.scaled(
            self._video_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._video_label.setPixmap(scaled)

    def closeEvent(self, event: object) -> None:
        self._stop_camera()
        super().closeEvent(event)  # type: ignore[arg-type]
