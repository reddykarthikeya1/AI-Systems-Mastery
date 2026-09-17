"""Problem 01 — Warp Divergence Metrics

Topic: 01 GPU Microarchitecture and Execution Model
Target: Production-grade implementation

Calculate active threads and warp execution efficiency under SIMT branch divergence.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def warp_divergence_metrics(active_masks: list[int], warp_size: int = 32) -> tuple[int, float]:
    """active_masks: list of 32-bit bitmasks representing active lanes for each branch path.
    Total cycles = len(active_masks).
    Average active threads per cycle = sum(popcount(mask)) / total_cycles.
    Efficiency = avg_active_threads / warp_size.
    Returns (total_cycles, efficiency rounded to 4 decimals).
    """
    raise NotImplementedError("Implement warp_divergence_metrics")
