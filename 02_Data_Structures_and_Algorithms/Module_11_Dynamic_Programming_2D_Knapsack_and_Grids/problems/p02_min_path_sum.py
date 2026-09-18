"""Problem 02 — Minimum Path Sum

Pattern:    2D grid DP
Difficulty: Medium
Target:     Time O(rows*cols), Space O(cols)

Move right or down from the top-left to the bottom-right, minimising the sum of
the numbers on the path. Return that minimum.

Constraints
- ``1 <= rows, cols <= 200``
- values may be negative

Example
    [[1,3,1],[1,5,1],[4,2,1]] -> 7    (1 -> 3 -> 1 -> 1 -> 1)

Example:
    >>> min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    7

Hints — read one at a time, and try again between each.

    Hint 1: Same shape as unique paths, but you take a minimum instead of a sum of counts, and you add the cell's own value.
    Hint 2: best(r, c) = grid[r][c] + min(best(r-1, c), best(r, c-1)), with the first row and column being running totals.
    Hint 3: Handle the first row and column separately - they have only one predecessor each, and taking min against a missing neighbour is where the off-by-one bugs live.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def min_path_sum(grid: list[list[int]]) -> int:
    raise NotImplementedError("implement min_path_sum")
