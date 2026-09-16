"""Reference solution — Problem 07: Redundant Connection

Pattern:    Union-find cycle detection
Complexity: Time O(n α(n)), Space O(n)
"""

from __future__ import annotations


def redundant_connection(edges: list[tuple[int, int]]) -> tuple[int, int]:
    # Size by the largest label present, NOT by len(edges): a genuine tree has
    # one more node than it has edges, and sizing by the edge count IndexErrors.
    largest = max((max(u, v) for u, v in edges), default=0)
    parent = list(range(largest + 1))

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            # Both ends already connected, so this edge closes the cycle.
            return (u, v)
        parent[rv] = ru

    raise ValueError("no redundant edge found - input was already a tree")
