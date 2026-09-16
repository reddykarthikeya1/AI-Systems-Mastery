#!/usr/bin/env python3
"""Graph traversal service. Exits 0, and rejects valid DAGs.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

from collections import defaultdict, deque

RULE = "=" * 68


def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    islands = 0
    DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or seen[r][c]:
                continue
            islands += 1
            stack = [(r, c)]
            seen[r][c] = True
            while stack:
                y, x = stack.pop()
                for dy, dx in DIRS:
                    ny, nx = y + dy, x + dx
                    if (0 <= ny < rows and 0 <= nx < cols
                            and not seen[ny][nx] and grid[ny][nx] == "1"):
                        seen[ny][nx] = True
                        stack.append((ny, nx))
    return islands


def has_cycle_directed(n: int, edges: list[tuple[int, int]]) -> bool:
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
    visited = [False] * n

    def dfs(u: int) -> bool:
        visited[u] = True
        for v in adj[u]:
            if visited[v]:
                return True
            if dfs(v):
                return True
        return False

    for start in range(n):
        if not visited[start] and dfs(start):
            return True
    return False


def topological_order(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    queue = deque(sorted(i for i in range(n) if indegree[i] == 0))
    out = []
    while queue:
        u = queue.popleft()
        out.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return out


def shortest_hops(n: int, edges: list[tuple[int, int]], src: int, dst: int) -> int:
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    best = [-1]

    def dfs(u: int, depth: int, seen: set[int]) -> None:
        if u == dst:
            if best[0] == -1:
                best[0] = depth
            return
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                dfs(v, depth + 1, seen)

    dfs(src, 0, {src})
    return best[0]


def main() -> None:
    print(RULE)
    print("GRAPH TRAVERSAL SERVICE")
    print(RULE)

    print()
    print("[1] Island counting (orthogonal adjacency only)")
    grids = [
        ([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]], 2),
        ([["1", "0"], ["0", "1"]], 2),
        ([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]], 5),
    ]
    for grid, expected in grids:
        print(f"      {grid} -> {num_islands(grid)} (expected {expected})")

    print()
    print("[2] Directed cycle detection")
    cases = [
        (2, [(0, 1), (1, 0)], True),
        (4, [(0, 1), (0, 2), (1, 3), (2, 3)], False),
        (4, [(0, 1), (1, 2), (2, 3)], False),
        (5, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)], False),
    ]
    for n, edges, expected in cases:
        print(f"      n={n} {edges}")
        print(f"          reported {has_cycle_directed(n, edges)!s:<6} expected {expected}")

    print()
    print("[3] Topological ordering")
    for n, edges in ((4, [(0, 1), (1, 2), (2, 3)]), (2, [(0, 1), (1, 0)]),
                     (3, [(0, 1), (1, 2), (2, 0)])):
        order = topological_order(n, edges)
        valid = len(order) == n
        print(f"      n={n} {edges} -> {order} (covers all {n} nodes: {valid})")
    print("      (a graph with a cycle has NO valid ordering)")

    print()
    print("[4] Shortest hop count")
    cases = [
        (4, [(0, 1), (1, 3), (0, 2), (2, 3)], 0, 3, 2),
        (5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)], 0, 4, 1),
        (4, [(0, 1), (1, 2), (2, 3), (0, 3)], 0, 3, 1),
    ]
    for n, edges, src, dst, expected in cases:
        print(f"      {edges} {src}->{dst} = {shortest_hops(n, edges, src, dst)} "
              f"(expected {expected})")

    print()
    print(RULE)
    print("Traversal service complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
