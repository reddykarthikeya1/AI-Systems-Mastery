"""Reference solution — Problem 06: Minimum Spanning Tree (Prim)

Pattern:    Prim with a heap
Complexity: Time O(E log V), Space O(V + E)
"""

from __future__ import annotations


def prim_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    import heapq

    if n <= 1:
        return 0

    adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))       # undirected

    visited = [False] * n
    heap: list[tuple[int, int]] = [(0, 0)]   # cost 0 to include the start
    total = 0
    count = 0

    while heap and count < n:
        w, u = heapq.heappop(heap)
        if visited[u]:
            continue                # stale entry, same idea as in Dijkstra
        visited[u] = True
        total += w
        count += 1
        for nw, v in adj[u]:
            if not visited[v]:
                heapq.heappush(heap, (nw, v))

    return total if count == n else -1
