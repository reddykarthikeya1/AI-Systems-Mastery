"""Reference solution — Problem 03: Longest Consecutive Sequence

Pattern:    Hash set + sequence-start check
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def longest_consecutive(nums: list[int]) -> int:
    present = set(nums)
    best = 0

    for x in present:
        # Only walk from a genuine run start, or each run is re-walked once per
        # member and the whole thing degrades to O(n^2).
        if x - 1 in present:
            continue
        length = 1
        cur = x
        while cur + 1 in present:
            cur += 1
            length += 1
        best = max(best, length)

    return best
