"""Reference solution — Problem 04: Cheapest Flight With At Most K Stops

Pattern:    Bellman-Ford by rounds
Complexity: Time O(k*E), Space O(V)
"""

from __future__ import annotations


def cheapest_flights(n: int, flights: list[tuple[int, int, int]], src: int, dst: int, k: int) -> int:
    INF = float("inf")
    dist: list[float] = [INF] * n
    dist[src] = 0

    # k stops means at most k+1 flights, so k+1 rounds.
    for _ in range(k + 1):
        # Relax into a COPY. Relaxing in place lets one round chain multiple
        # flights, which silently exceeds the hop limit.
        nxt = dist[:]
        for u, v, w in flights:
            if dist[u] != INF and dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt

    return -1 if dist[dst] == INF else int(dist[dst])
