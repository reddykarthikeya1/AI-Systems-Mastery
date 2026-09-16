"""Reference solution — Problem 07: N-Queens

Pattern:    Backtracking with constraint pruning
Complexity: Time O(n!) with heavy pruning, Space O(n)
"""

from __future__ import annotations


def n_queens(n: int) -> int:
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n == 0:
        return 1        # the empty board is one valid arrangement

    cols: set[int] = set()
    diag: set[int] = set()      # row - col is constant along one diagonal
    anti: set[int] = set()      # row + col is constant along the other
    count = 0

    def place(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            # Three O(1) checks replace scanning the whole board.
            if col in cols or (row - col) in diag or (row + col) in anti:
                continue
            cols.add(col)
            diag.add(row - col)
            anti.add(row + col)
            place(row + 1)
            cols.remove(col)        # undo all three
            diag.remove(row - col)
            anti.remove(row + col)

    place(0)
    return count
