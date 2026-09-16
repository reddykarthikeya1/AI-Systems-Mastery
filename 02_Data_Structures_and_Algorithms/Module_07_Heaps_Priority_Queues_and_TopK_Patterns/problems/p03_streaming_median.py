"""Problem 03 — Median From A Data Stream

Pattern:    Two heaps
Difficulty: Hard
Target:     Time O(n log n) total, O(1) per query, Space O(n)

After each number arrives, report the median of everything seen so far. Return
the list of medians.

Constraints
- ``1 <= len(nums) <= 10**5``
- each insertion must be O(log n) and each query O(1) — re-sorting per element
  is O(n^2 log n) overall and far too slow

Example
    streaming_median([2, 3, 4]) -> [2.0, 2.5, 3.0]

Hints — read one at a time, and try again between each.

    Hint 1: Split the data at the median: a lower half and an upper half.
    Hint 2: Keep the lower half in a MAX-heap and the upper half in a MIN-heap. Then both candidates for the median sit at the two roots.
    Hint 3: Python's heapq is min-only, so negate values for the max-heap. After each insert, rebalance so the sizes differ by at most 1.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def streaming_median(nums: list[int]) -> list[float]:
    raise NotImplementedError("implement streaming_median")
