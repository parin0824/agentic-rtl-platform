from __future__ import annotations

from pathlib import Path

from agentic_rtl.core.models import ToolResult
from agentic_rtl.tools.runner import CommandRunner


class EdaTools:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.runner = CommandRunner(workspace)

    def lint(self, rtl: Path, top: str) -> ToolResult:
        return self.runner.run(
            "verilator_lint",
            ["verilator", "--lint-only", "--Wall", "--top-module", top, str(rtl)],
        )

    def synthesize(self, rtl: Path, top: str) -> ToolResult:
        script = f"read_verilog -sv {rtl}; hierarchy -top {top}; proc; check"
        return self.runner.run("yosys_check", ["yosys", "-q", "-p", script])

    def regression(self, verification_dir: Path, seed: int) -> ToolResult:
        return self.runner.run(
            "cocotb_regression",
            ["make", "SIM=verilator", f"RANDOM_SEED={seed}"],
            cwd=verification_dir,
        )
