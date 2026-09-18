"""Problem 06 — Word Search In A Grid

Pattern:    Backtracking on a grid
Difficulty: Medium
Target:     Time O(rows*cols*4^len(word)), Space O(len(word))

Return True if ``word`` can be spelled by moving between horizontally or
vertically adjacent cells, using each cell **at most once** per path.

The board must not be permanently modified.

Constraints
- ``1 <= rows, cols <= 6``, ``1 <= len(word) <= 15``

Example
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    word_search(board, "ABCCED") -> True
    word_search(board, "SEE")    -> True
    word_search(board, "ABCB")   -> False    (the B would be reused)

Example:
    >>> board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    >>> word_search(board, "ABCCED")
    True
    >>> word_search(board, "ABCB")
    False

Hints — read one at a time, and try again between each.

    Hint 1: Try every cell as a starting point, then walk outward matching one character at a time.
    Hint 2: A cell may not be reused within one path, so mark it before recursing and UNMARK it after - the unmark is what allows a different path to use it later.
    Hint 3: Overwriting the cell with a sentinel is the classic trick, but you must restore the original character on the way out or the board is corrupted for every subsequent start.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def word_search(board: list[list[str]], word: str) -> bool:
    raise NotImplementedError("implement word_search")
