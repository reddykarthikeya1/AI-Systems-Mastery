"""Problem 05 - Vertex-Disjoint Paths

Pattern:    Node splitting
Difficulty: Hard
Target:     Time O(V * E^2)

Same question, stricter: the paths may not share any *node* either,
apart from ``source`` and ``sink``.

Constraints
- ``2 <= nodes <= 200``, ``0 <= len(edges) <= 2000``

Example
    vertex_disjoint_paths(4, [(0,1),(1,3),(0,2),(2,3),(0,3)], 0, 3) -> 3
    vertex_disjoint_paths(5, [(0,1),(1,2),(2,4),(0,3),(3,2)], 0, 4) -> 1

In the second example both routes must pass through node 2, so only one path can
use it. Flow has no notion of node capacity - so you have to give it one.

Hints - read one at a time, and try again between each.

    Hint 1: Split every node v into two, v_in and v_out, joined by one edge.
    Hint 2: Give that internal edge capacity 1 and it becomes "this node may be used once". Every original edge (u, v) becomes u_out -> v_in.
    Hint 3: The source and the sink must keep unlimited internal capacity, or you cap the answer at 1 by accident.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def vertex_disjoint_paths(nodes: int, edges: list[tuple[int, int]],
                          source: int, sink: int) -> int:
    raise NotImplementedError("implement vertex_disjoint_paths")
