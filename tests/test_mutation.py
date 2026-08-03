from pathlib import Path

from agentic_rtl.tools.mutation import MUTATIONS, create_mutants


def test_mutants_are_generated(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    mutants = create_mutants(root / "rtl/async_fifo/async_fifo.sv", tmp_path)
    assert len(mutants) == len(MUTATIONS)
    assert all(path.exists() for path in mutants)
