"""Problem 07 — Shortest Path In A Binary Matrix

Pattern:    BFS with 8-directional moves
Difficulty: Medium
Target:     Time O(n^2), Space O(n^2)

Move from the top-left to the bottom-right of an ``n x n`` grid, stepping only
on ``0`` cells and moving in any of the **8** directions. Return the number of
cells on the shortest such path, or ``-1`` if there is none.

Constraints
- ``1 <= n <= 100``

Example
    [[0, 1], [1, 0]] -> 2
    [[0, 0, 0], [1, 1, 0], [1, 1, 0]] -> 4
    [[1, 0], [0, 0]] -> -1

Hints — read one at a time, and try again between each.

    Hint 1: Shortest path, unweighted: BFS. DFS finds a path but not the shortest.
    Hint 2: The 8 directions include the four diagonals - that is what makes [[0,1],[1,0]] solvable in 2 steps.
    Hint 3: Check the start and end cells before doing anything: if either is blocked the answer is -1. And mark cells visited when you ENQUEUE, not when you dequeue.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def shortest_path_grid(grid: list[list[int]]) -> int:
    raise NotImplementedError("implement shortest_path_grid")
