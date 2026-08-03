# Development guide

## Local Python validation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
ruff check src tests
```

## Open-source EDA validation

```bash
make rtl-lint
make synth
pip install -e '.[verification]'
make regression
```

## Build the candidate workspace

```bash
agentic-rtl prepare --workspace . --skip-external-tools
```

Remove `--skip-external-tools` after installing Verilator and Yosys.

## Generate controlled mutants

```bash
python3 scripts/create_mutants.py
```

Each mutant is derived from the accepted FIFO source using one named substitution. A production audit should compile and run the complete regression against every generated mutant, then report the fraction detected.

## Adding another DUT

1. Add a versioned JSON specification under `specs/`.
2. Add accepted RTL under `rtl/<dut>/`.
3. Add a verification environment under `verification/`.
4. Add static review rules that map to requirement identifiers.
5. Add controlled mutations tied to likely escaped defects.
6. Add an orchestrator profile rather than embedding DUT logic in the central state machine.
