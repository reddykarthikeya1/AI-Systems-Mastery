"""Production solution for BacktrackingSolverEngine."""
from __future__ import annotations


class BacktrackingSolverEngine:
    """Constraint satisfaction problem solvers."""

    @staticmethod
    def solve_n_queens(n: int) -> list[list[str]]:
        results: list[list[str]] = []
        cols: set[int] = set()
        diag1: set[int] = set()  # r - c
        diag2: set[int] = set()  # r + c
        board = [["."] * n for _ in range(n)]

        def backtrack(r: int):
            if r == n:
                results.append(["".join(row) for row in board])
                return

            for c in range(n):
                if c in cols or (r - c) in diag1 or (r + c) in diag2:
                    continue

                cols.add(c)
                diag1.add(r - c)
                diag2.add(r + c)
                board[r][c] = "Q"

                backtrack(r + 1)

                board[r][c] = "."
                cols.remove(c)
                diag1.remove(r - c)
                diag2.remove(r + c)

        backtrack(0)
        return results

    @staticmethod
    def solve_sudoku(board: list[list[str]]) -> bool:
        def is_valid(r: int, c: int, char: str) -> bool:
            for i in range(9):
                if board[r][i] == char or board[i][c] == char:
                    return False
                box_r = 3 * (r // 3) + i // 3
                box_c = 3 * (c // 3) + i % 3
                if board[box_r][box_c] == char:
                    return False
            return True

        def solve() -> bool:
            for r in range(9):
                for c in range(9):
                    if board[r][c] == ".":
                        for num in "123456789":
                            if is_valid(r, c, num):
                                board[r][c] = num
                                if solve():
                                    return True
                                board[r][c] = "."
                        return False
            return True

        return solve()
