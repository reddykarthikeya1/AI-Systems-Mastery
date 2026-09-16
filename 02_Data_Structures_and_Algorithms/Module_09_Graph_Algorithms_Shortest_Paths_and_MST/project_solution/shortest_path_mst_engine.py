"""Production solution for ShortestPathMSTEngine."""
from __future__ import annotations

import heapq
from collections import defaultdict
from typing import Generic, TypeVar

T = TypeVar("T")

class DSU(Generic[T]):
    def __init__(self):
        self.parent: dict[T, T] = {}
        self.rank: dict[T, int] = defaultdict(int)

    def find(self, x: T) -> T:
        if x not in self.parent:
            self.parent[x] = x
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: T, y: T) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


class ShortestPathMSTEngine(Generic[T]):
    """Algorithms for shortest paths (Dijkstra, Bellman-Ford) and MST (Kruskal)."""

    def __init__(self) -> None:
        self.adj: dict[T, list[tuple[T, float]]] = defaultdict(list)
        self.edges: list[tuple[float, T, T]] = []
        self.nodes: set[T] = set()

    def add_edge(self, u: T, v: T, weight: float, directed: bool = False) -> None:
        self.nodes.add(u)
        self.nodes.add(v)
        self.adj[u].append((v, weight))
        self.edges.append((weight, u, v))
        if not directed:
            self.adj[v].append((u, weight))
            self.edges.append((weight, v, u))

    def dijkstra(self, start: T) -> dict[T, float]:
        dist: dict[T, float] = {node: float("inf") for node in self.nodes}
        dist[start] = 0.0
        pq: list[tuple[float, T]] = [(0.0, start)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    def bellman_ford(self, start: T) -> dict[T, float]:
        dist: dict[T, float] = {node: float("inf") for node in self.nodes}
        dist[start] = 0.0
        v_count = len(self.nodes)

        for _ in range(v_count - 1):
            relaxed = False
            for w, u, v in self.edges:
                if dist[u] != float("inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    relaxed = True
            if not relaxed:
                break

        # Check for negative weight cycles
        for w, u, v in self.edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                raise ValueError("Graph contains a negative weight cycle")

        return dist

    def kruskal_mst(self) -> tuple[float, list[tuple[T, T, float]]]:
        dsu = DSU[T]()
        unique_undirected_edges: list[tuple[float, T, T]] = []
        seen = set()

        for w, u, v in self.edges:
            edge_id = tuple(sorted([str(u), str(v)]))
            if edge_id not in seen:
                seen.add(edge_id)
                unique_undirected_edges.append((w, u, v))

        unique_undirected_edges.sort(key=lambda x: x[0])
        total_weight = 0.0
        mst_edges: list[tuple[T, T, float]] = []

        for w, u, v in unique_undirected_edges:
            if dsu.union(u, v):
                total_weight += w
                mst_edges.append((u, v, w))

        return total_weight, mst_edges
