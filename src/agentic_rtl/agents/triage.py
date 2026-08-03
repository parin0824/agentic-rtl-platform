from __future__ import annotations

from dataclasses import dataclass

from agentic_rtl.agents.base import Agent


@dataclass(frozen=True)
class TriageRequest:
    return_code: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class TriageDecision:
    classification: str
    evidence: str
    owner: str


class FailureTriageAgent(Agent[TriageRequest, TriageDecision]):
    name = "failure_triage_agent"

    def run(self, request: TriageRequest) -> TriageDecision:
        text = f"{request.stdout}\n{request.stderr}".lower()
        if request.return_code == 127 or "not found" in text:
            return TriageDecision("TOOL_FAILURE", text[-1000:], "environment")
        if "timeout" in text:
            return TriageDecision("TIMEOUT", text[-1000:], "simulation_agent")
        if "assert" in text or "mismatch" in text:
            return TriageDecision("RTL_OR_REFERENCE_BUG", text[-1000:], "rtl_review_agent")
        if "syntax" in text or "compile" in text:
            return TriageDecision("COMPILE_ERROR", text[-1000:], "rtl_generation_agent")
        return TriageDecision("UNCLASSIFIED", text[-1000:], "human_review")
