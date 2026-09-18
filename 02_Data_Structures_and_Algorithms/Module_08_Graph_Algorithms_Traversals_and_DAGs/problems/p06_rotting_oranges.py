"""Problem 06 — Rotting Oranges

Pattern:    Multi-source BFS
Difficulty: Medium
Target:     Time O(rows*cols), Space O(rows*cols)

In a grid, ``0`` is empty, ``1`` is a fresh orange and ``2`` is rotten. Each
minute, every rotten orange rots its four orthogonal neighbours. Return the
number of minutes until no fresh orange remains, or ``-1`` if some fresh orange
can never rot.

Constraints
- ``1 <= rows, cols <= 100``

Example
    [[2,1,1],[1,1,0],[0,1,1]] -> 4
    [[2,1,1],[0,1,1],[1,0,1]] -> -1
    [[0,2]]                   -> 0

Example:
    >>> rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]])
    4
    >>> rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]])
    -1

Hints — read one at a time, and try again between each.

    Hint 1: This must be BFS, not DFS - you need the number of *rounds*, and BFS processes the grid in exactly those rounds.
    Hint 2: Seed the queue with EVERY rotten orange at once, at time 0. That is multi-source BFS, and it turns 'nearest rotten source' into one pass instead of one pass per source.
    Hint 3: Count fresh oranges up front. At the end, if any remain unreached, return -1. A grid with no fresh oranges at all takes 0 minutes, not -1.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def rotting_oranges(grid: list[list[int]]) -> int:
    raise NotImplementedError("implement rotting_oranges")
