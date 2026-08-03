# Interview notes

## Thirty-second explanation

This project is a controlled multi-agent workflow for RTL development and verification. A deterministic Python orchestrator owns state and permissions. Separate agents prepare RTL, review it, generate tests, classify failures, and audit verification quality. Agents access Verilator, Yosys, cocotb, and repository resources through narrow tools. Tool results are evidence; model output is only a proposal.

## Why multiple agents

Generation and approval are conflicting responsibilities. Separating them creates independent review, smaller contexts, clearer permissions, and traceable ownership.

## Why an orchestrator

The orchestrator prevents agents from changing authoritative state, tracks artifact versions, applies retry limits, and routes failures using structured results.

## Why MCP

MCP standardizes discovery and invocation of tools and resources. It does not provide reasoning or correctness. The host still owns security, approval, and workflow state.

## How hallucination is controlled

- Typed inputs and outputs
- Restricted tools
- External compile, lint, synthesis, and simulation evidence
- Requirement identifiers attached to findings
- Recorded commands and seeds
- Independent review and mutation testing

## How verification is evaluated

Coverage alone is insufficient. The platform introduces known RTL defects and measures whether the regression detects them. A surviving mutation identifies a weakness in the tests or reference model.

## Honest project boundary

This is a research prototype for AI-assisted RTL development and verification. It does not replace industrial sign-off, complete SystemVerilog/UVM support, commercial CDC analysis, or engineer accountability.
