"""Problem 01 — Little Law Concurrency

Topic: 01 Physics of Scalability Capacity Math
Target: Production-grade implementation

Calculate average concurrency using Little's Law (L = lambda * W).

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def little_law_concurrency(arrival_rate_rps: float, avg_latency_seconds: float) -> float:
    """Return average number of concurrent requests in flight L = lambda * W."""
    raise NotImplementedError("Implement little_law_concurrency")
