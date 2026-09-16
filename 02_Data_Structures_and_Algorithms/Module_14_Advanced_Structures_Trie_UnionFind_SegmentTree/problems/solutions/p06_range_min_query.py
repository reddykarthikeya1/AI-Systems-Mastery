"""Reference solution — Problem 06: Sparse Table: Range Minimum, No Updates

Pattern:    Sparse table
Complexity: Time O(n log n) preprocessing, O(1) per query
"""

from __future__ import annotations


def range_minimums(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    n = len(nums)
    if n == 0:
        return [0 for _ in queries]

    # levels = floor(log2(n)) + 1
    levels = n.bit_length()
    table: list[list[int]] = [list(nums)]
    for k in range(1, levels):
        span = 1 << k
        half = span >> 1
        prev = table[k - 1]
        row = [
            min(prev[i], prev[i + half])
            for i in range(n - span + 1)
        ]
        table.append(row)

    out: list[int] = []
    for lo, hi in queries:
        if lo > hi:
            raise ValueError(f"empty range ({lo}, {hi})")
        length = hi - lo + 1
        k = length.bit_length() - 1     # floor(log2(length))
        span = 1 << k
        # The two blocks OVERLAP when length is not a power of two, which is
        # harmless because min is idempotent - unlike sum.
        out.append(min(table[k][lo], table[k][hi - span + 1]))
    return out
