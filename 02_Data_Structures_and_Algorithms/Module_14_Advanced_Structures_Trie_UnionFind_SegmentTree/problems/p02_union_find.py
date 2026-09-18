"""Problem 02 — Union-Find With Path Compression

Pattern:    Disjoint set union
Difficulty: Medium
Target:     Time O(α(n)) amortised per op, Space O(n)

Simulate a disjoint-set structure over ``0..n-1`` supporting:

* ``("union", a, b)`` — merge the two sets; returns nothing
* ``("connected", a, b)`` — are they in the same set?
* ``("count", 0, 0)`` — how many disjoint sets remain?

Return the results of ``connected`` and ``count``, in order.

Constraints
- ``1 <= n <= 10**5``, ``1 <= len(ops) <= 10**5``
- must be near-O(1) amortised per operation

Example
    n = 4, ops = [("connected",0,1), ("union",0,1), ("connected",0,1), ("count",0,0)]
    -> [False, True, 3]

Example:
    >>> ops = [("connected", 0, 1), ("union", 0, 1), ("connected", 0, 1), ("count", 0, 0)]
    >>> simulate_union_find(4, ops)
    [False, True, 3]

Hints — read one at a time, and try again between each.

    Hint 1: `parent[x]` points toward the representative of x's set. `find` walks to the root.
    Hint 2: Path compression: after finding the root, point every node on the path directly at it. Without this, `find` degrades to O(n) on a chain.
    Hint 3: Union by size (attach the smaller tree under the larger) keeps trees shallow. Maintain the set count by decrementing on every successful merge, rather than recounting.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def simulate_union_find(n: int, ops: list[tuple[str, int, int]]) -> list[bool | int]:
    raise NotImplementedError("implement simulate_union_find")
