from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentic_rtl.agents.base import Agent
from agentic_rtl.core.models import AuditReport, MutationResult, TestResult


@dataclass(frozen=True)
class AuditRequest:
    mutation_dir: Path
    detector: callable


class VerificationAuditAgent(Agent[AuditRequest, AuditReport]):
    name = "verification_audit_agent"

    def run(self, request: AuditRequest) -> AuditReport:
        results: list[MutationResult] = []
        for mutation in sorted(request.mutation_dir.glob("*.sv")):
            detected, evidence = request.detector(mutation)
            results.append(
                MutationResult(
                    mutation_id=mutation.stem,
                    description=mutation.stem.replace("_", " "),
                    detected=detected,
                    test_results=[
                        TestResult(
                            name="regression",
                            passed=detected,
                            seed=1,
                            duration_seconds=0.0,
                            evidence=evidence,
                        )
                    ],
                )
            )
        detected_count = sum(item.detected for item in results)
        score = detected_count / len(results) if results else 0.0
        return AuditReport(
            total_mutations=len(results),
            detected_mutations=detected_count,
            mutation_score=score,
            results=results,
        )
