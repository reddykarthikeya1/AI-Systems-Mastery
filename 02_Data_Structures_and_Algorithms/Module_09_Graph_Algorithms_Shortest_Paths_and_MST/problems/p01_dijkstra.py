"""Problem 01 — Dijkstra's Shortest Paths

Pattern:    Dijkstra with a heap
Difficulty: Medium
Target:     Time O(E log V), Space O(V + E)

Directed edges ``(u, v, w)`` with ``w >= 0``. Return a list of shortest
distances from ``source`` to every node, using ``float('inf')`` for unreachable
nodes.

Constraints
- ``1 <= n <= 10**5``, ``0 <= len(edges) <= 2 * 10**5``
- ``0 <= w <= 10**6``
- parallel edges and self-loops may appear

Example
    dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0) -> [0, 3, 1]

Hints — read one at a time, and try again between each.

    Hint 1: Always expand the unfinalised node with the smallest known distance. A min-heap gives you that.
    Hint 2: Python's heapq has no decrease-key, so push a new (dist, node) entry instead of updating an old one. The heap will then hold stale entries.
    Hint 3: Skip a popped entry whose distance is worse than the best you have already recorded - that is how you discard the stale ones. Without that check the algorithm still terminates but does redundant work.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def dijkstra(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float]:
    raise NotImplementedError("implement dijkstra")
