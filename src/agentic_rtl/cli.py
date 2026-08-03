from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from agentic_rtl.core.orchestrator import Orchestrator

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def prepare(
    workspace: Path = typer.Option(Path.cwd(), exists=True, file_okay=False),
    skip_external_tools: bool = typer.Option(False),
) -> None:
    record = Orchestrator(workspace).prepare(execute_tools=not skip_external_tools)
    console.print(json.dumps(record.model_dump(mode="json"), indent=2, default=str))


@app.command()
def status(workspace: Path = typer.Option(Path.cwd(), exists=True, file_okay=False)) -> None:
    path = workspace / "reports/project_record.json"
    if not path.exists():
        raise typer.Exit("No project record exists. Run prepare first.")
    console.print(path.read_text(encoding="utf-8"))
