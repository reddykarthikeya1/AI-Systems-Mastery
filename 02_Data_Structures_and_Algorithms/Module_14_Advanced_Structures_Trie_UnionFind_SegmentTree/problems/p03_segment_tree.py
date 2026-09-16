"""Problem 03 — Segment Tree: Range Sum With Updates

Pattern:    Segment tree
Difficulty: Hard
Target:     Time O(log n) per operation, Space O(n)

Support two operations on an array, both in ``O(log n)``:

* ``("update", i, value)`` — set ``nums[i] = value``; returns nothing
* ``("query", lo, hi)`` — the sum of ``nums[lo..hi]`` inclusive

Return the results of the queries, in order.

Constraints
- ``1 <= len(nums) <= 10**5``, ``1 <= len(ops) <= 10**5``

Example
    nums = [1, 3, 5], ops = [("query",0,2), ("update",1,2), ("query",0,2)]
    -> [9, 8]

Prefix sums give O(1) queries but O(n) updates. A plain array gives O(1)
updates but O(n) queries. A segment tree makes both O(log n), which is the right
trade when both are frequent.

Hints — read one at a time, and try again between each.

    Hint 1: Store the tree in a flat array of size 2n: leaves in the second half, internal nodes in the first, with node i's children at 2i and 2i+1.
    Hint 2: Building bottom-up means tree[i] = tree[2i] + tree[2i+1] for i from n-1 down to 1.
    Hint 3: For an update, write the leaf then walk up recomputing parents. For a query, walk lo and hi inward from the leaves, accumulating whichever side is not aligned with its parent. This iterative form avoids recursion entirely.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def simulate_segment_tree(nums: list[int], ops: list[tuple[str, int, int]]) -> list[int]:
    raise NotImplementedError("implement simulate_segment_tree")
