"""File system operations: search, move, delete, preview."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from jarvis.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class FileInfo:
    path: str
    name: str
    size: int
    is_dir: bool
    modified: float
    extension: str


class FileOperations:
    """Safe, audited file system operations."""

    def search(
        self,
        root: str | Path,
        pattern: str,
        max_results: int = 100,
    ) -> list[FileInfo]:
        """Recursively search for files matching *pattern*."""
        root_path = Path(root)
        results: list[FileInfo] = []
        try:
            for p in root_path.rglob(f"*{pattern}*"):
                if len(results) >= max_results:
                    break
                results.append(self._file_info(p))
        except PermissionError:
            log.warning("search_permission_denied", root=str(root))
        return results

    def list_directory(self, path: str | Path) -> list[FileInfo]:
        """List contents of a directory."""
        dir_path = Path(path)
        if not dir_path.is_dir():
            return []
        results: list[FileInfo] = []
        try:
            for entry in sorted(dir_path.iterdir()):
                results.append(self._file_info(entry))
        except PermissionError:
            log.warning("list_permission_denied", path=str(path))
        return results

    def move(self, source: str | Path, destination: str | Path) -> bool:
        """Move a file or directory."""
        try:
            shutil.move(str(source), str(destination))
            log.info("file_moved", src=str(source), dst=str(destination))
            return True
        except Exception:
            log.exception("move_failed")
            return False

    def copy(self, source: str | Path, destination: str | Path) -> bool:
        """Copy a file or directory."""
        try:
            src = Path(source)
            if src.is_dir():
                shutil.copytree(str(source), str(destination))
            else:
                shutil.copy2(str(source), str(destination))
            return True
        except Exception:
            log.exception("copy_failed")
            return False

    def delete(self, path: str | Path, *, confirm: bool = True) -> bool:
        """Delete a file or directory (requires confirmation by default)."""
        if confirm:
            log.info("delete_requires_confirmation", path=str(path))
        target = Path(path)
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            log.info("file_deleted", path=str(path))
            return True
        except Exception:
            log.exception("delete_failed")
            return False

    def get_info(self, path: str | Path) -> FileInfo | None:
        p = Path(path)
        if not p.exists():
            return None
        return self._file_info(p)

    @staticmethod
    def _file_info(p: Path) -> FileInfo:
        stat = p.stat()
        return FileInfo(
            path=str(p),
            name=p.name,
            size=stat.st_size,
            is_dir=p.is_dir(),
            modified=stat.st_mtime,
            extension=p.suffix,
        )
