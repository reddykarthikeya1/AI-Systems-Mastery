"""Problem 04 — Detect A Cycle In A Directed Graph

Pattern:    DFS with three colours
Difficulty: Medium
Target:     Time O(n + E), Space O(n + E)

Return True if the directed graph contains a cycle.

Constraints
- ``0 <= n <= 10**5``

Example
    has_cycle_directed(2, [(0, 1), (1, 0)]) -> True
    has_cycle_directed(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) -> False

The second example is a **diamond**: node 3 is reached twice, by two different
paths, and the graph is a perfectly valid DAG. A solution that flags a cycle
whenever it re-encounters a visited node returns True here, which is wrong.

Hints — read one at a time, and try again between each.

    Hint 1: Two states (visited / not visited) is not enough. Re-encountering a visited node is only a cycle if that node is still ON the current DFS path.
    Hint 2: Use three: WHITE (untouched), GREY (on the current path), BLACK (finished, all descendants explored).
    Hint 3: A cycle exists exactly when DFS finds an edge to a GREY node - a back edge. An edge to a BLACK node is just a re-convergence, which a DAG is allowed to have.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def has_cycle_directed(n: int, edges: list[tuple[int, int]]) -> bool:
    raise NotImplementedError("implement has_cycle_directed")
