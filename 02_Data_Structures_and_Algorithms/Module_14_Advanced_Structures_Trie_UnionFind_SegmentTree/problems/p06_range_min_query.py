"""Problem 06 — Sparse Table: Range Minimum, No Updates

Pattern:    Sparse table
Difficulty: Hard
Target:     Time O(n log n) preprocessing, O(1) per query

Answer many range-minimum queries on a **static** array. Each query is an
inclusive ``(lo, hi)``.

Constraints
- ``1 <= len(nums) <= 10**5``, ``1 <= len(queries) <= 10**5``
- O(1) per query after preprocessing is the target

Example
    range_minimums([2, 5, 1, 4, 9], [(0, 2), (1, 4), (3, 3)]) -> [1, 1, 4]

A segment tree gives `O(log n)` queries and supports updates. When the array
never changes, a sparse table gives `O(1)` queries — because `min` is
*idempotent*, so overlapping ranges may be combined freely. That does not work
for `sum`, which is why sums use a different structure.

Example:
    >>> range_minimums([2, 5, 1, 4, 9], [(0, 2), (1, 4), (3, 3)])
    [1, 1, 4]

Hints — read one at a time, and try again between each.

    Hint 1: Precompute the minimum of every range whose length is a power of two: table[k][i] covers nums[i .. i + 2^k - 1].
    Hint 2: table[k][i] = min(table[k-1][i], table[k-1][i + 2^(k-1)]) - each level built from the one below.
    Hint 3: A query of length L is answered by two blocks of size 2^floor(log2 L) that together cover it and may OVERLAP. Overlapping is fine because min is idempotent; this is exactly why the same trick fails for sum.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def range_minimums(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError("implement range_minimums")
