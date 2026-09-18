"""Problem 02 — Count Connected Components

Pattern:    BFS/DFS over an adjacency list
Difficulty: Medium
Target:     Time O(n + E), Space O(n + E)

Nodes are labelled ``0..n-1``. Return the number of connected components in the
undirected graph.

Constraints
- ``0 <= n <= 10**5``
- edges may repeat, and self-loops may appear

Example
    count_components(5, [(0, 1), (1, 2), (3, 4)]) -> 2
    count_components(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) -> 1

Example:
    >>> count_components(5, [(0, 1), (1, 2), (3, 4)])
    2
    >>> count_components(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    1

Hints — read one at a time, and try again between each.

    Hint 1: Build an adjacency list first - scanning the edge list per node would be O(n * E).
    Hint 2: Then start a traversal from every node you have not yet visited.
    Hint 3: Each such start is exactly one new component. Isolated nodes with no edges still count as components of size 1.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    raise NotImplementedError("implement count_components")
