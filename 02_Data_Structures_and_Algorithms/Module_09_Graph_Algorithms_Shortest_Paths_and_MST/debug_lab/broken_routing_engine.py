#!/usr/bin/env python3
"""Routing engine. Exits 0, and quotes impossible prices.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import heapq
from collections import defaultdict

RULE = "=" * 68
INF = float("inf")


def dijkstra(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float]:
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def bellman_ford(n, edges, source):
    dist = [INF] * n
    dist[source] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    total = 0
    taken = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru
            total += w
            taken += 1
    return total


def main() -> None:
    print(RULE)
    print("ROUTING ENGINE")
    print(RULE)

    print()
    print("[1] Dijkstra shortest paths (non-negative weights)")
    cases = [
        (3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0, [0, 3, 1]),
        (4, [(0, 1, 10), (0, 2, 1), (2, 3, 1), (3, 1, 1)], 0, [0, 3, 1, 2]),
    ]
    for n, edges, src, expected in cases:
        print(f"      {edges} -> {dijkstra(n, edges, src)} (expected {expected})")

    print()
    print("[2] Dijkstra on a graph containing a negative edge")
    n, edges, src = 3, [(0, 1, 4), (0, 2, 1), (2, 1, -2)], 0
    print(f"      {edges}")
    print(f"          dijkstra     -> {dijkstra(n, edges, src)}")
    print(f"          bellman_ford -> {bellman_ford(n, edges, src)}")
    print("      (both claim to compute shortest paths from node 0)")

    print()
    print("[3] Negative cycle detection")
    cases = [
        (2, [(0, 1, 1), (1, 0, -3)], "a reachable negative cycle exists"),
        (3, [(0, 1, 4), (0, 2, 1), (2, 1, -2)], "no negative cycle"),
    ]
    for n, edges, note in cases:
        print(f"      {edges}")
        print(f"          bellman_ford -> {bellman_ford(n, edges, 0)}   ({note})")
    print("      (with a negative cycle, no shortest path is well defined)")

    print()
    print("[4] Minimum spanning tree cost")
    cases = [
        (4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)], 6, True),
        (3, [(0, 1, 1)], None, False),
        (2, [], None, False),
        (4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)], 3, True),
    ]
    for n, edges, expected, connected in cases:
        got = kruskal_mst(n, edges)
        label = expected if connected else "disconnected: no spanning tree exists"
        print(f"      n={n} {edges} -> {got} (expected {label})")

    print()
    print(RULE)
    print("Routing complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
