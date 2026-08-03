from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agentic_rtl.agents.base import Agent
from agentic_rtl.core.models import Specification


@dataclass(frozen=True)
class RtlGenerationRequest:
    specification: Specification
    template_path: Path
    output_path: Path


class RtlGenerationAgent(Agent[RtlGenerationRequest, Path]):
    name = "rtl_generation_agent"

    def run(self, request: RtlGenerationRequest) -> Path:
        source = request.template_path.read_text(encoding="utf-8")
        required = {request.specification.module_name, "wr_clk", "rd_clk", "full", "empty"}
        missing = sorted(item for item in required if item not in source)
        if missing:
            raise ValueError(f"RTL template is missing required elements: {', '.join(missing)}")
        request.output_path.parent.mkdir(parents=True, exist_ok=True)
        request.output_path.write_text(source, encoding="utf-8")
        return request.output_path
