"""Launch, close, and manage desktop applications."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import psutil

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger

log = get_logger(__name__)


class AppController:
    """Launch and manage desktop applications across platforms."""

    def __init__(self, event_bus: EventBus) -> None:
        self._bus = event_bus

    def launch(self, app_name_or_path: str) -> bool:
        """Launch an application by name or path."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(  # noqa: S603
                    ["start", "", app_name_or_path],
                    shell=True,  # noqa: S602
                )
            elif sys.platform == "darwin":
                subprocess.Popen(["open", app_name_or_path])  # noqa: S603
            else:
                subprocess.Popen([app_name_or_path])  # noqa: S603
            self._bus.emit(Event.APP_LAUNCHED, app=app_name_or_path)
            log.info("app_launched", app=app_name_or_path)
            return True
        except Exception:
            log.exception("app_launch_failed", app=app_name_or_path)
            return False

    def close(self, process_name: str) -> bool:
        """Close all processes matching *process_name*."""
        closed = False
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
                try:
                    proc.terminate()
                    closed = True
                except psutil.AccessDenied:
                    log.warning("access_denied_closing", process=process_name)
        return closed

    def list_running(self) -> list[dict[str, object]]:
        """List running processes (name, PID, CPU%, memory%)."""
        procs: list[dict[str, object]] = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                info = proc.info
                procs.append(
                    {
                        "pid": info["pid"],
                        "name": info["name"],
                        "cpu": info["cpu_percent"],
                        "memory": info["memory_percent"],
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return procs

    def is_running(self, process_name: str) -> bool:
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
                return True
        return False

    def launch_steam(self) -> bool:
        """Launch Steam client."""
        if sys.platform == "win32":
            steam_path = Path("C:/Program Files (x86)/Steam/steam.exe")
            if steam_path.exists():
                return self.launch(str(steam_path))
        return self.launch("steam")

    def launch_game(self, game_name: str) -> bool:
        """Attempt to launch a game via Steam or directly."""
        log.info("launching_game", game=game_name)
        return self.launch(game_name)
