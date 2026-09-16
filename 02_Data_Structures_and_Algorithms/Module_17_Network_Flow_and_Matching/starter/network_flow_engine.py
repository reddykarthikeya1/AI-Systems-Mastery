"""Starter template for the network flow engine.

Implement each piece. Run the shipped tests against your work:

    cd starter
    python -m pytest ../project_solution -q

They must FAIL until you have written the code.

Build order that works: `FlowNetwork` first (get `add_edge` and its residual
partner right, because everything depends on it), then `edmonds_karp`, then
`min_cut`, then `dinic`, then the two applications.
"""
from __future__ import annotations

INF = float("inf")


class FlowNetwork:
    """A directed graph with capacities.

    Store edges in one flat list in pairs, so edge `i` and its residual partner
    are `i` and `i ^ 1`. That is what makes "push forward, credit backward" two
    lines instead of a lookup.
    """

    def __init__(self, nodes: int) -> None:
        raise NotImplementedError("implement FlowNetwork.__init__")

    def add_edge(self, source: int, target: int, capacity: int) -> int:
        """Add source -> target, plus a residual edge of capacity 0 the other
        way. Return the forward edge's id."""
        raise NotImplementedError("implement FlowNetwork.add_edge")

    def flow_on(self, edge_id: int) -> int:
        """How much is flowing along an edge: original capacity - remaining."""
        raise NotImplementedError("implement FlowNetwork.flow_on")

    def reset(self) -> None:
        raise NotImplementedError("implement FlowNetwork.reset")


def edmonds_karp(network: FlowNetwork, source: int, sink: int) -> int:
    """Max flow, always augmenting along a SHORTEST path (so: BFS)."""
    raise NotImplementedError("implement edmonds_karp")


def dinic(network: FlowNetwork, source: int, sink: int) -> int:
    """Max flow via level graphs and blocking flows."""
    raise NotImplementedError("implement dinic")


def min_cut(network: FlowNetwork, source: int,
            sink: int) -> tuple[int, list[tuple[int, int]]]:
    """Return (cut value, edges crossing the cut).

    Run the flow, then explore the RESIDUAL graph from the source.
    """
    raise NotImplementedError("implement min_cut")


def bipartite_matching(left: int, right: int,
                       edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Maximum matching, expressed as a unit-capacity flow problem."""
    raise NotImplementedError("implement bipartite_matching")


def greedy_matching(left: int, right: int,
                    edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Take each edge if both endpoints are still free. Deliberately not
    maximum - a test pins down a case where it loses."""
    raise NotImplementedError("implement greedy_matching")


def max_profit_projects(profits: dict[str, int], costs: dict[str, int],
                        requires: dict[str, list[str]]) -> tuple[int, list[str]]:
    """Project selection: answer is total profit minus the minimum cut."""
    raise NotImplementedError("implement max_profit_projects")
