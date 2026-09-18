"""Problem 01 — Roofline Model Arithmetic Intensity

Topic: 11 Profiling with Nsight Compute and Systems
Target: Production-grade implementation

Determine compute-bound vs memory-bound regime in Roofline model.

Example:
    >>> roofline_model_arithmetic_intensity(1000.0, 2.0, 1000.0, 3000.0)
    (500.0, 'COMPUTE_BOUND')

Hints:
    Hint 1: The regime is decided by comparing two ratios that are both
        expressed in the same unit (FLOP/byte) — the workload's own
        FLOP-to-byte ratio versus the machine's peak FLOP-to-byte ratio.
    Hint 2: Compute arithmetic intensity as `flops / memory_bytes` and the
        machine's balance point as `peak_gflops / peak_gbps`; the workload
        is `'COMPUTE_BOUND'` when its AI meets or exceeds that balance
        point, otherwise `'MEMORY_BOUND'`.
    Hint 3: Guard both divisions — `memory_bytes <= 0` and `peak_gbps <= 0`
        should fall back to `0.0` rather than raising a
        `ZeroDivisionError`, and equality (`AI == balance`) counts as
        compute-bound, not memory-bound. Round the AI to 2 decimals.
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
