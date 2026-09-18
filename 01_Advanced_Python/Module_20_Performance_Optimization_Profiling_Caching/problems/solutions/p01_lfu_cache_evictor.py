"""Problem 01 — LFU Cache Eviction Frequency Counter

Target: Production-grade implementation
"""

from __future__ import annotations


def lfu_eviction_candidate(freq_map: dict[str, int], recency_order: list[str]) -> str | None:
    if not freq_map: return None
    min_freq = min(freq_map.values())
    candidates = {k for k, v in freq_map.items() if v == min_freq}
    for item in recency_order:
        if item in candidates:
            return item
    return next(iter(candidates))
