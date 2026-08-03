# Architecture

## Design position

The platform uses a deterministic orchestrator around specialized agents. The language model, when connected, proposes artifacts and classifications. External tools establish evidence. The orchestrator owns state transitions, version references, retry limits, and sign-off gates.

## Initial agent set

| Agent | Responsibility | May write RTL | May approve own work |
|---|---|---:|---:|
| Specification | Validate the machine-readable requirements | No | No |
| RTL generation | Produce a candidate implementation | Candidate workspace only | No |
| RTL review | Compare implementation with requirements and tool results | No | No |
| Verification | Produce tests and reference behavior | Verification workspace only | No |
| Failure triage | Classify failed evidence and select an owner | No | No |
| Verification audit | Measure tests against controlled mutations | Mutant workspace only | No |

## State flow

```text
SPEC_READY
  -> RTL_GENERATED
  -> RTL_REVIEW_PASSED | RTL_REVIEW_FAILED
  -> VERIFICATION_READY
  -> REGRESSION_PASSED | REGRESSION_FAILED
  -> SIGNOFF_READY | AUDIT_FAILED
  -> COMPLETED
```

## Evidence hierarchy

1. Simulator, formal engine, linter, and synthesis results
2. Reproducible test results and stored seeds
3. Requirement-to-test traceability
4. Agent analysis
5. Model confidence

A model statement is never treated as proof of correctness.

## Security boundaries

- Commands use argument arrays rather than shell strings.
- Commands run only inside the repository workspace.
- Tool execution has a fixed timeout.
- Generated files are limited to `workspaces/` and `reports/generated/`.
- The verification agent cannot modify the accepted RTL.
- The RTL agent cannot modify the specification or accepted tests.
- Tool results retain command, exit code, standard output, standard error, and duration.

## LLM integration

The repository intentionally keeps model-provider code outside the critical path. A provider adapter should accept a typed request and return a typed response. The adapter must not own filesystem permissions, workflow state, or command execution.
