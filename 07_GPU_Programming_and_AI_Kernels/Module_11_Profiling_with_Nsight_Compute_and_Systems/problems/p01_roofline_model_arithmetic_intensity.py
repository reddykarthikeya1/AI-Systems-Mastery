"""Problem 01 — Roofline Model Arithmetic Intensity

Topic: 11 Profiling with Nsight Compute and Systems
Target: Production-grade implementation

Determine compute-bound vs memory-bound regime in Roofline model.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def roofline_model_arithmetic_intensity(flops: float, memory_bytes: float, peak_gflops: float, peak_gbps: float) -> tuple[float, str]:
    """Arithmetic intensity AI = flops / memory_bytes (FLOP/byte).
    Machine balance = peak_gflops / peak_gbps.
    If AI >= machine_balance: regime is 'COMPUTE_BOUND'.
    Else: regime is 'MEMORY_BOUND'.
    Returns (AI rounded to 2 decimals, regime).
    """
    raise NotImplementedError("Implement roofline_model_arithmetic_intensity")
