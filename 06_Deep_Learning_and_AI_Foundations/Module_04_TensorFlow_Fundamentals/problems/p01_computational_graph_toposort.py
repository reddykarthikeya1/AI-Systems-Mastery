"""Problem 01 — Computational Graph Toposort

Topic: 04 TensorFlow Fundamentals
Target: Production-grade implementation

Topologically order nodes in static computational graph.

Example:
    >>> computational_graph_toposort({'Loss': ['Pred', 'Y'], 'Pred': ['W', 'X'], 'W': [], 'X': [], 'Y': []})
    ['W', 'X', 'Y', 'Pred', 'Loss']

Hints:
    Hint 1: This is Kahn's algorithm: a node is only ready to execute once
        every one of its dependencies has already been emitted, i.e. once
        its remaining "indegree" of unmet dependencies hits zero.
    Hint 2: Build an indegree count per node (how many deps it still needs)
        and a reverse map from each dependency to the nodes that depend on
        it; repeatedly pop a zero-indegree node, append it to the order,
        and decrement indegree for everything that depended on it.
    Hint 3: A dependency name can appear in some node's list without ever
        being a top-level key of `nodes` itself — register it with
        indegree 0 the first time you see it, don't assume every dependency
        is a dict key. Break ties between simultaneously-ready nodes by
        sorting alphabetically so the output order is deterministic.
"""

from __future__ import annotations


def computational_graph_toposort(nodes: dict[str, list[str]]) -> list[str]:
    """nodes maps node_name -> list of dependency input node names.
    Return execution sequence such that all dependencies execute before consumer.
    """
    raise NotImplementedError("Implement computational_graph_toposort")
