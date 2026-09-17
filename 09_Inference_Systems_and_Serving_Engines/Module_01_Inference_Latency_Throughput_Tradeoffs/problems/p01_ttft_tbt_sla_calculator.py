"""Problem 01 — Ttft Tbt Sla Calculator

Topic: 01 Inference Latency Throughput Tradeoffs
Target: Production-grade implementation

Compute Time-To-First-Token and Time-Between-Tokens SLA latency percentiles.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def ttft_tbt_sla_calculator(ttft_ms: list[float], tbt_ms: list[float]) -> dict[str, float]:
    """Compute p50 and p99 for TTFT and TBT.
    Returns dict with 'p50_ttft', 'p99_ttft', 'p50_tbt', 'p99_tbt' rounded to 2 decimals.
    """
    raise NotImplementedError("Implement ttft_tbt_sla_calculator")
