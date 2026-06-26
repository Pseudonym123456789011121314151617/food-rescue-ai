"""Async helpers for bridging Qt's event loop and asyncio."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Callable, Coroutine
from concurrent.futures import Future
from typing import Any, TypeVar

T = TypeVar("T")


class AsyncRunner:
    """Runs asyncio coroutines from synchronous Qt code."""

    def __init__(self) -> None:
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the background event loop."""
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=5)

    def run(self, coro: Coroutine[Any, Any, T]) -> Future[T]:
        """Schedule a coroutine and return a Future."""
        assert self._loop is not None, "Call start() first"
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def run_sync(self, coro: Coroutine[Any, Any, T], timeout: float = 30.0) -> T:
        """Schedule a coroutine and block until it completes."""
        future = self.run(coro)
        return future.result(timeout=timeout)

    def _run_loop(self) -> None:
        assert self._loop is not None
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()


def run_in_thread(func: Callable[..., T], *args: Any, **kwargs: Any) -> threading.Thread:
    """Run *func* in a daemon thread."""
    t = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    t.start()
    return t
