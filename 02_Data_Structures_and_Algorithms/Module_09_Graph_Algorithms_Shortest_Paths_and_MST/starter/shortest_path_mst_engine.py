"""Starter template for ShortestPathMSTEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class ShortestPathMSTEngine(Generic[T]):
    """Dijkstra, Bellman-Ford, and Kruskal's MST algorithms."""

    def __init__(self) -> None:
        raise NotImplementedError

    def add_edge(self, u: T, v: T, weight: float, directed: bool = False) -> None:
        raise NotImplementedError

    def dijkstra(self, start: T) -> dict[T, float]:
        raise NotImplementedError

    def bellman_ford(self, start: T) -> dict[T, float]:
        """Find shortest paths with negative weights. Raises ValueError on negative cycle."""
        raise NotImplementedError

    def kruskal_mst(self) -> tuple[float, list[tuple[T, T, float]]]:
        """Compute Minimum Spanning Tree using Kruskal's algorithm."""
        raise NotImplementedError
