"""System monitor widget: CPU, RAM, Disk, GPU, Battery, Network."""

from __future__ import annotations

import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QGridLayout, QLabel, QProgressBar, QVBoxLayout, QWidget

from jarvis.ui.components.glass_panel import GlassPanel


class SystemStatBar(QWidget):
    """Single stat with label + progress bar + value."""

    def __init__(self, label: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        header = QWidget()
        header_layout = QGridLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(label)
        self._label.setObjectName("statLabel")
        header_layout.addWidget(self._label, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._value = QLabel("0%")
        self._value.setStyleSheet("color: #00d4ff; font-weight: 600; font-size: 13px;")
        header_layout.addWidget(self._value, 0, 1, Qt.AlignmentFlag.AlignRight)

        layout.addWidget(header)

        self._bar = QProgressBar()
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(6)
        layout.addWidget(self._bar)

    def set_value(self, percent: float, text: str | None = None) -> None:
        self._bar.setValue(int(percent))
        self._value.setText(text or f"{percent:.1f}%")


class SystemWidget(GlassPanel):
    """System resource monitor dashboard widget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=16, bg_opacity=180)

        layout = self.content_layout
        layout.setSpacing(8)

        title = QLabel("SYSTEM MONITOR")
        title.setObjectName("statLabel")
        title.setStyleSheet("font-size: 11px; letter-spacing: 2px; color: #8892a8;")
        layout.addWidget(title)

        self._cpu = SystemStatBar("CPU")
        self._ram = SystemStatBar("RAM")
        self._disk = SystemStatBar("DISK")
        self._gpu = SystemStatBar("GPU")
        self._battery = SystemStatBar("BATTERY")
        self._network = SystemStatBar("NETWORK")

        for stat in [self._cpu, self._ram, self._disk, self._gpu, self._battery, self._network]:
            layout.addWidget(stat)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        self._timer.start(2000)
        self._update()

    def _update(self) -> None:
        self._cpu.set_value(psutil.cpu_percent(interval=0))
        mem = psutil.virtual_memory()
        self._ram.set_value(
            mem.percent,
            f"{mem.used / (1024**3):.1f} / {mem.total / (1024**3):.1f} GB",
        )
        disk = psutil.disk_usage("/")
        self._disk.set_value(
            disk.percent,
            f"{disk.used / (1024**3):.0f} / {disk.total / (1024**3):.0f} GB",
        )

        # GPU (placeholder)
        self._gpu.set_value(0, "N/A")

        # Battery
        battery = psutil.sensors_battery()
        if battery:
            status = "Charging" if battery.power_plugged else "On Battery"
            self._battery.set_value(battery.percent, f"{battery.percent}% ({status})")
        else:
            self._battery.set_value(0, "No Battery")

        # Network
        net = psutil.net_io_counters()
        sent_mb = net.bytes_sent / (1024 * 1024)
        recv_mb = net.bytes_recv / (1024 * 1024)
        self._network.set_value(0, f"↑{sent_mb:.0f} MB  ↓{recv_mb:.0f} MB")
