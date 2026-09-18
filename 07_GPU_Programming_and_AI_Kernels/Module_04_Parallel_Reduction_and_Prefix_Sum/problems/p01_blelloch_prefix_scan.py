"""Problem 01 — Blelloch Prefix Scan

Topic: 04 Parallel Reduction and Prefix Sum
Target: Production-grade implementation

Compute exclusive prefix scan using work-efficient Blelloch tree algorithm.

Example:
    >>> blelloch_prefix_scan([3, 1, 7, 4])
    [0, 3, 4, 11]

Hints:
    Hint 1: This module cares about the observable result of the scan, not
        the up-sweep/down-sweep tree structure that makes it parallel —
        element `i` of the output is the sum of everything strictly before
        it in the input.
    Hint 2: Walk `values` once, tracking a running total: append the total
        seen *so far* (before adding the current element), then add the
        current element to the running total for the next position.
    Hint 3: The scan is exclusive, so `out[0]` is always `0` regardless of
        `values[0]`, and an empty input must return an empty list rather
        than raising or returning `[0]`.
"""

from __future__ import annotations


def blelloch_prefix_scan(values: list[int]) -> list[int]:
    """Compute exclusive prefix sum of values:
    out[0] = 0, out[i] = sum(values[:i]).
    Returns list of scanned values.
    """
    raise NotImplementedError("Implement blelloch_prefix_scan")
