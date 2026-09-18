"""Problem 02 — Bellman-Ford With Negative Cycle Detection

Pattern:    Bellman-Ford
Difficulty: Hard
Target:     Time O(V*E), Space O(V)

Directed edges ``(u, v, w)`` where ``w`` **may be negative**. Return the
shortest distances from ``source``, or ``None`` if a negative cycle is reachable
from the source (in which case no shortest path is well defined).

Constraints
- ``1 <= n <= 500``, ``0 <= len(edges) <= 10**4``
- ``-10**4 <= w <= 10**4``

Example
    bellman_ford(3, [(0, 1, 4), (0, 2, 1), (2, 1, -2)], 0) -> [0, -1, 1]
    bellman_ford(2, [(0, 1, 1), (1, 0, -3)], 0)            -> None

Note the first example: Dijkstra returns ``[0, 4, 1]`` here — wrong, and
without any error. Dijkstra finalises a node the first time it is reached, and a
negative edge can improve a node after it has been finalised.

Example:
    >>> bellman_ford(3, [(0, 1, 4), (0, 2, 1), (2, 1, -2)], 0)
    [0, -1, 1]
    >>> bellman_ford(2, [(0, 1, 1), (1, 0, -3)], 0) is None
    True

Hints — read one at a time, and try again between each.

    Hint 1: A shortest path visits at most n-1 edges, so relaxing every edge n-1 times is enough to propagate all distances.
    Hint 2: After those n-1 rounds, distances are final IF there is no negative cycle.
    Hint 3: So do one extra round: if any edge can still be relaxed, a negative cycle is reachable. Relaxing from an unreachable node (inf) must be skipped, or inf + negative looks like an improvement.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def bellman_ford(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float] | None:
    raise NotImplementedError("implement bellman_ford")
