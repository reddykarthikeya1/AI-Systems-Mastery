"""Problem 02 — Merge Overlapping Intervals

Pattern:    Sort by START, then sweep
Difficulty: Medium
Target:     Time O(n log n), Space O(n)

Merge all overlapping intervals and return them sorted. Intervals that merely
touch (``[1,4]`` and ``[4,5]``) do overlap and must be merged.

Constraints
- ``0 <= len(intervals) <= 10**4``

Example
    [(1,3), (2,6), (8,10), (15,18)] -> [(1,6), (8,10), (15,18)]
    [(1,4), (4,5)]                  -> [(1,5)]

Hints — read one at a time, and try again between each.

    Hint 1: Sort by START. This is the merging case - compare with the next problem, which sorts by end for a different reason.
    Hint 2: Then sweep: if the next interval starts at or before the current one ends, extend the current end.
    Hint 3: Extend with max(current_end, next_end), not just next_end - a fully nested interval like [1,10] then [2,3] would otherwise shrink the merged range.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    raise NotImplementedError("implement merge_intervals")
