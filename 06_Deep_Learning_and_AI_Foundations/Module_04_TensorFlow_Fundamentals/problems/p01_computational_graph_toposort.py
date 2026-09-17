"""Problem 01 — Computational Graph Toposort

Topic: 04 TensorFlow Fundamentals
Target: Production-grade implementation

Topologically order nodes in static computational graph.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def computational_graph_toposort(nodes: dict[str, list[str]]) -> list[str]:
    """nodes maps node_name -> list of dependency input node names.
    Return execution sequence such that all dependencies execute before consumer.
    """
    raise NotImplementedError("Implement computational_graph_toposort")
