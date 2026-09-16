"""Problem 03 — Maximum Non-Overlapping Intervals

Pattern:    Sort by END, then greedy
Difficulty: Medium
Target:     Time O(n log n), Space O(1)

Return the largest number of mutually non-overlapping intervals you can select.
Intervals that merely touch (``[1,2]`` and ``[2,3]``) do **not** overlap and may
both be selected.

Constraints
- ``0 <= len(intervals) <= 10**4``

Example
    max_non_overlapping([(1,3), (2,4), (3,5)]) -> 2     ((1,3) and (3,5))

Compare this with the previous problem. Same input shape, and the sort key is
different: **end**, not start. Sorting by start here gives a plausible wrong
answer — the tests include a case where it does.

Hints — read one at a time, and try again between each.

    Hint 1: Which interval is always safe to take first? Think about which choice leaves the most room for everything after it.
    Hint 2: The one that FINISHES earliest. So sort by end time.
    Hint 3: Then take an interval whenever its start is at or after the last taken end. The exchange argument proves this is optimal: any optimal solution can have its first interval swapped for the earliest-finishing one without getting worse.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def max_non_overlapping(intervals: list[tuple[int, int]]) -> int:
    raise NotImplementedError("implement max_non_overlapping")
