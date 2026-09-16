"""Reference solution — Problem 01: Two Sum

Pattern:    Hash map complement
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        complement = target - x
        # Look up before inserting: otherwise x could pair with itself when
        # 2 * x == target.
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []
