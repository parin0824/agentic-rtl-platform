from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentic_rtl.agents.base import Agent
from agentic_rtl.core.models import ReviewIssue, ReviewReport, Severity, Specification
from agentic_rtl.tools.eda import EdaTools


@dataclass(frozen=True)
class RtlReviewRequest:
    specification: Specification
    rtl_path: Path
    workspace: Path
    execute_tools: bool = True


class RtlReviewAgent(Agent[RtlReviewRequest, ReviewReport]):
    name = "rtl_review_agent"

    def run(self, request: RtlReviewRequest) -> ReviewReport:
        text = request.rtl_path.read_text(encoding="utf-8")
        issues: list[ReviewIssue] = []
        checks = {
            "module_name": f"module {request.specification.module_name}" in text,
            "gray_conversion": "bin2gray" in text,
            "two_stage_sync": "sync1" in text and "sync2" in text,
            "write_guard": "wr_en && !full" in text,
            "read_guard": "rd_en && !empty" in text,
            "local_full_register": "always_ff @(posedge wr_clk" in text,
            "local_empty_register": "always_ff @(posedge rd_clk" in text,
        }
        requirement_map = {
            "gray_conversion": "FIFO_REQ_006",
            "two_stage_sync": "FIFO_REQ_006",
            "write_guard": "FIFO_REQ_003",
            "read_guard": "FIFO_REQ_005",
            "local_full_register": "FIFO_REQ_008",
            "local_empty_register": "FIFO_REQ_008",
        }
        for check, passed in checks.items():
            if not passed:
                issues.append(
                    ReviewIssue(
                        severity=Severity.HIGH,
                        file=str(request.rtl_path),
                        requirement_id=requirement_map.get(check),
                        description=f"Static review check failed: {check}",
                        evidence=f"Required pattern for {check} was not found",
                    )
                )
        if request.execute_tools:
            tools = EdaTools(request.workspace)
            for result in (
                tools.lint(request.rtl_path, request.specification.module_name),
                tools.synthesize(request.rtl_path, request.specification.module_name),
            ):
                checks[result.tool] = result.passed
                if not result.passed:
                    severity = Severity.MEDIUM if result.return_code == 127 else Severity.HIGH
                    issues.append(
                        ReviewIssue(
                            severity=severity,
                            file=str(request.rtl_path),
                            description=f"{result.tool} did not pass",
                            evidence=(result.stderr or result.stdout)[-2000:],
                            recommended_fix="Install the required tool" if result.return_code == 127 else None,
                        )
                    )
        status = "PASS" if not any(i.severity in {Severity.HIGH, Severity.CRITICAL} for i in issues) else "FAIL"
        return ReviewReport(status=status, issues=issues, checks=checks)
