"""Reference solution — Problem 02: Merge Overlapping Intervals

Pattern:    Sort by START, then sweep
Complexity: Time O(n log n), Space O(n)
"""

from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []

    # Sort by START: merging needs intervals in the order they begin.
    ordered = sorted(intervals)
    out: list[tuple[int, int]] = [ordered[0]]

    for start, end in ordered[1:]:
        last_start, last_end = out[-1]
        if start <= last_end:
            # max() matters: a nested interval must not shrink the range.
            out[-1] = (last_start, max(last_end, end))
        else:
            out.append((start, end))

    return out
