"""Reference solution — Problem 07: Unique Paths With Obstacles

Pattern:    2D grid DP with blocked cells
Complexity: Time O(rows*cols), Space O(cols)
"""

from __future__ import annotations


def unique_paths_obstacles(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    # A blocked start or finish makes the whole thing impossible.
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return 0

    row = [0] * cols
    row[0] = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                row[c] = 0          # nothing passes through an obstacle
            elif c > 0:
                row[c] += row[c - 1]
    return row[-1]
