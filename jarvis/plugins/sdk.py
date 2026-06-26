"""Plugin SDK — base class and decorators for plugin authors."""

from __future__ import annotations

import abc
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from jarvis.core.config import AppConfig
    from jarvis.core.events import EventBus


@dataclass
class PluginMetadata:
    """Describes a plugin for the registry."""

    name: str
    version: str = "0.0.1"
    description: str = ""
    author: str = ""
    homepage: str = ""
    dependencies: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)


class JarvisPlugin(abc.ABC):
    """Base class every JARVIS plugin must extend."""

    metadata: PluginMetadata = PluginMetadata(name="unnamed")

    def __init__(self, config: AppConfig, event_bus: EventBus) -> None:
        self.config = config
        self.event_bus = event_bus

    @abc.abstractmethod
    def activate(self) -> None:
        """Called when the plugin is loaded and enabled."""

    @abc.abstractmethod
    def deactivate(self) -> None:
        """Called when the plugin is unloaded or disabled."""

    def get_settings_schema(self) -> dict[str, Any]:
        """Return a JSON-schema-like dict describing plugin settings."""
        return {}

    def get_commands(self) -> list[dict[str, str]]:
        """Return a list of AI-callable commands this plugin provides."""
        return []

    def get_widgets(self) -> list[Any]:
        """Return QWidget instances to embed in the dashboard."""
        return []


def command(name: str, description: str = "") -> Callable[..., Any]:
    """Decorator to register a method as an AI-callable command."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._jarvis_command = {"name": name, "description": description}  # type: ignore[attr-defined]
        return func

    return decorator


def on_event(event_name: str) -> Callable[..., Any]:
    """Decorator to subscribe a method to an event."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func._jarvis_event = event_name  # type: ignore[attr-defined]
        return func

    return decorator
