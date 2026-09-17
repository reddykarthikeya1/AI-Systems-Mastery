"""Problem 01 — Bidirectional Graph Expansion

Topic: 16 Neo4j Graph Databases Cypher
Target: Production-grade implementation

Find shortest path length between start and target nodes within max_depth.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bidirectional_graph_expansion(adj: dict[str, list[str]], start: str, target: str, max_depth: int = 5) -> int:
    """Return shortest distance between start and target using bidirectional BFS.
    Return -1 if disconnected or path length > max_depth.
    """
    raise NotImplementedError("Implement bidirectional_graph_expansion")
