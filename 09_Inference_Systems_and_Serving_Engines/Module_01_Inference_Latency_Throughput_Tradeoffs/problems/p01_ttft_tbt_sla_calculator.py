"""Problem 01 — Ttft Tbt Sla Calculator

Topic: 01 Inference Latency Throughput Tradeoffs
Target: Production-grade implementation

Compute Time-To-First-Token and Time-Between-Tokens SLA latency percentiles.

Example:
    >>> ttft_tbt_sla_calculator([100.0, 120.0, 110.0, 300.0, 105.0], [20.0, 22.0, 21.0, 19.0, 50.0])
    {'p50_ttft': 110.0, 'p99_ttft': 300.0, 'p50_tbt': 21.0, 'p99_tbt': 50.0}

Hints:
    Hint 1: TTFT and TBT are two independent latency distributions — sort
        each series on its own and read percentiles off it; nothing links
        the two lists together besides both needing p50 and p99.
    Hint 2: Use nearest-rank indexing into the sorted list: sort ascending,
        then index at `int(q * len(sorted_list))` clamped to the last valid
        index, rather than interpolating between neighboring ranks.
    Hint 3: An empty ttft_ms or tbt_ms list must yield 0.0 for its
        percentiles instead of raising, and because the index truncates
        (floors) rather than rounds, p99 on a small sample often lands
        exactly on the maximum value; round every result to 2 decimals.
"""

from __future__ import annotations


def ttft_tbt_sla_calculator(ttft_ms: list[float], tbt_ms: list[float]) -> dict[str, float]:
    """Compute p50 and p99 for TTFT and TBT.
    Returns dict with 'p50_ttft', 'p99_ttft', 'p50_tbt', 'p99_tbt' rounded to 2 decimals.
    """
    raise NotImplementedError("Implement ttft_tbt_sla_calculator")
