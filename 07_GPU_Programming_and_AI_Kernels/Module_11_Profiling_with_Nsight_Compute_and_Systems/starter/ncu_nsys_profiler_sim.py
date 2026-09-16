"""Starter template for NCU & NSYS Profiling Simulator."""
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
    """Diagnose kernel performance, compute SOL %, and provide tuning advice."""
    raise NotImplementedError("Implement analyze_kernel_bottleneck")


def calculate_speedup_potential(
    current_profile: KernelProfileMetric,
    stall_reason: str,
    reduction_factor: float = 0.5,
) -> float:
    """Estimate execution time speedup if a specific warp stall is mitigated."""
    raise NotImplementedError("Implement calculate_speedup_potential")
