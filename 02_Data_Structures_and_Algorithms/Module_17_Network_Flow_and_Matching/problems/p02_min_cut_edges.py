"""Problem 02 - Which Edges Are the Bottleneck?

Pattern:    Max-flow min-cut
Difficulty: Hard
Target:     Time O(V * E^2)

Return the edges of a minimum cut, sorted, as ``(from, to)`` pairs:
the cheapest set of edges whose removal leaves no path from ``source`` to
``sink``.

Constraints
- ``2 <= nodes <= 200``, ``0 <= len(edges) <= 2000``

Example
    min_cut_edges(4, [(0,1,10),(1,3,3),(0,2,5),(2,3,5)], 0, 3) -> [(0, 2), (1, 3)]

The capacities of the edges you return must sum to the maximum flow. If they do
not, you have a bug - that equality is a theorem, not a coincidence.

A graph can have several different minimum cuts, all of the same capacity. This
one also has `[(1, 3), (2, 3)]`, which is equally valid. Return the one you
reach by exploring from the source in the residual graph - the *source-minimal*
cut - because that is the one the tests expect and the one the standard method
produces.

Example:
    >>> min_cut_edges(4, [(0, 1, 10), (1, 3, 3), (0, 2, 5), (2, 3, 5)], 0, 3)
    [(0, 2), (1, 3)]

Hints - read one at a time, and try again between each.

    Hint 1: Run max flow first. The cut is read off the graph that is left behind.
    Hint 2: From the source, explore every edge that still has capacity REMAINING. That set of nodes is the source side.
    Hint 3: The cut is every original edge whose tail is reachable and whose head is not. Use the residual capacities for the exploration, not the original ones.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def min_cut_edges(nodes: int, edges: list[tuple[int, int, int]],
                  source: int, sink: int) -> list[tuple[int, int]]:
    raise NotImplementedError("implement min_cut_edges")
