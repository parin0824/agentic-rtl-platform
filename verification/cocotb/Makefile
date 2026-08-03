TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../../rtl/async_fifo/async_fifo.sv
TOPLEVEL = async_fifo
MODULE = test_async_fifo
COMPILE_ARGS += -Wall -Wno-fatal
SIM ?= verilator
include $(shell cocotb-config --makefiles)/Makefile.sim
