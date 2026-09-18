"""Problem 06 — Minimum Spanning Tree (Prim)

Pattern:    Prim with a heap
Difficulty: Medium
Target:     Time O(E log V), Space O(V + E)

Same problem as Kruskal, solved the other way: grow one tree outward from a
single node, always taking the cheapest edge that leaves the tree.

Return the MST weight, or ``-1`` if disconnected.

Constraints
- ``1 <= n <= 10**5``

Example
    prim_mst(4, [(0,1,1),(1,2,2),(2,3,3),(0,3,10)]) -> 6

Both algorithms are `O(E log V)`. Prim wins on dense graphs, Kruskal on sparse
ones and when the edges arrive already sorted.

Example:
    >>> prim_mst(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)])
    6

Hints — read one at a time, and try again between each.

    Hint 1: Keep the tree as a visited set. The candidate edges are those with exactly one endpoint inside it.
    Hint 2: A min-heap of (weight, node) gives the cheapest candidate in O(log V).
    Hint 3: Pop until you find a node not yet in the tree - stale entries are normal, exactly as in Dijkstra. If you finish with fewer than n nodes, the graph was disconnected.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def prim_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    raise NotImplementedError("implement prim_mst")
