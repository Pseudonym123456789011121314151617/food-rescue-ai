"""Tests for AI function registry."""

from __future__ import annotations

import asyncio

from jarvis.ai.functions import FunctionRegistry


class TestFunctionRegistry:
    def test_register_and_get(self) -> None:
        registry = FunctionRegistry()

        def greet(name: str) -> str:
            return f"Hello, {name}"

        registry.register(
            name="greet",
            description="Greet someone",
            parameters={"name": {"type": "string"}},
            handler=greet,
            required=["name"],
        )

        fn = registry.get("greet")
        assert fn is not None
        assert fn.name == "greet"

    def test_execute(self) -> None:
        registry = FunctionRegistry()

        def add(a: int, b: int) -> int:
            return a + b

        registry.register(
            name="add",
            description="Add two numbers",
            parameters={
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            },
            handler=add,
        )

        result = asyncio.get_event_loop().run_until_complete(
            registry.execute("add", '{"a": 3, "b": 5}')
        )
        assert "8" in result

    def test_unregister(self) -> None:
        registry = FunctionRegistry()
        registry.register(
            name="test",
            description="test",
            parameters={},
            handler=lambda: None,
        )
        registry.unregister("test")
        assert registry.get("test") is None

    def test_openai_schema(self) -> None:
        registry = FunctionRegistry()
        registry.register(
            name="demo",
            description="A demo function",
            parameters={},
            handler=lambda: None,
        )

        schemas = registry.to_openai_schema()
        assert len(schemas) == 1
        assert schemas[0]["name"] == "demo"
