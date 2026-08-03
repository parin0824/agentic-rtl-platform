from pathlib import Path

from agentic_rtl.core.models import WorkflowState
from agentic_rtl.core.orchestrator import Orchestrator


def test_prepare_without_external_tools() -> None:
    root = Path(__file__).resolve().parents[1]
    record = Orchestrator(root).prepare(execute_tools=False)
    assert record.state == WorkflowState.VERIFICATION_READY
    assert record.rtl_path.exists()
    assert (record.verification_path / "test_async_fifo.py").exists()
