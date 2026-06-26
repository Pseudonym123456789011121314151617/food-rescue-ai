"""Browser automation and control."""

from __future__ import annotations

import webbrowser

from jarvis.core.logging import get_logger

log = get_logger(__name__)


class BrowserController:
    """Open URLs, search the web, and manage bookmarks."""

    def __init__(self) -> None:
        self._bookmarks: list[dict[str, str]] = []

    def open_url(self, url: str) -> bool:
        """Open a URL in the default browser."""
        try:
            webbrowser.open(url)
            log.info("url_opened", url=url)
            return True
        except Exception:
            log.exception("url_open_failed")
            return False

    def search(self, query: str, engine: str = "google") -> bool:
        """Search the web using the specified engine."""
        engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
        }
        base = engines.get(engine, engines["google"])
        return self.open_url(f"{base}{query}")

    def add_bookmark(self, title: str, url: str) -> None:
        self._bookmarks.append({"title": title, "url": url})

    def get_bookmarks(self) -> list[dict[str, str]]:
        return list(self._bookmarks)

    def remove_bookmark(self, url: str) -> None:
        self._bookmarks = [b for b in self._bookmarks if b["url"] != url]
