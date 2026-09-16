"""Production reference implementation for NCU & NSYS Profiling Simulator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class KernelProfileMetric:
    kernel_name: str
    duration_us: float
    achieved_tflops: float
    achieved_dram_gbs: float
    warp_stall_breakdown: dict[str, float]  # reason -> percentage (0..100)


def analyze_kernel_bottleneck(
    profile: KernelProfileMetric,
    peak_tflops: float = 60.0,
    peak_dram_gbs: float = 2000.0,
) -> dict[str, Any]:
    """Diagnose kernel performance, compute SOL %, and provide tuning advice.

    Speed of Light (SOL):
    - Compute SOL % = (achieved_tflops / peak_tflops) * 100
    - Memory SOL % = (achieved_dram_gbs / peak_dram_gbs) * 100
    """
    compute_sol_pct = (profile.achieved_tflops / peak_tflops) * 100.0
    memory_sol_pct = (profile.achieved_dram_gbs / peak_dram_gbs) * 100.0

    dominant_regime = "compute_bound" if compute_sol_pct >= memory_sol_pct else "memory_bound"

    # Identify top warp stall reason
    top_stall = max(profile.warp_stall_breakdown.items(), key=lambda item: item[1]) if profile.warp_stall_breakdown else ("none", 0.0)

    recommendations = []
    if dominant_regime == "memory_bound":
        if top_stall[0] == "stall_long_scoreboard":
            recommendations.append("High DRAM latency: increase thread occupancy, vectorize loads with float4, or tile into SRAM.")
        elif top_stall[0] == "stall_short_scoreboard":
            recommendations.append("SRAM bank conflicts: pad shared memory arrays (e.g. tile[32][33]).")
        else:
            recommendations.append("Improve memory coalescing to saturate 128-byte cache lines.")
    else:
        if top_stall[0] == "stall_barrier":
            recommendations.append("Excessive __syncthreads(): use warp shuffle instructions to bypass shared memory barriers.")
        elif top_stall[0] == "stall_math_pipe_throttle":
            recommendations.append("Kernel is compute-saturated. Consider FP16/FP8 Tensor Core precision.")
        else:
            recommendations.append("Increase instruction-level parallelism (ILP) with register unrolling.")

    return {
        "kernel_name": profile.kernel_name,
        "compute_sol_pct": compute_sol_pct,
        "memory_sol_pct": memory_sol_pct,
        "dominant_regime": dominant_regime,
        "primary_stall_reason": top_stall[0],
        "primary_stall_pct": top_stall[1],
        "recommendations": recommendations,
    }


def calculate_speedup_potential(
    current_profile: KernelProfileMetric,
    stall_reason: str,
    reduction_factor: float = 0.5,
) -> float:
    """Estimate execution time speedup if a specific warp stall is mitigated.

    Amortized speedup according to Amdahl's Law:
    Speedup = 1 / ((1 - P) + P / S)
    where P is fraction of time caused by the stall, and S = 1 / (1 - reduction_factor).
    """
    stall_pct = current_profile.warp_stall_breakdown.get(stall_reason, 0.0)
    p = stall_pct / 100.0
    if p <= 0:
        return 1.0

    new_p = p * (1.0 - reduction_factor)
    new_duration_fraction = (1.0 - p) + new_p
    return 1.0 / new_duration_fraction if new_duration_fraction > 0 else 1.0
