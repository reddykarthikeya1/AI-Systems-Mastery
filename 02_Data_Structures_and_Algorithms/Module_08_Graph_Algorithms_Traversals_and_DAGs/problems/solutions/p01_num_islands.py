"""Reference solution — Problem 01: Number Of Islands

Pattern:    DFS flood fill
Complexity: Time O(rows*cols), Space O(rows*cols)
"""

from __future__ import annotations


def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    islands = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or seen[r][c]:
                continue
            islands += 1
            # Explicit stack: a 300x300 grid of land would recurse 90,000 deep
            # and blow Python's 1000-frame limit.
            stack = [(r, c)]
            seen[r][c] = True
            while stack:
                y, x = stack.pop()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if (
                        0 <= ny < rows
                        and 0 <= nx < cols
                        and not seen[ny][nx]
                        and grid[ny][nx] == "1"
                    ):
                        seen[ny][nx] = True
                        stack.append((ny, nx))

    return islands
