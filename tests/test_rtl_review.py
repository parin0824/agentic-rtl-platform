from pathlib import Path

from agentic_rtl.agents.rtl_review import RtlReviewAgent, RtlReviewRequest
from agentic_rtl.agents.specification import SpecificationAgent


def test_static_rtl_review_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    specification = SpecificationAgent().run(root / "specs/async_fifo.json")
    report = RtlReviewAgent().run(
        RtlReviewRequest(
            specification=specification,
            rtl_path=root / "rtl/async_fifo/async_fifo.sv",
            workspace=root,
            execute_tools=False,
        )
    )
    assert report.status == "PASS"
    assert all(report.checks.values())
