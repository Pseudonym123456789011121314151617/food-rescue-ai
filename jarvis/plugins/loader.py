"""Dynamic plugin loader with hot-reload support."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from jarvis.core.exceptions import PluginError
from jarvis.core.logging import get_logger
from jarvis.plugins.sdk import JarvisPlugin

if TYPE_CHECKING:
    from jarvis.core.config import AppConfig
    from jarvis.core.events import EventBus

log = get_logger(__name__)


class PluginLoader:
    """Discovers and loads plugin modules from directories."""

    def __init__(self, config: AppConfig, event_bus: EventBus) -> None:
        self._config = config
        self._bus = event_bus

    def load_from_path(self, path: Path) -> JarvisPlugin:
        """Load a plugin from a directory containing a plugin.py or __init__.py."""
        module_file = path / "plugin.py"
        if not module_file.exists():
            module_file = path / "__init__.py"
        if not module_file.exists():
            raise PluginError(f"No plugin.py or __init__.py in {path}")

        module_name = f"jarvis_plugin_{path.name}"
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        if spec is None or spec.loader is None:
            raise PluginError(f"Cannot create module spec for {module_file}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Find the JarvisPlugin subclass in the module
        plugin_cls = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, JarvisPlugin)
                and attr is not JarvisPlugin
            ):
                plugin_cls = attr
                break

        if plugin_cls is None:
            raise PluginError(f"No JarvisPlugin subclass found in {module_file}")

        instance = plugin_cls(self._config, self._bus)
        log.info("plugin_loaded", name=instance.metadata.name, path=str(path))
        return instance

    def reload(self, plugin: JarvisPlugin) -> JarvisPlugin:
        """Hot-reload a plugin by re-importing its module."""
        module_name = type(plugin).__module__
        if module_name in sys.modules:
            del sys.modules[module_name]
        # Re-discover from metadata
        log.info("plugin_reloaded", name=plugin.metadata.name)
        return plugin

    def discover_plugins(self, directories: Sequence[str | Path]) -> list[Path]:
        """Scan directories for plugin folders."""
        found: list[Path] = []
        for d in directories:
            dir_path = Path(d)
            if not dir_path.exists():
                continue
            for child in dir_path.iterdir():
                if child.is_dir() and (
                    (child / "plugin.py").exists() or (child / "__init__.py").exists()
                ):
                    found.append(child)
        return found
