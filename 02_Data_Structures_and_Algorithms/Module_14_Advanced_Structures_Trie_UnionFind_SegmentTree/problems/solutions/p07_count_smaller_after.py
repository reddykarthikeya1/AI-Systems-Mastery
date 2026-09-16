"""Reference solution — Problem 07: Count Of Smaller Numbers After Self

Pattern:    Fenwick tree (BIT)
Complexity: Time O(n log n), Space O(n)
"""

from __future__ import annotations


def count_smaller_after(nums: list[int]) -> list[int]:
    n = len(nums)
    if n == 0:
        return []

    # Coordinate compression: map values to 1..m ranks so the tree stays small
    # and handles negatives without offsetting.
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(ranks)

    tree = [0] * (m + 1)

    def add(i: int) -> None:
        while i <= m:
            tree[i] += 1
            i += i & -i         # i & -i isolates the lowest set bit

    def prefix(i: int) -> int:
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    out = [0] * n
    # Right to left, so everything already inserted lies to the right.
    for idx in range(n - 1, -1, -1):
        r = ranks[nums[idx]]
        out[idx] = prefix(r - 1)    # strictly smaller
        add(r)
    return out
