"""Problem 01 — Dependency Inversion Container

Topic: 05 SOLID Principles Clean Architecture
Target: Production-grade implementation

Resolve dependency injection registrations with circular dependency detection.

Example:
    >>> dependency_inversion_container({'Controller': ['Service'], 'Service': ['Repository'], 'Repository': ['Database'], 'Database': []})
    ['Database', 'Repository', 'Service', 'Controller']

Hints:
    Hint 1: This is really a topological sort over a dependency graph --
        a service can only be instantiated after everything it depends on
        already exists.
    Hint 2: Use Kahn's algorithm: build an indegree count and an adjacency
        list from dependency -> dependent edges, then repeatedly pop
        nodes with indegree 0 from a sorted, deterministic queue and
        decrement their neighbors' indegree.
    Hint 3: If the resulting order has fewer entries than there are
        services, a cycle exists and you must raise
        `ValueError("Circular dependency detected")`; a dependency named
        only as a value (never its own top-level key) must still be
        registered as a node in the graph.
"""

from __future__ import annotations


def dependency_inversion_container(bindings: dict[str, list[str]]) -> list[str]:
    """bindings maps service_name -> list of dependency service names.
    Return valid instantiation order (topological sort).
    Raise ValueError("Circular dependency detected") if a cycle exists.
    """
    raise NotImplementedError("Implement dependency_inversion_container")
