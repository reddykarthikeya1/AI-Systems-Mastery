"""Reference solution — Problem 03: Topological Sort

Pattern:    Kahn's algorithm
Complexity: Time O((n + E) log n), Space O(n + E)
"""

from __future__ import annotations


def topological_order(n: int, edges: list[tuple[int, int]]) -> list[int]:
    import heapq

    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1

    # A heap rather than a deque so the result is deterministic.
    ready = [i for i in range(n) if indegree[i] == 0]
    heapq.heapify(ready)

    out: list[int] = []
    while ready:
        u = heapq.heappop(ready)
        out.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(ready, v)

    # Emitting fewer than n nodes means the rest are in a cycle - Kahn detects
    # cycles for free.
    return out if len(out) == n else []
