from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class WorkflowState(StrEnum):
    SPEC_READY = "SPEC_READY"
    RTL_GENERATED = "RTL_GENERATED"
    RTL_REVIEW_FAILED = "RTL_REVIEW_FAILED"
    RTL_REVIEW_PASSED = "RTL_REVIEW_PASSED"
    VERIFICATION_READY = "VERIFICATION_READY"
    REGRESSION_FAILED = "REGRESSION_FAILED"
    REGRESSION_PASSED = "REGRESSION_PASSED"
    AUDIT_FAILED = "AUDIT_FAILED"
    SIGNOFF_READY = "SIGNOFF_READY"
    COMPLETED = "COMPLETED"


class Severity(StrEnum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Requirement(BaseModel):
    id: str
    text: str


class Specification(BaseModel):
    project_id: str
    module_name: str
    parameters: dict[str, int]
    clocks: list[str]
    resets: list[str]
    requirements: list[Requirement]
    acceptance: dict[str, float | int]


class ReviewIssue(BaseModel):
    severity: Severity
    file: str
    line: int | None = None
    requirement_id: str | None = None
    description: str
    evidence: str
    recommended_fix: str | None = None


class ReviewReport(BaseModel):
    status: str
    issues: list[ReviewIssue] = Field(default_factory=list)
    checks: dict[str, bool] = Field(default_factory=dict)


class ToolResult(BaseModel):
    tool: str
    command: list[str]
    return_code: int
    stdout: str
    stderr: str
    duration_seconds: float

    @property
    def passed(self) -> bool:
        return self.return_code == 0


class TestResult(BaseModel):
    name: str
    passed: bool
    seed: int
    duration_seconds: float
    evidence: str = ""


class MutationResult(BaseModel):
    mutation_id: str
    description: str
    detected: bool
    test_results: list[TestResult] = Field(default_factory=list)


class AuditReport(BaseModel):
    total_mutations: int
    detected_mutations: int
    mutation_score: float
    results: list[MutationResult]


class ProjectRecord(BaseModel):
    project_id: str
    state: WorkflowState = WorkflowState.SPEC_READY
    specification_path: Path
    rtl_path: Path
    verification_path: Path
    revision: int = 0
    open_issues: list[ReviewIssue] = Field(default_factory=list)
    evidence: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def transition(self, state: WorkflowState) -> None:
        self.state = state
        self.updated_at = datetime.now(timezone.utc)
