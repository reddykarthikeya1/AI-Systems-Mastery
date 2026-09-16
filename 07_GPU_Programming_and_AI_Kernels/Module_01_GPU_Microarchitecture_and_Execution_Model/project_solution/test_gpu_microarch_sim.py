"""Unit tests for GPU Microarchitecture Simulator."""
from __future__ import annotations

import pytest
from gpu_microarch_sim import (
    calculate_arithmetic_intensity,
    calculate_sm_occupancy,
    compute_warp_divergence,
    evaluate_roofline,
)


def test_warp_divergence_uniform_vs_split() -> None:
    # 32 identical threads -> 1 pass, full mask
    uniform_true = [True] * 32
    passes, masks = compute_warp_divergence(uniform_true)
    assert passes == 1
    assert masks == [0xFFFFFFFF]

    # Alternating threads -> 2 serialized passes
    alternating = [i % 2 == 0 for i in range(32)]
    passes, masks = compute_warp_divergence(alternating)
    assert passes == 2
    assert masks[0] == 0x55555555
    assert masks[1] == 0xAAAAAAAA


def test_arithmetic_intensity_and_roofline() -> None:
    # 2048 FLOPs on 1024 Bytes -> 2.0 FLOPs/byte
    intensity = calculate_arithmetic_intensity(2048, 1024)
    assert pytest.approx(intensity, rel=1e-5) == 2.0

    # NVIDIA A100 specs: 60 TFLOPs FP32, 2000 GB/s bandwidth -> Ridge point = 30 FLOPs/byte
    res_mem = evaluate_roofline(
        peak_tflops=60.0, peak_bandwidth_gbs=2000.0, arithmetic_intensity=5.0
    )
    assert res_mem.bound_type == "memory_bound"
    assert pytest.approx(res_mem.achieved_tflops, rel=1e-3) == 10.0  # 5 * 2000 / 1000

    # High intensity kernel: 100 FLOPs/byte -> Compute bound
    res_comp = evaluate_roofline(
        peak_tflops=60.0, peak_bandwidth_gbs=2000.0, arithmetic_intensity=100.0
    )
    assert res_comp.bound_type == "compute_bound"
    assert pytest.approx(res_comp.achieved_tflops, rel=1e-3) == 60.0


def test_sm_occupancy_limits() -> None:
    # 256 threads per block (8 warps), 32 regs/thread, 0 shared memory
    # 256 * 32 = 8192 regs/block -> 65536 / 8192 = 8 blocks -> 8 * 8 = 64 warps (100% occupancy)
    occ = calculate_sm_occupancy(
        threads_per_block=256,
        regs_per_thread=32,
        shared_mem_per_block_bytes=0,
    )
    assert pytest.approx(occ, rel=1e-5) == 1.0

    # Heavy register usage: 128 regs/thread -> limits occupancy
    occ_heavy = calculate_sm_occupancy(
        threads_per_block=256,
        regs_per_thread=128,
        shared_mem_per_block_bytes=0,
    )
    assert occ_heavy < 1.0
