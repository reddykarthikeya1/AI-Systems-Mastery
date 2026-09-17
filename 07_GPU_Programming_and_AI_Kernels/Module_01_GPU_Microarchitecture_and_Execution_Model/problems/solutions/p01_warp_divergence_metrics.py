"""Reference Solution — Problem 01: Warp Divergence Metrics

Topic: 01 GPU Microarchitecture and Execution Model
"""

from __future__ import annotations


def warp_divergence_metrics(active_masks: list[int], warp_size: int = 32) -> tuple[int, float]:
    if not active_masks:
        return (0, 1.0)
    total_active = sum(bin(m).count('1') for m in active_masks)
    total_slots = len(active_masks) * warp_size
    eff = total_active / float(total_slots)
    return (len(active_masks), round(eff, 4))
