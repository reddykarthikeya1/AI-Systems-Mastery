"""Reference solution — Problem 01: Unique Paths In A Grid

Pattern:    2D grid DP
Complexity: Time O(m*n), Space O(n)
"""

from __future__ import annotations


def unique_paths(m: int, n: int) -> int:
    if m < 1 or n < 1:
        raise ValueError(f"grid dimensions must be positive, got {m}x{n}")

    # One row suffices: row[c] is updated in place from the value above (its
    # own old value) plus the value to the left (already updated this pass).
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
