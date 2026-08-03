from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentic_rtl.agents.base import Agent
from agentic_rtl.core.models import Specification


@dataclass(frozen=True)
class VerificationRequest:
    specification: Specification
    source_dir: Path
    output_dir: Path


class VerificationAgent(Agent[VerificationRequest, Path]):
    name = "verification_agent"

    def run(self, request: VerificationRequest) -> Path:
        request.output_dir.mkdir(parents=True, exist_ok=True)
        for source in request.source_dir.glob("*"):
            if source.is_file():
                target = request.output_dir / source.name
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        tests = (request.output_dir / "test_async_fifo.py").read_text(encoding="utf-8")
        required_tests = ("test_reset", "test_ordering", "test_full_and_overflow", "test_empty_and_underflow")
        missing = [name for name in required_tests if name not in tests]
        if missing:
            raise ValueError(f"Verification source is missing tests: {', '.join(missing)}")
        return request.output_dir
