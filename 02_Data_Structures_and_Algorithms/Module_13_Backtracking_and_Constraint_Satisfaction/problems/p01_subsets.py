"""Problem 01 — All Subsets

Pattern:    Backtracking
Difficulty: Medium
Target:     Time O(n * 2^n), Space O(n) excluding output

Return every subset of ``nums`` (the power set). The input has no duplicates.

Return the subsets sorted, so the output is deterministic.

Constraints
- ``0 <= len(nums) <= 10`` — the output has 2^n entries, so exponential is
  inherent, not a failure

Example
    subsets([1, 2, 3])
    -> [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]

Example:
    >>> subsets([1, 2, 3])
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

Hints — read one at a time, and try again between each.

    Hint 1: Each element is either in a subset or not, so there are 2^n subsets. That is the shape of the recursion.
    Hint 2: At each index, branch: include the element and recurse, then exclude it and recurse.
    Hint 3: Record path[:] - a COPY - not path itself. Storing the live list means every result is the same object and ends up empty.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def subsets(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError("implement subsets")
