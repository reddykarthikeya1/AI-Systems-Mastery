"""Problem 04 - Edge-Disjoint Paths

Pattern:    Unit-capacity flow
Difficulty: Medium
Target:     Time O(V * E^2)

How many paths from ``source`` to ``sink`` can you find that share
no edge? ``edges`` is a list of ``(from, to)`` with no capacities.

Constraints
- ``2 <= nodes <= 200``, ``0 <= len(edges) <= 2000``

Example
    edge_disjoint_paths(4, [(0,1),(1,3),(0,2),(2,3),(0,3)], 0, 3) -> 3

This is the network-reliability question: how many independent link failures can
the route survive? Menger's theorem says the answer equals the smallest number
of edges whose removal disconnects the two nodes - which is a minimum cut, which
is a maximum flow.

Hints - read one at a time, and try again between each.

    Hint 1: Give every edge capacity 1.
    Hint 2: Then one unit of flow is one path, and the capacity-1 constraint is exactly "no edge is reused".
    Hint 3: The answer is the max flow value. Nothing else to do.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def edge_disjoint_paths(nodes: int, edges: list[tuple[int, int]],
                        source: int, sink: int) -> int:
    raise NotImplementedError("implement edge_disjoint_paths")
