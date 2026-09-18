"""Problem 01 — Warp Divergence Metrics

Topic: 01 GPU Microarchitecture and Execution Model
Target: Production-grade implementation

Calculate active threads and warp execution efficiency under SIMT branch divergence.

Example:
    >>> warp_divergence_metrics([0xF, 0xFF], 8)
    (2, 0.75)

Hints:
    Hint 1: Efficiency measures what fraction of all available lane-slots
        across every divergent pass actually did work — not the average
        popcount of a single mask in isolation.
    Hint 2: Popcount each bitmask with `bin(mask).count('1')`, sum those
        counts across all masks, then divide by `len(active_masks) *
        warp_size` to get the fraction of busy lane-slots.
    Hint 3: An empty `active_masks` list must short-circuit to `(0, 1.0)`
        instead of dividing by zero, and the efficiency value must be
        rounded to exactly 4 decimal places.
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
