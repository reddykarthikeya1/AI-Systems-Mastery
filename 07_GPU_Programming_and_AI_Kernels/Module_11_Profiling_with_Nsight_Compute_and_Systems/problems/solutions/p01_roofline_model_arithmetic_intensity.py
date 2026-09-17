"""Reference Solution — Problem 01: Roofline Model Arithmetic Intensity

Topic: 11 Profiling with Nsight Compute and Systems
"""

from __future__ import annotations


def roofline_model_arithmetic_intensity(flops: float, memory_bytes: float, peak_gflops: float, peak_gbps: float) -> tuple[float, str]:
    ai = flops / memory_bytes if memory_bytes > 0 else 0.0
    balance = peak_gflops / peak_gbps if peak_gbps > 0 else 0.0
    regime = 'COMPUTE_BOUND' if ai >= balance else 'MEMORY_BOUND'
    return (round(ai, 2), regime)
