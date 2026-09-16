"""Reference solution — Problem 06: Rotting Oranges

Pattern:    Multi-source BFS
Complexity: Time O(rows*cols), Space O(rows*cols)
"""

from __future__ import annotations


def rotting_oranges(grid: list[list[int]]) -> int:
    from collections import deque

    rows, cols = len(grid), len(grid[0])
    queue: deque[tuple[int, int]] = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))    # every source starts at time 0
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0                        # nothing to rot, so no time passes

    seen = [[grid[r][c] == 2 for c in range(cols)] for r in range(rows)]
    minutes = 0

    while queue and fresh:
        # One full level of the BFS is one minute.
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and not seen[nr][nc]
                    and grid[nr][nc] == 1
                ):
                    seen[nr][nc] = True
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1

    return -1 if fresh else minutes
