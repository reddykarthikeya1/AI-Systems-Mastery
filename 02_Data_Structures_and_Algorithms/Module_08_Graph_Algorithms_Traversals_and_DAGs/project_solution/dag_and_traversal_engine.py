"""Production solution for DAGAndTraversalEngine."""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Generic, TypeVar

T = TypeVar("T")

class GraphEngine(Generic[T]):
    """Adjacency list graph with BFS, DFS, and Kahn's Topological Sort."""

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: dict[T, list[T]] = defaultdict(list)
        self.in_degree: dict[T, int] = defaultdict(int)

    def add_vertex(self, u: T) -> None:
        if u not in self.adj:
            self.adj[u] = []
            self.in_degree[u] = 0

    def add_edge(self, u: T, v: T) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if self.directed:
            self.in_degree[v] += 1
        else:
            self.adj[v].append(u)

    def bfs(self, start: T) -> list[T]:
        if start not in self.adj:
            return []
        visited: set[T] = {start}
        queue: deque[T] = deque([start])
        order: list[T] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in self.adj[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        return order

    def dfs(self, start: T) -> list[T]:
        if start not in self.adj:
            return []
        visited: set[T] = set()
        order: list[T] = []

        def _dfs(curr: T):
            visited.add(curr)
            order.append(curr)
            for nxt in self.adj[curr]:
                if nxt not in visited:
                    _dfs(nxt)

        _dfs(start)
        return order

    def topological_sort(self) -> list[T]:
        """Kahn's algorithm using in-degree queue."""
        if not self.directed:
            raise ValueError("Topological sort requires a directed graph")

        in_deg = dict(self.in_degree)
        queue = deque([u for u in self.adj if in_deg[u] == 0])
        order: list[T] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in self.adj[node]:
                in_deg[nxt] -= 1
                if in_deg[nxt] == 0:
                    queue.append(nxt)

        if len(order) != len(self.adj):
            raise ValueError("Cycle detected in directed graph; topological sort impossible")
        return order

    def count_connected_components(self) -> int:
        """Count components (undirected) or weakly connected components (directed)."""
        visited: set[T] = set()
        components = 0

        for node in list(self.adj.keys()):
            if node not in visited:
                components += 1
                queue: deque[T] = deque([node])
                visited.add(node)
                while queue:
                    curr = queue.popleft()
                    for nxt in self.adj[curr]:
                        if nxt not in visited:
                            visited.add(nxt)
                            queue.append(nxt)
        return components
