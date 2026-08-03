from __future__ import annotations

from collections import deque

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def reset(dut) -> None:
    dut.wr_rst_n.value = 0
    dut.rd_rst_n.value = 0
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.wr_data.value = 0
    await Timer(40, units="ns")
    dut.wr_rst_n.value = 1
    dut.rd_rst_n.value = 1
    await Timer(40, units="ns")


async def write_word(dut, value: int) -> None:
    while int(dut.full.value):
        await RisingEdge(dut.wr_clk)
    dut.wr_data.value = value
    dut.wr_en.value = 1
    await RisingEdge(dut.wr_clk)
    dut.wr_en.value = 0


async def read_word(dut) -> int:
    while int(dut.empty.value):
        await RisingEdge(dut.rd_clk)
    dut.rd_en.value = 1
    await RisingEdge(dut.rd_clk)
    dut.rd_en.value = 0
    await RisingEdge(dut.rd_clk)
    return int(dut.rd_data.value)


async def start_clocks(dut) -> None:
    cocotb.start_soon(Clock(dut.wr_clk, 10, units="ns").start())
    cocotb.start_soon(Clock(dut.rd_clk, 14, units="ns").start())


@cocotb.test()
async def test_reset(dut) -> None:
    await start_clocks(dut)
    await reset(dut)
    assert int(dut.full.value) == 0
    assert int(dut.empty.value) == 1


@cocotb.test()
async def test_ordering(dut) -> None:
    await start_clocks(dut)
    await reset(dut)
    expected = deque(range(12))
    for value in expected:
        await write_word(dut, value)
    observed = [await read_word(dut) for _ in range(len(expected))]
    assert observed == list(expected)


@cocotb.test()
async def test_full_and_overflow(dut) -> None:
    await start_clocks(dut)
    await reset(dut)
    for value in range(16):
        await write_word(dut, value)
    for _ in range(8):
        await RisingEdge(dut.wr_clk)
    assert int(dut.full.value) == 1
    dut.wr_data.value = 255
    dut.wr_en.value = 1
    await RisingEdge(dut.wr_clk)
    dut.wr_en.value = 0
    observed = [await read_word(dut) for _ in range(16)]
    assert observed == list(range(16))


@cocotb.test()
async def test_empty_and_underflow(dut) -> None:
    await start_clocks(dut)
    await reset(dut)
    dut.rd_en.value = 1
    for _ in range(4):
        await RisingEdge(dut.rd_clk)
    dut.rd_en.value = 0
    assert int(dut.empty.value) == 1
    await write_word(dut, 91)
    assert await read_word(dut) == 91
