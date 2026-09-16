"""Problem 07 — Redundant Connection

Pattern:    Union-find cycle detection
Difficulty: Medium
Target:     Time O(n α(n)), Space O(n)

A tree on ``n`` nodes had one extra edge added, producing exactly one cycle.
Return the edge that can be removed to make it a tree again. If several
qualify, return the one that appears **last** in the input.

Nodes are labelled ``1..n``.

Constraints
- ``3 <= len(edges) <= 1000``

Example
    redundant_connection([(1, 2), (1, 3), (2, 3)]) -> (2, 3)

Hints — read one at a time, and try again between each.

    Hint 1: Process the edges in order, merging endpoints as you go.
    Hint 2: The first edge whose two endpoints are ALREADY in the same component is the one that closes the cycle.
    Hint 3: Because you scan in input order, that first such edge is also the last one that could be removed - which is what the problem asks for.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def redundant_connection(edges: list[tuple[int, int]]) -> tuple[int, int]:
    raise NotImplementedError("implement redundant_connection")
