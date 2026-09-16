"""Reference solution — Problem 03: Maximum Non-Overlapping Intervals

Pattern:    Sort by END, then greedy
Complexity: Time O(n log n), Space O(1)
"""

from __future__ import annotations


def max_non_overlapping(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0

    # Sort by END. The earliest-finishing interval leaves the most room for
    # everything after it, which is the exchange argument in one line.
    count = 0
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count
