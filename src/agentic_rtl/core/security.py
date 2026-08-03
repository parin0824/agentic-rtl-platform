from __future__ import annotations

from pathlib import Path


class WorkspacePolicy:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def resolve_read(self, relative: str) -> Path:
        return self._resolve(relative)

    def resolve_write(self, relative: str, allowed_roots: tuple[str, ...]) -> Path:
        path = self._resolve(relative)
        roots = [(self.root / item).resolve() for item in allowed_roots]
        if not any(path == root or root in path.parents for root in roots):
            raise PermissionError(f"Write denied outside allowed roots: {relative}")
        return path

    def _resolve(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PermissionError(f"Path escapes workspace: {relative}")
        return candidate
