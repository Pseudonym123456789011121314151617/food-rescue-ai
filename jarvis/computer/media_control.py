"""Media playback control: Spotify, system media keys."""

from __future__ import annotations

import subprocess
import sys

from jarvis.core.logging import get_logger

log = get_logger(__name__)


class MediaController:
    """Control media playback and Spotify."""

    def play_pause(self) -> None:
        """Toggle play/pause for the active media player."""
        if sys.platform == "win32":
            self._send_media_key("play_pause")
        elif sys.platform == "linux":
            subprocess.run(  # noqa: S603, S607
                [
                    "dbus-send",
                    "--print-reply",
                    "--dest=org.mpris.MediaPlayer2.spotify",
                    "/org/mpris/MediaPlayer2",
                    "org.mpris.MediaPlayer2.Player.PlayPause",
                ],
                check=False,
                capture_output=True,
            )

    def next_track(self) -> None:
        if sys.platform == "linux":
            subprocess.run(  # noqa: S603, S607
                [
                    "dbus-send",
                    "--print-reply",
                    "--dest=org.mpris.MediaPlayer2.spotify",
                    "/org/mpris/MediaPlayer2",
                    "org.mpris.MediaPlayer2.Player.Next",
                ],
                check=False,
                capture_output=True,
            )

    def previous_track(self) -> None:
        if sys.platform == "linux":
            subprocess.run(  # noqa: S603, S607
                [
                    "dbus-send",
                    "--print-reply",
                    "--dest=org.mpris.MediaPlayer2.spotify",
                    "/org/mpris/MediaPlayer2",
                    "org.mpris.MediaPlayer2.Player.Previous",
                ],
                check=False,
                capture_output=True,
            )

    def open_spotify(self) -> bool:
        """Launch the Spotify application."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(  # noqa: S603, S607
                    ["start", "spotify:"],
                    shell=True,  # noqa: S602
                )
            elif sys.platform == "linux":
                subprocess.Popen(["spotify"])  # noqa: S603, S607
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", "Spotify"])  # noqa: S603, S607
            return True
        except Exception:
            log.exception("spotify_launch_failed")
            return False

    @staticmethod
    def _send_media_key(key: str) -> None:
        """Send media key on Windows via PowerShell."""
        if sys.platform == "win32":
            key_map = {
                "play_pause": "0xB3",
                "next": "0xB0",
                "previous": "0xB1",
                "volume_up": "0xAF",
                "volume_down": "0xAE",
                "mute": "0xAD",
            }
            vk = key_map.get(key)
            if vk:
                subprocess.run(  # noqa: S603
                    [
                        "powershell",
                        "-Command",
                        f"$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys('{vk}')",
                    ],
                    check=False,
                    capture_output=True,
                )
