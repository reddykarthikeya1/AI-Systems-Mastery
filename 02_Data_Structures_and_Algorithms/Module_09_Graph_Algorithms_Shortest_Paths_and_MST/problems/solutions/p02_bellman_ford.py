"""Reference solution — Problem 02: Bellman-Ford With Negative Cycle Detection

Pattern:    Bellman-Ford
Complexity: Time O(V*E), Space O(V)
"""

from __future__ import annotations


def bellman_ford(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float] | None:
    dist: list[float] = [float("inf")] * n
    dist[source] = 0

    # n-1 rounds: a shortest path uses at most n-1 edges, so this is enough for
    # every distance to propagate all the way.
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            # Never relax from an unreachable node: inf + (-5) would look like
            # an improvement and poison the result.
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                # already stable; no more rounds can help

    # One extra round. Any further improvement means a negative cycle.
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None

    return dist
