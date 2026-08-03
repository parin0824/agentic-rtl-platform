from pathlib import Path

import pytest

from agentic_rtl.core.security import WorkspacePolicy


def test_workspace_rejects_escape(tmp_path: Path) -> None:
    policy = WorkspacePolicy(tmp_path)
    with pytest.raises(PermissionError):
        policy.resolve_read("../outside.txt")


def test_workspace_limits_writes(tmp_path: Path) -> None:
    policy = WorkspacePolicy(tmp_path)
    accepted = policy.resolve_write("workspaces/run/output.txt", ("workspaces",))
    assert accepted == (tmp_path / "workspaces/run/output.txt").resolve()
    with pytest.raises(PermissionError):
        policy.resolve_write("specs/spec.json", ("workspaces",))
