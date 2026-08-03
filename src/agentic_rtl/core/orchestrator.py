from __future__ import annotations

from pathlib import Path

from agentic_rtl.agents.rtl_generation import RtlGenerationAgent, RtlGenerationRequest
from agentic_rtl.agents.rtl_review import RtlReviewAgent, RtlReviewRequest
from agentic_rtl.agents.specification import SpecificationAgent
from agentic_rtl.agents.verification import VerificationAgent, VerificationRequest
from agentic_rtl.core.io import save_model
from agentic_rtl.core.models import ProjectRecord, WorkflowState


class Orchestrator:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()

    def prepare(self, execute_tools: bool = True) -> ProjectRecord:
        specification_path = self.workspace / "specs/async_fifo.json"
        specification = SpecificationAgent().run(specification_path)
        generated_rtl = self.workspace / "workspaces/async_fifo/generated_rtl/async_fifo.sv"
        verification_dir = self.workspace / "workspaces/async_fifo/verification"
        record = ProjectRecord(
            project_id=specification.project_id,
            specification_path=specification_path,
            rtl_path=generated_rtl,
            verification_path=verification_dir,
        )
        RtlGenerationAgent().run(
            RtlGenerationRequest(
                specification=specification,
                template_path=self.workspace / "rtl/async_fifo/async_fifo.sv",
                output_path=generated_rtl,
            )
        )
        record.transition(WorkflowState.RTL_GENERATED)
        review = RtlReviewAgent().run(
            RtlReviewRequest(
                specification=specification,
                rtl_path=generated_rtl,
                workspace=self.workspace,
                execute_tools=execute_tools,
            )
        )
        record.open_issues = review.issues
        record.evidence["rtl_review"] = review.model_dump(mode="json")
        if review.status != "PASS":
            record.transition(WorkflowState.RTL_REVIEW_FAILED)
            save_model(self.workspace / "reports/project_record.json", record)
            return record
        record.transition(WorkflowState.RTL_REVIEW_PASSED)
        VerificationAgent().run(
            VerificationRequest(
                specification=specification,
                source_dir=self.workspace / "verification/cocotb",
                output_dir=verification_dir,
            )
        )
        record.transition(WorkflowState.VERIFICATION_READY)
        save_model(self.workspace / "reports/project_record.json", record)
        return record
