# JARVIS AI — Plugin Development Guide

## Overview

JARVIS AI supports plugins that extend its functionality. Plugins can add
new commands, respond to events, provide custom widgets, and integrate with
external services.

## Quick Start

Create a new plugin in the `plugins/` directory:

```
plugins/
  my_plugin/
    __init__.py
```

### Minimal Plugin

```python
from jarvis.plugins.sdk import JarvisPlugin, PluginMetadata, command

class MyPlugin(JarvisPlugin):
    @classmethod
    def metadata(cls) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            description="My custom plugin",
            author="Your Name",
        )

    def activate(self) -> None:
        self.logger.info("Plugin activated!")

    def deactivate(self) -> None:
        self.logger.info("Plugin deactivated!")

    @command(name="greet", description="Say hello")
    def greet(self, name: str = "World") -> str:
        return f"Hello, {name}!"
```

## Plugin SDK

### `JarvisPlugin` Base Class

All plugins must extend `JarvisPlugin` and implement:

- `metadata()` — returns `PluginMetadata` with name, version, etc.
- `activate()` — called when the plugin is loaded
- `deactivate()` — called when the plugin is unloaded

### Decorators

- `@command(name, description)` — registers a callable command
- `@on_event(event_type)` — subscribes to EventBus events

### PluginMetadata Fields

| Field | Type | Required |
|-------|------|----------|
| `name` | str | Yes |
| `version` | str | Yes |
| `description` | str | Yes |
| `author` | str | Yes |
| `requires` | list[str] | No |
| `tags` | list[str] | No |

## Hot Reload

Plugins can be reloaded at runtime via the Settings > Plugins page or
programmatically:

```python
plugin_manager.reload("my_plugin")
```

## Settings Schema

Plugins can expose configurable settings:

```python
def get_settings_schema(self) -> dict:
    return {
        "api_key": {
            "type": "string",
            "description": "API key for external service",
        },
        "enabled": {
            "type": "bool",
            "default": True,
        },
    }
```

## Event Handling

```python
from jarvis.core.events import Event

class MyPlugin(JarvisPlugin):
    @on_event(Event.USER_LOGGED_IN)
    def on_login(self, **kwargs):
        user = kwargs.get("user")
        self.logger.info(f"User logged in: {user}")
```
