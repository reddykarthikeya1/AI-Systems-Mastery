"""Problem 01 — Unique Paths In A Grid

Pattern:    2D grid DP
Difficulty: Medium
Target:     Time O(m*n), Space O(n)

Count the paths from the top-left to the bottom-right of an ``m x n`` grid,
moving only right or down.

Constraints
- ``1 <= m, n <= 100``

Example
    unique_paths(3, 7) -> 28
    unique_paths(3, 2) -> 3

Hints — read one at a time, and try again between each.

    Hint 1: You reach a cell only from above or from the left.
    Hint 2: So paths(r, c) = paths(r-1, c) + paths(r, c-1), with the first row and first column all 1.
    Hint 3: Each row depends only on the row above, so one row of length n is enough - O(n) space rather than O(m*n).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def unique_paths(m: int, n: int) -> int:
    raise NotImplementedError("implement unique_paths")
