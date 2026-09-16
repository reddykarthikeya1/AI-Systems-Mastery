"""Problem 01 - Maximum Flow

Pattern:    Edmonds-Karp
Difficulty: Medium
Target:     Time O(V * E^2)

Given a directed graph with capacities, return the maximum flow
from ``source`` to ``sink``.

``edges`` is a list of ``(from, to, capacity)``. There may be parallel edges.

Constraints
- ``2 <= nodes <= 200``, ``0 <= len(edges) <= 2000``, ``0 <= capacity <= 10**6``

Example
    max_flow_value(4, [(0,1,10),(1,3,3),(0,2,5),(2,3,5)], 0, 3) -> 8

Everything else in this module is this function with a different graph in front
of it. Get it right once.

Hints - read one at a time, and try again between each.

    Hint 1: Store edges in pairs so edge `i` and its residual partner are `i` and `i ^ 1`. Add the reverse edge with capacity 0 at the same time as the forward one.
    Hint 2: Repeatedly BFS for a path with spare capacity, find the smallest capacity along it, and push that much.
    Hint 3: Pushing means subtracting from the forward edge AND adding the same amount to its partner. Skip the second half and you get a wrong, too-small answer on any graph that needs to reroute.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def max_flow_value(nodes: int, edges: list[tuple[int, int, int]],
                   source: int, sink: int) -> int:
    raise NotImplementedError("implement max_flow_value")
