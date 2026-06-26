"""Tests for platform utilities."""

from __future__ import annotations

from jarvis.utils.platform import PlatformInfo, get_platform_info


class TestPlatform:
    def test_get_platform_info(self) -> None:
        info = get_platform_info()
        assert isinstance(info, PlatformInfo)
        assert info.os_name in ("Windows", "Linux", "Darwin")
        assert isinstance(info.python_version, str)
        assert isinstance(info.architecture, str)
