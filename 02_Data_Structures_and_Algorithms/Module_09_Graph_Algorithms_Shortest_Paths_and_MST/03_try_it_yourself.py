"""Module 09: Interactive Shortest Paths CLI Sandbox."""
from __future__ import annotations

import heapq


def demo():
    print("\n=== DEMO: Dijkstra\'s Shortest Path ===")
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": []
    }
    pq = [(0, "A")]
    dist = {}
    while pq:
        d, u = heapq.heappop(pq)
        if u in dist:
            continue
        dist[u] = d
        for v, w in graph[u]:
            if v not in dist:
                heapq.heappush(pq, (d + w, v))
    print("Shortest distances from A to all nodes:", dist)


if __name__ == "__main__":
    demo()
