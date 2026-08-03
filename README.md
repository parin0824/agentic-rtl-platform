# Agentic RTL Platform

An evidence-driven research platform for coordinating RTL generation, independent review, verification, failure triage, and verification auditing with open-source tools.

The first target is a dual-clock asynchronous FIFO. The repository contains synthesizable SystemVerilog, a cocotb regression, static review rules, controlled RTL mutations, a deterministic Python orchestrator, restricted tool wrappers, an optional MCP server, Docker packaging, and CI.

## Engineering principles

- Models propose; tools prove.
- No agent approves its own output.
- The orchestrator owns state and permissions.
- Agent communication uses typed records.
- Every failure must be reproducible.
- Coverage does not replace functional checking.
- Verification quality is measured with controlled mutations.

## System flow

```text
Specification
    -> RTL generation
    -> independent RTL review
    -> Verilator lint and Yosys synthesis checks
    -> verification preparation
    -> cocotb regression
    -> failure triage
    -> mutation-based verification audit
    -> evidence-based sign-off
```

## Repository layout

```text
src/agentic_rtl/       Python package, agents, orchestration, MCP, tools
rtl/async_fifo/        Accepted asynchronous FIFO RTL
verification/cocotb/   Python regression and simulator makefile
formal/                Initial SymbiYosys harness
specs/                 Versioned machine-readable requirements
mutations/             Mutation catalog examples
scripts/               Repository utilities
reports/               Generated structured evidence
workspaces/            Generated candidates and mutants
```

## Quick start without EDA tools

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
agentic-rtl prepare --workspace . --skip-external-tools
```

This validates orchestration, schemas, filesystem controls, static review, candidate generation, verification preparation, and mutation generation.

## Full open-source flow

Install Verilator, Yosys, Make, and a supported C++ compiler, then run:

```bash
pip install -e '.[dev,verification,mcp]'
make rtl-lint
make synth
make regression
agentic-rtl prepare --workspace .
```

Docker provides a reproducible starting environment:

```bash
docker compose build
docker compose run --rm agentic-rtl
```

## MCP server

After installing the MCP extra:

```bash
python3 -m agentic_rtl.mcp.server
```

The server exposes narrowly scoped operations for reading repository files, linting RTL, checking synthesis, running the cocotb regression, and writing generated artifacts only to approved directories.

## Current scope

Implemented:

- Typed project, review, tool, test, and audit records
- Deterministic workflow state
- Restricted command runner and workspace policy
- FIFO specification with requirement identifiers
- Synthesizable asynchronous FIFO RTL
- Static requirement-oriented RTL review
- Verilator and Yosys wrappers
- cocotb reset, ordering, overflow, and underflow tests
- Controlled mutation generation
- Optional MCP server
- Unit tests, Docker, and GitHub Actions

Planned:

- Provider-neutral LLM adapter with structured responses
- Complete mutation regression runner
- HTML evidence report and traceability matrix
- Formal harness refinement for asynchronous clocks
- Coverage ingestion and targeted-test requests
- AXI4-Lite and UART profiles

## Authorship and use

This repository is an AI-assisted engineering project. Generated work must be reviewed, understood, tested, and defended by the person presenting it. Do not represent unreviewed generated code as independently authored or production-signoff ready.
