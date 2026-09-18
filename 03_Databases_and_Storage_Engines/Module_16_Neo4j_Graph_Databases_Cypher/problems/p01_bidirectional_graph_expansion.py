"""Problem 01 — Bidirectional Graph Expansion

Topic: 16 Neo4j Graph Databases Cypher
Target: Production-grade implementation

Find shortest path length between start and target nodes within max_depth.

Example:
    >>> adj = {'A': ['B'], 'B': ['A', 'C'], 'C': ['B', 'D'], 'D': ['C', 'E'], 'E': ['D']}
    >>> bidirectional_graph_expansion(adj, 'A', 'E', 5)
    4
    >>> bidirectional_graph_expansion(adj, 'A', 'E', 2)
    -1

Hints:
    Hint 1: Searching outward from both start and target at once lets you
        stop as soon as the two expanding frontiers touch, instead of
        exploring the whole graph outward from just one side.
    Hint 2: Keep two visited-distance dicts (one growing from start, one
        from target) and their current frontiers; on each round, expand
        whichever frontier is currently smaller using adj.get(u, []) to
        keep the search balanced.
    Hint 3: The moment a neighbor discovered from one side is already known
        to the other side, the shortest path length is the sum of the two
        partial distances plus 1 for the connecting edge — but that total
        must still be checked against max_depth before returning it (and a
        start == target query short-circuits to 0 before any search runs).
"""

from __future__ import annotations


def bidirectional_graph_expansion(adj: dict[str, list[str]], start: str, target: str, max_depth: int = 5) -> int:
    """Return shortest distance between start and target using bidirectional BFS.
    Return -1 if disconnected or path length > max_depth.
    """
    raise NotImplementedError("Implement bidirectional_graph_expansion")
