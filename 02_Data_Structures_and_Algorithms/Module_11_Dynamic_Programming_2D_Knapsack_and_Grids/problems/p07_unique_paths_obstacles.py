"""Problem 07 — Unique Paths With Obstacles

Pattern:    2D grid DP with blocked cells
Difficulty: Medium
Target:     Time O(rows*cols), Space O(cols)

``1`` marks an obstacle. Count the paths from top-left to bottom-right moving
only right or down, avoiding obstacles.

Constraints
- ``1 <= rows, cols <= 100``

Example
    [[0,0,0],[0,1,0],[0,0,0]] -> 2
    [[1]]                     -> 0

Hints — read one at a time, and try again between each.

    Hint 1: Same recurrence as unique paths, with one addition: an obstacle cell has zero paths through it.
    Hint 2: So set the cell to 0 and skip the addition entirely.
    Hint 3: Check the start and end cells first - a blocked start means the answer is 0, and it is easy to compute a nonsense number instead.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def unique_paths_obstacles(grid: list[list[int]]) -> int:
    raise NotImplementedError("implement unique_paths_obstacles")
