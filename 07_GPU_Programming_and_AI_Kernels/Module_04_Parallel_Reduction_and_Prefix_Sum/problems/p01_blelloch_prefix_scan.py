"""Problem 01 — Blelloch Prefix Scan

Topic: 04 Parallel Reduction and Prefix Sum
Target: Production-grade implementation

Compute exclusive prefix scan using work-efficient Blelloch tree algorithm.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def blelloch_prefix_scan(values: list[int]) -> list[int]:
    """Compute exclusive prefix sum of values:
    out[0] = 0, out[i] = sum(values[:i]).
    Returns list of scanned values.
    """
    raise NotImplementedError("Implement blelloch_prefix_scan")
