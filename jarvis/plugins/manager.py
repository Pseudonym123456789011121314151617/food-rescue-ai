"""Plugin lifecycle manager."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from jarvis.core.events import Event, EventBus
from jarvis.core.logging import get_logger
from jarvis.plugins.loader import PluginLoader
from jarvis.plugins.sdk import JarvisPlugin

if TYPE_CHECKING:
    from jarvis.core.config import AppConfig

log = get_logger(__name__)


class PluginManager:
    """Manages plugin discovery, loading, activation, and shutdown."""

    def __init__(self, config: AppConfig, event_bus: EventBus) -> None:
        self._config = config
        self._bus = event_bus
        self._loader = PluginLoader(config, event_bus)
        self._plugins: dict[str, JarvisPlugin] = {}

    @property
    def loaded_plugins(self) -> dict[str, JarvisPlugin]:
        return dict(self._plugins)

    def discover(self) -> list[str]:
        """Scan plugin directories and load all discovered plugins."""
        dirs = [Path(d) for d in self._config.plugin_dirs]
        paths = self._loader.discover_plugins(dirs)
        names: list[str] = []
        for path in paths:
            try:
                plugin = self._loader.load_from_path(path)
                self._plugins[plugin.metadata.name] = plugin
                plugin.activate()
                self._bus.emit(Event.PLUGIN_LOADED, name=plugin.metadata.name)
                names.append(plugin.metadata.name)
            except Exception:
                log.exception("plugin_load_failed", path=str(path))
        log.info("plugins_discovered", count=len(names))
        return names

    def load(self, path: str | Path) -> JarvisPlugin | None:
        """Load and activate a single plugin."""
        try:
            plugin = self._loader.load_from_path(Path(path))
            self._plugins[plugin.metadata.name] = plugin
            plugin.activate()
            self._bus.emit(Event.PLUGIN_LOADED, name=plugin.metadata.name)
            return plugin
        except Exception:
            log.exception("plugin_load_failed", path=str(path))
            return None

    def unload(self, name: str) -> bool:
        """Deactivate and remove a plugin."""
        plugin = self._plugins.pop(name, None)
        if plugin is None:
            return False
        try:
            plugin.deactivate()
        except Exception:
            log.exception("plugin_deactivate_error", name=name)
        self._bus.emit(Event.PLUGIN_UNLOADED, name=name)
        return True

    def unload_all(self) -> None:
        """Deactivate all plugins."""
        for name in list(self._plugins.keys()):
            self.unload(name)

    def get_plugin(self, name: str) -> JarvisPlugin | None:
        return self._plugins.get(name)

    def list_names(self) -> list[str]:
        return list(self._plugins.keys())

    def reload(self, name: str) -> bool:
        """Hot-reload a plugin."""
        plugin = self._plugins.get(name)
        if plugin is None:
            return False
        try:
            plugin.deactivate()
            reloaded = self._loader.reload(plugin)
            reloaded.activate()
            self._plugins[name] = reloaded
            return True
        except Exception:
            log.exception("plugin_reload_failed", name=name)
            return False
