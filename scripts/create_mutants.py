from pathlib import Path

from agentic_rtl.tools.mutation import create_mutants

root = Path(__file__).resolve().parents[1]
for path in create_mutants(root / "rtl/async_fifo/async_fifo.sv", root / "workspaces/mutants"):
    print(path)
