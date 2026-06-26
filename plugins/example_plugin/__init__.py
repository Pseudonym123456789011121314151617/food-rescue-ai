"""Example JARVIS AI plugin demonstrating the SDK."""

from __future__ import annotations

from jarvis.plugins.sdk import JarvisPlugin, PluginMetadata, command, on_event


class ExamplePlugin(JarvisPlugin):
    """A simple example plugin that showcases the JARVIS plugin SDK."""

    @classmethod
    def metadata(cls) -> PluginMetadata:
        return PluginMetadata(
            name="example_plugin",
            version="1.0.0",
            description="Example plugin demonstrating the JARVIS AI SDK",
            author="JARVIS Team",
            requires=[],
            tags=["example", "demo"],
        )

    def activate(self) -> None:
        """Called when the plugin is loaded."""
        self.logger.info("Example plugin activated!")

    def deactivate(self) -> None:
        """Called when the plugin is unloaded."""
        self.logger.info("Example plugin deactivated!")

    @command(name="hello", description="Greet the user")
    def hello_command(self, name: str = "World") -> str:
        """A simple greeting command."""
        return f"Hello, {name}! I'm the Example Plugin."

    @command(name="echo", description="Echo back a message")
    def echo_command(self, message: str) -> str:
        """Echo back whatever the user says."""
        return f"Echo: {message}"

    @command(name="dice", description="Roll a dice")
    def roll_dice(self) -> str:
        """Roll a virtual dice."""
        import random

        result = random.randint(1, 6)
        return f"🎲 You rolled a {result}!"

    def get_settings_schema(self) -> dict[str, object]:
        return {
            "greeting_prefix": {
                "type": "string",
                "default": "Hello",
                "description": "Prefix for greetings",
            },
            "enable_dice": {
                "type": "bool",
                "default": True,
                "description": "Enable the dice command",
            },
        }
