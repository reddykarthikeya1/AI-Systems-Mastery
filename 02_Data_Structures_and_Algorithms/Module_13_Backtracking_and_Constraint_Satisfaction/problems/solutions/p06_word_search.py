"""Reference solution — Problem 06: Word Search In A Grid

Pattern:    Backtracking on a grid
Complexity: Time O(rows*cols*4^len(word)), Space O(len(word))
"""

from __future__ import annotations


def word_search(board: list[list[str]], word: str) -> bool:
    if not board or not board[0] or not word:
        return False

    rows, cols = len(board), len(board[0])

    def walk(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False

        original = board[r][c]
        board[r][c] = "\0"          # mark as in-use for THIS path only
        found = (
            walk(r + 1, c, i + 1)
            or walk(r - 1, c, i + 1)
            or walk(r, c + 1, i + 1)
            or walk(r, c - 1, i + 1)
        )
        board[r][c] = original      # restore, or later starts see a corrupt board
        return found

    return any(walk(r, c, 0) for r in range(rows) for c in range(cols))
