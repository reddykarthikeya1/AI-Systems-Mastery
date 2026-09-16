"""Starter template for DAGAndTraversalEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class GraphEngine(Generic[T]):
    """Adjacency list graph with BFS, DFS, and Topological Sort."""

    def __init__(self, directed: bool = False) -> None:
        raise NotImplementedError

    def add_edge(self, u: T, v: T) -> None:
        raise NotImplementedError

    def bfs(self, start: T) -> list[T]:
        raise NotImplementedError

    def dfs(self, start: T) -> list[T]:
        raise NotImplementedError

    def topological_sort(self) -> list[T]:
        """Kahn's algorithm for DAGs. Raises ValueError if cycle detected."""
        raise NotImplementedError

    def count_connected_components(self) -> int:
        raise NotImplementedError
