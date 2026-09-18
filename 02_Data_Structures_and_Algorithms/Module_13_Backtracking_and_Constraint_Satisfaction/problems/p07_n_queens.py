"""Problem 07 — N-Queens

Pattern:    Backtracking with constraint pruning
Difficulty: Hard
Target:     Time O(n!) with heavy pruning, Space O(n)

Return the number of ways to place ``n`` queens on an ``n x n`` board so that
no two attack each other.

Constraints
- ``0 <= n <= 9``

Example
    n_queens(4) -> 2
    n_queens(8) -> 92

This problem is intractable without pruning and instant with it. Enumerating
all placements for n = 8 is C(64, 8) ≈ 4.4 billion; pruning column by column
with three constraint sets visits a few thousand states.

Example:
    >>> n_queens(4)
    2

Hints — read one at a time, and try again between each.

    Hint 1: Place one queen per row - that removes row conflicts by construction.
    Hint 2: For each row, try every column that is not attacked. You need to check three things: the column, and the two diagonals.
    Hint 3: Both diagonals have a constant signature: row - col is fixed along one, row + col along the other. Keep three sets and membership is O(1), which is what makes the pruning cheap enough to matter.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def n_queens(n: int) -> int:
    raise NotImplementedError("implement n_queens")
