from pathlib import Path

from agentic_rtl.agents.specification import SpecificationAgent


def test_specification_loads() -> None:
    root = Path(__file__).resolve().parents[1]
    specification = SpecificationAgent().run(root / "specs/async_fifo.json")
    assert specification.module_name == "async_fifo"
    assert len(specification.requirements) == 8
