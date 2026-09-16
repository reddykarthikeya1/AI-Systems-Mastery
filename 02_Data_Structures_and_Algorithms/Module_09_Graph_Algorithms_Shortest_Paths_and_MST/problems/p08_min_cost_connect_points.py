"""Problem 08 — Minimum Cost To Connect All Points

Pattern:    MST on a complete graph
Difficulty: Hard
Target:     Time O(n^2 log n), Space O(n)

Connect all points so every pair is reachable, minimising total cost, where the
cost between two points is their Manhattan distance.

Constraints
- ``1 <= len(points) <= 1000``
- ``-10**6 <= x, y <= 10**6``

Example
    min_cost_connect_points([(0,0),(2,2),(3,10),(5,2),(7,0)]) -> 20

Hints — read one at a time, and try again between each.

    Hint 1: 'Connect everything at minimum total cost' is a minimum spanning tree.
    Hint 2: The graph is complete and implicit: every pair of points is an edge. For n = 1000 that is ~500,000 edges, which is fine to materialise.
    Hint 3: Prim is the better fit on a dense graph - it never needs the full edge list at once. Either algorithm works here; Kruskal on 500k edges costs the sort.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def min_cost_connect_points(points: list[tuple[int, int]]) -> int:
    raise NotImplementedError("implement min_cost_connect_points")
