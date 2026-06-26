"""AI function-calling registry for tool use."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from jarvis.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class FunctionDef:
    """Describes a callable function the AI can invoke."""

    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., Any]
    required: list[str] = field(default_factory=list)


class FunctionRegistry:
    """Registry of functions the AI model can call."""

    def __init__(self) -> None:
        self._functions: dict[str, FunctionDef] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        handler: Callable[..., Any],
        required: list[str] | None = None,
    ) -> None:
        """Register a function for AI tool use."""
        self._functions[name] = FunctionDef(
            name=name,
            description=description,
            parameters=parameters,
            handler=handler,
            required=required or [],
        )
        log.debug("function_registered", name=name)

    def unregister(self, name: str) -> None:
        self._functions.pop(name, None)

    def get(self, name: str) -> FunctionDef | None:
        return self._functions.get(name)

    async def execute(self, name: str, arguments: str) -> str:
        """Parse JSON arguments and call the handler."""
        func = self._functions.get(name)
        if not func:
            return json.dumps({"error": f"Unknown function: {name}"})
        try:
            args = json.loads(arguments) if arguments else {}
            result = func.handler(**args)
            if hasattr(result, "__await__"):
                result = await result
            return json.dumps({"result": str(result)})
        except Exception as exc:
            log.exception("function_execution_error", name=name)
            return json.dumps({"error": str(exc)})

    def to_openai_schema(self) -> list[dict[str, object]]:
        """Export functions in OpenAI function-calling format."""
        schemas: list[dict[str, object]] = []
        for f in self._functions.values():
            schemas.append(
                {
                    "name": f.name,
                    "description": f.description,
                    "parameters": {
                        "type": "object",
                        "properties": f.parameters,
                        "required": f.required,
                    },
                }
            )
        return schemas

    def list_names(self) -> list[str]:
        return list(self._functions.keys())
