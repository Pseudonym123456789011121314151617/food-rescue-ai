"""JARVIS AI entry point."""

from __future__ import annotations

import sys


def main() -> int:
    """Launch JARVIS AI application."""
    from jarvis.app import JarvisApplication

    app = JarvisApplication(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
