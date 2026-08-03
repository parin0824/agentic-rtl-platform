from __future__ import annotations

from pathlib import Path

from agentic_rtl.agents.base import Agent
from agentic_rtl.core.io import load_model
from agentic_rtl.core.models import Specification


class SpecificationAgent(Agent[Path, Specification]):
    name = "specification_agent"

    def run(self, request: Path) -> Specification:
        specification = load_model(request, Specification)
        ids = [item.id for item in specification.requirements]
        if len(ids) != len(set(ids)):
            raise ValueError("Requirement identifiers must be unique")
        if not specification.clocks or not specification.resets:
            raise ValueError("Clock and reset definitions are mandatory")
        return specification
