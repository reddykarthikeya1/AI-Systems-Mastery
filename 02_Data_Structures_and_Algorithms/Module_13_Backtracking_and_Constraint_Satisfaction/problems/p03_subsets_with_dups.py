"""Problem 03 — Subsets With Duplicates

Pattern:    Backtracking with duplicate skipping
Difficulty: Medium
Target:     Time O(n * 2^n), Space O(n) excluding output

Return every **unique** subset, where ``nums`` may contain duplicates. Return
them sorted.

Constraints
- ``0 <= len(nums) <= 10``

Example
    subsets_with_dups([1, 2, 2]) -> [[], [1], [1,2], [1,2,2], [2], [2,2]]

Example:
    >>> subsets_with_dups([1, 2, 2])
    [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

Hints — read one at a time, and try again between each.

    Hint 1: Deduplicating the output afterwards works but is wasteful - you generate the duplicates first.
    Hint 2: Sort the input so equal values sit next to each other.
    Hint 3: Then at each level, skip a value equal to the previous one: `if i > start and ordered[i] == ordered[i-1]: continue`. The `i > start` part is essential - without it you also skip legitimate repeats WITHIN a subset, and [1,2,2] never appears.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def subsets_with_dups(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError("implement subsets_with_dups")
