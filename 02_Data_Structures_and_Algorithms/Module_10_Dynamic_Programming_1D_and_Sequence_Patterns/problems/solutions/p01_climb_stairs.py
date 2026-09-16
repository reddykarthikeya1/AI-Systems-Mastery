"""Reference solution — Problem 01: Climbing Stairs

Pattern:    1D DP / Fibonacci recurrence
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def climb_stairs(n: int) -> int:
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n <= 1:
        return 1        # one way to stand still, one way to take a single step

    # Only the previous two values are ever needed, so no array is required.
    prev, cur = 1, 1
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur
