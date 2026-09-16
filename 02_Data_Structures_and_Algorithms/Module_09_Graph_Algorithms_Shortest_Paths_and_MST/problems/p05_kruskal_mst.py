"""Problem 05 — Minimum Spanning Tree (Kruskal)

Pattern:    Sort edges + union-find
Difficulty: Medium
Target:     Time O(E log E), Space O(V)

Undirected weighted edges ``(u, v, w)``. Return the total weight of a minimum
spanning tree, or ``-1`` if the graph is not connected.

Constraints
- ``1 <= n <= 10**5``, ``0 <= len(edges) <= 2 * 10**5``
- weights may be negative

Example
    kruskal_mst(4, [(0,1,1),(1,2,2),(2,3,3),(0,3,10)]) -> 6

Hints — read one at a time, and try again between each.

    Hint 1: Consider the edges in increasing weight order and take an edge only if it joins two currently separate components.
    Hint 2: 'Are these two nodes already connected?' with merging is exactly union-find.
    Hint 3: Stop once you have taken n-1 edges. If you run out of edges before that, the graph was disconnected. Use path compression and union by size or the union-find degrades to a linked list.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    raise NotImplementedError("implement kruskal_mst")
