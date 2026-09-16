"""Problem 03 — Network Delay Time

Pattern:    Dijkstra, single-source maximum
Difficulty: Medium
Target:     Time O(E log V), Space O(V + E)

``times[i] = (u, v, w)`` is a directed edge with travel time ``w``. A signal
starts at node ``k``. Return the time for **all** ``n`` nodes to receive it, or
``-1`` if some node never does.

Nodes are labelled ``1..n``.

Constraints
- ``1 <= n <= 100``
- ``1 <= u, v <= n``, ``0 <= w <= 100``

Example
    network_delay(4, [(2,1,1),(2,3,1),(3,4,1)], 2) -> 2

Hints — read one at a time, and try again between each.

    Hint 1: The time for all nodes to receive it is the MAXIMUM of the shortest distances - not the sum.
    Hint 2: So run Dijkstra from k and take the maximum.
    Hint 3: Watch the 1-based labelling. And if any distance is still infinite, return -1.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations

from p01_dijkstra import dijkstra


def network_delay(n: int, times: list[tuple[int, int, int]], k: int) -> int:
    raise NotImplementedError("implement network_delay")
