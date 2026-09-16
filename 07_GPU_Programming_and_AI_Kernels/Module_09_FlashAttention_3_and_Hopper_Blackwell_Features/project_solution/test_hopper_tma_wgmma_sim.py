"""Unit tests for Hopper TMA and WGMMA Simulator."""
from __future__ import annotations

import numpy as np
from hopper_tma_wgmma_sim import (
    HopperTMASimulator,
    simulate_ping_pong_gemm_pipeline,
)


def test_tma_async_copy_simulator() -> None:
    tma = HopperTMASimulator(sram_capacity_kb=228)
    tensor = np.zeros((512, 512), dtype=np.float32)

    # 64x64 tile of float32 -> 64 * 64 * 4 = 16,384 bytes
    bytes_transferred = tma.issue_async_load(tensor, tile_coords=(0, 0), tile_shape=(64, 64))
    assert bytes_transferred == 16384
    assert tma.allocated_bytes == 16384

    # Release tile
    tma.release_tile(bytes_transferred)
    assert tma.allocated_bytes == 0


def test_ping_pong_pipeline_speedup() -> None:
    # GEMM dimensions: M=128, N=128, K=512 with tile_k=64
    res = simulate_ping_pong_gemm_pipeline(m=128, n=128, k=512, tile_k=64)

    assert res["num_phases"] == 8.0
    # Pipelining must be strictly faster than sequential execution
    assert res["pipelined_time_us"] < res["sequential_time_us"]
    assert res["speedup_factor"] > 1.0
