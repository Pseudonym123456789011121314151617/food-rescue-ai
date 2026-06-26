"""System-level controls: volume, brightness, power, clipboard, screenshot."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import psutil

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class SystemController:
    """Cross-platform system control operations."""

    def __init__(self, event_bus: EventBus) -> None:
        self._bus = event_bus

    # -- Power ---------------------------------------------------------------

    def shutdown(self) -> None:
        """Shut down the computer."""
        log.info("system_shutdown_requested")
        if sys.platform == "win32":
            subprocess.run(["shutdown", "/s", "/t", "5"], check=False)  # noqa: S603, S607
        else:
            subprocess.run(["shutdown", "-h", "now"], check=False)  # noqa: S603, S607

    def restart(self) -> None:
        log.info("system_restart_requested")
        if sys.platform == "win32":
            subprocess.run(["shutdown", "/r", "/t", "5"], check=False)  # noqa: S603, S607
        else:
            subprocess.run(["shutdown", "-r", "now"], check=False)  # noqa: S603, S607

    def sleep(self) -> None:
        log.info("system_sleep_requested")
        if sys.platform == "win32":
            subprocess.run(  # noqa: S603, S607
                ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                check=False,
            )
        elif sys.platform == "linux":
            subprocess.run(["systemctl", "suspend"], check=False)  # noqa: S603, S607
        else:
            subprocess.run(  # noqa: S603, S607
                ["pmset", "sleepnow"], check=False
            )

    # -- Volume --------------------------------------------------------------

    def set_volume(self, level: int) -> None:
        """Set system volume (0-100)."""
        level = max(0, min(100, level))
        if sys.platform == "win32":
            subprocess.run(  # noqa: S603, S607
                [
                    "powershell",
                    "-Command",
                    "(New-Object -ComObject WScript.Shell).SendKeys([char]173)",
                ],
                check=False,
            )
            log.info("volume_set", level=level)
        elif sys.platform == "linux":
            subprocess.run(  # noqa: S603, S607
                ["amixer", "set", "Master", f"{level}%"],
                check=False,
            )

    def get_volume(self) -> int:
        """Get current system volume."""
        if sys.platform == "linux":
            try:
                result = subprocess.run(  # noqa: S603, S607
                    ["amixer", "get", "Master"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                for line in result.stdout.splitlines():
                    if "%" in line:
                        import re

                        match = re.search(r"\[(\d+)%\]", line)
                        if match:
                            return int(match.group(1))
            except Exception:
                pass
        return 50

    # -- Screenshot ----------------------------------------------------------

    def take_screenshot(self, save_dir: str | Path | None = None) -> str | None:
        """Capture the screen and return the file path."""
        try:
            from PIL import ImageGrab

            img = ImageGrab.grab()
            if save_dir is None:
                save_dir = Path.home() / "Pictures" / "Screenshots"
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = save_path / filename
            img.save(filepath)
            self._bus.emit(Event.SCREENSHOT_TAKEN, path=str(filepath))
            log.info("screenshot_taken", path=str(filepath))
            return str(filepath)
        except Exception:
            log.exception("screenshot_failed")
            return None

    # -- Clipboard -----------------------------------------------------------

    @staticmethod
    def get_clipboard() -> str:
        """Get clipboard text content."""
        try:
            from PySide6.QtGui import QGuiApplication

            app = QGuiApplication.instance()
            if isinstance(app, QGuiApplication):
                clipboard = app.clipboard()
                if clipboard:
                    return clipboard.text() or ""
        except Exception:
            pass
        return ""

    @staticmethod
    def set_clipboard(text: str) -> None:
        """Set clipboard text content."""
        try:
            from PySide6.QtGui import QGuiApplication

            app = QGuiApplication.instance()
            if isinstance(app, QGuiApplication):
                clipboard = app.clipboard()
                if clipboard:
                    clipboard.setText(text)
        except Exception:
            log.exception("clipboard_set_failed")

    # -- System info ---------------------------------------------------------

    @staticmethod
    def get_system_info() -> dict[str, object]:
        """Return CPU, RAM, disk, battery, network stats."""
        battery = psutil.sensors_battery()
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "cpu_count": psutil.cpu_count(),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "ram_used_percent": psutil.virtual_memory().percent,
            "disk_total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
            "disk_used_percent": psutil.disk_usage("/").percent,
            "battery_percent": battery.percent if battery else None,
            "battery_plugged": battery.power_plugged if battery else None,
            "net_io": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv,
            },
        }
