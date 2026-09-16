"""Reference solution — Problem 03: Segment Tree: Range Sum With Updates

Pattern:    Segment tree
Complexity: Time O(log n) per operation, Space O(n)
"""

from __future__ import annotations


def simulate_segment_tree(nums: list[int], ops: list[tuple[str, int, int]]) -> list[int]:
    n = len(nums)
    if n == 0:
        return []

    # Flat iterative segment tree: leaves at [n, 2n), internals at [1, n).
    tree = [0] * (2 * n)
    tree[n : 2 * n] = nums
    for i in range(n - 1, 0, -1):
        tree[i] = tree[2 * i] + tree[2 * i + 1]

    out: list[int] = []

    for name, a, b in ops:
        if name == "update":
            i = a + n
            tree[i] = b
            # Walk up recomputing each parent from its two children.
            i //= 2
            while i >= 1:
                tree[i] = tree[2 * i] + tree[2 * i + 1]
                i //= 2
        elif name == "query":
            lo, hi = a + n, b + n + 1       # half-open [lo, hi)
            total = 0
            while lo < hi:
                # A left index that is a right child must be taken alone.
                if lo & 1:
                    total += tree[lo]
                    lo += 1
                # A right bound that is a right child means hi-1 is included.
                if hi & 1:
                    hi -= 1
                    total += tree[hi]
                lo //= 2
                hi //= 2
            out.append(total)
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
