"""Reference solution — Problem 07: Shortest Path In A Binary Matrix

Pattern:    BFS with 8-directional moves
Complexity: Time O(n^2), Space O(n^2)
"""

from __future__ import annotations


def shortest_path_grid(grid: list[list[int]]) -> int:
    from collections import deque

    n = len(grid)
    # A blocked start or end makes the whole thing impossible.
    if n == 0 or grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
        return -1
    if n == 1:
        return 1

    DIRS = (
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    )

    seen = [[False] * n for _ in range(n)]
    seen[0][0] = True
    queue: deque[tuple[int, int, int]] = deque([(0, 0, 1)])

    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] == 0:
                if nr == n - 1 and nc == n - 1:
                    return dist + 1
                # Mark on ENQUEUE: marking on dequeue lets a cell be queued
                # many times and degrades the complexity badly.
                seen[nr][nc] = True
                queue.append((nr, nc, dist + 1))

    return -1
