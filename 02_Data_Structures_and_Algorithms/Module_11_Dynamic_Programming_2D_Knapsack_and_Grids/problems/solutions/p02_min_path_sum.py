"""Reference solution — Problem 02: Minimum Path Sum

Pattern:    2D grid DP
Complexity: Time O(rows*cols), Space O(cols)
"""

from __future__ import annotations


def min_path_sum(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        raise ValueError("grid must be non-empty")

    rows, cols = len(grid), len(grid[0])
    best = [0] * cols
    best[0] = grid[0][0]

    # First row: only one way in, from the left.
    for c in range(1, cols):
        best[c] = best[c - 1] + grid[0][c]

    for r in range(1, rows):
        best[0] += grid[r][0]           # first column: only from above
        for c in range(1, cols):
            # best[c] is still the row above; best[c-1] is already this row.
            best[c] = grid[r][c] + min(best[c], best[c - 1])

    return best[-1]
