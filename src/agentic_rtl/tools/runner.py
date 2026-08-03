from __future__ import annotations

import subprocess
import time
from pathlib import Path

from agentic_rtl.core.models import ToolResult


class CommandRunner:
    def __init__(self, workspace: Path, timeout_seconds: int = 120) -> None:
        self.workspace = workspace.resolve()
        self.timeout_seconds = timeout_seconds

    def run(self, tool: str, command: list[str], cwd: Path | None = None) -> ToolResult:
        working_dir = (cwd or self.workspace).resolve()
        if working_dir != self.workspace and self.workspace not in working_dir.parents:
            raise PermissionError("Command working directory must remain inside the workspace")
        started = time.monotonic()
        try:
            process = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            return ToolResult(
                tool=tool,
                command=command,
                return_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
                duration_seconds=time.monotonic() - started,
            )
        except FileNotFoundError as exc:
            return ToolResult(
                tool=tool,
                command=command,
                return_code=127,
                stdout="",
                stderr=str(exc),
                duration_seconds=time.monotonic() - started,
            )
        except subprocess.TimeoutExpired as exc:
            return ToolResult(
                tool=tool,
                command=command,
                return_code=124,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "Command timed out",
                duration_seconds=time.monotonic() - started,
            )
