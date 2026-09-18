"""Problem 01 — Number Of Islands

Pattern:    DFS flood fill
Difficulty: Medium
Target:     Time O(rows*cols), Space O(rows*cols)

Count the connected groups of ``'1'`` (land) in a grid of ``'1'`` and ``'0'``.
Cells connect only horizontally and vertically, not diagonally.

Do not mutate the caller's grid.

Constraints
- ``0 <= rows, cols <= 300``

Example
    [["1","1","0"],
     ["1","0","0"],
     ["0","0","1"]]  -> 2

Example:
    >>> num_islands([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]])
    2

Hints — read one at a time, and try again between each.

    Hint 1: Every time you find an unvisited land cell, you have found a new island.
    Hint 2: Then flood-fill it so its other cells are not counted again.
    Hint 3: Track visited separately rather than overwriting the input - a function that silently destroys its argument is a bug waiting to happen. Use an explicit stack, since a 300x300 grid can recurse 90,000 deep.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def num_islands(grid: list[list[str]]) -> int:
    raise NotImplementedError("implement num_islands")
