"""Problem 01 — Little Law Concurrency

Topic: 01 Physics of Scalability Capacity Math
Target: Production-grade implementation

Calculate average concurrency using Little's Law (L = lambda * W).

Example:
    >>> little_law_concurrency(5000.0, 0.05)
    250.0

Hints:
    Hint 1: The relationship is a direct proportionality -- the number of
        requests "in flight" at any instant depends only on how fast they
        arrive and how long each one lingers in the system, nothing else.
    Hint 2: This is pure arithmetic, not a simulation or loop -- Little's
        Law reduces to a single multiplication of the two inputs.
    Hint 3: A zero arrival rate (or zero latency) must yield exactly 0.0,
        not raise or return an int -- keep the result a float even at the
        boundary case tested by `little_law_concurrency(0.0, 1.0)`.
"""

from __future__ import annotations


def little_law_concurrency(arrival_rate_rps: float, avg_latency_seconds: float) -> float:
    """Return average number of concurrent requests in flight L = lambda * W."""
    raise NotImplementedError("Implement little_law_concurrency")
