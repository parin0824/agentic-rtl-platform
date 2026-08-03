.PHONY: install test lint rtl-lint synth prepare mutants regression

install:
	python3 -m pip install -e '.[dev,verification,mcp]'

test:
	pytest -q

lint:
	ruff check src tests

rtl-lint:
	verilator --lint-only --Wall --Wno-fatal --top-module async_fifo rtl/async_fifo/async_fifo.sv

synth:
	yosys -q -p 'read_verilog -sv rtl/async_fifo/async_fifo.sv; hierarchy -top async_fifo; proc; check'

prepare:
	agentic-rtl prepare --workspace .

mutants:
	python3 scripts/create_mutants.py

regression:
	$(MAKE) -C verification/cocotb SIM=verilator
