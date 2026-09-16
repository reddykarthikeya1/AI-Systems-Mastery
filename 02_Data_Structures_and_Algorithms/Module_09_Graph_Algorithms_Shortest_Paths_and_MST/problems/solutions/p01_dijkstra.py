"""Reference solution — Problem 01: Dijkstra's Shortest Paths

Pattern:    Dijkstra with a heap
Complexity: Time O(E log V), Space O(V + E)
"""

from __future__ import annotations


def dijkstra(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float]:
    import heapq

    adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    dist: list[float] = [float("inf")] * n
    dist[source] = 0
    heap: list[tuple[float, int]] = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        # heapq has no decrease-key, so stale entries accumulate. This is how
        # they are discarded.
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist
