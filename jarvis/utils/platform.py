"""Platform detection and OS-specific helpers."""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass


@dataclass
class PlatformInfo:
    os_name: str
    os_version: str
    architecture: str
    python_version: str
    hostname: str
    is_windows: bool
    is_linux: bool
    is_macos: bool


def get_platform_info() -> PlatformInfo:
    """Return information about the current platform."""
    return PlatformInfo(
        os_name=platform.system(),
        os_version=platform.version(),
        architecture=platform.machine(),
        python_version=platform.python_version(),
        hostname=platform.node(),
        is_windows=sys.platform == "win32",
        is_linux=sys.platform == "linux",
        is_macos=sys.platform == "darwin",
    )


def get_data_dir_name() -> str:
    """Return the conventional data directory name for the current OS."""
    if sys.platform == "win32":
        return "AppData/Roaming/JARVIS AI"
    if sys.platform == "darwin":
        return "Library/Application Support/JARVIS AI"
    return ".local/share/JARVIS AI"
