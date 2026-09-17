"""Unit tests for NCU & NSYS Profiling Simulator."""
from __future__ import annotations

import pytest
from ncu_nsys_profiler_sim import (
    KernelProfileMetric,
    analyze_kernel_bottleneck,
    calculate_speedup_potential,
)


def test_kernel_bottleneck_diagnosis_memory() -> None:
    profile = KernelProfileMetric(
        kernel_name="unfused_layernorm",
        duration_us=150.0,
        achieved_tflops=3.0,       # 3 / 60 = 5% compute SOL
        achieved_dram_gbs=1800.0,  # 1800 / 2000 = 90% memory SOL
        warp_stall_breakdown={
            "stall_long_scoreboard": 70.0,
            "stall_barrier": 15.0,
            "stall_math_pipe_throttle": 5.0,
        },
    )

    diag = analyze_kernel_bottleneck(profile, peak_tflops=60.0, peak_dram_gbs=2000.0)
    assert diag["dominant_regime"] == "memory_bound"
    assert pytest.approx(diag["memory_sol_pct"], rel=1e-3) == 90.0
    assert diag["primary_stall_reason"] == "stall_long_scoreboard"
    assert len(diag["recommendations"]) > 0


def test_kernel_bottleneck_diagnosis_compute() -> None:
    profile = KernelProfileMetric(
        kernel_name="tiled_fp16_gemm",
        duration_us=45.0,
        achieved_tflops=55.0,     # 55 / 60 = 91.6% compute SOL
        achieved_dram_gbs=400.0,  # 400 / 2000 = 20% memory SOL
        warp_stall_breakdown={
            "stall_math_pipe_throttle": 80.0,
            "stall_short_scoreboard": 10.0,
        },
    )

    diag = analyze_kernel_bottleneck(profile, peak_tflops=60.0, peak_dram_gbs=2000.0)
    assert diag["dominant_regime"] == "compute_bound"
    assert diag["primary_stall_reason"] == "stall_math_pipe_throttle"


def test_speedup_potential_amdahl() -> None:
    profile = KernelProfileMetric(
        kernel_name="test_kernel",
        duration_us=100.0,
        achieved_tflops=10.0,
        achieved_dram_gbs=500.0,
        warp_stall_breakdown={"stall_long_scoreboard": 60.0},
    )

    # 60% of time in stall. If reduced by 50% (to 30%), total time = 40 + 30 = 70% -> speedup = 100/70 = ~1.428x
    speedup = calculate_speedup_potential(profile, "stall_long_scoreboard", reduction_factor=0.5)
    assert pytest.approx(speedup, rel=1e-2) == 1.428
