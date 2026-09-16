"""Problem 03 — Topological Sort

Pattern:    Kahn's algorithm
Difficulty: Medium
Target:     Time O((n + E) log n), Space O(n + E)

Nodes ``0..n-1`` with directed edges ``(u, v)`` meaning *u must come before v*.
Return a valid topological ordering, or ``[]`` if the graph has a cycle.

To make the output deterministic, always take the smallest available node next.

Constraints
- ``0 <= n <= 10**5``

Example
    topological_order(4, [(0, 1), (1, 2), (2, 3)]) -> [0, 1, 2, 3]
    topological_order(2, [(0, 1), (1, 0)])         -> []

Hints — read one at a time, and try again between each.

    Hint 1: A node can be emitted once every prerequisite is already emitted - that is, once its in-degree reaches 0.
    Hint 2: Compute all in-degrees, seed a queue with the zero-in-degree nodes, and each time you emit a node decrement its successors.
    Hint 3: Kahn's algorithm doubles as cycle detection for free: if you emit fewer than n nodes, the remainder are stuck in a cycle. Use a heap instead of a plain queue to always take the smallest available node.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def topological_order(n: int, edges: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError("implement topological_order")
