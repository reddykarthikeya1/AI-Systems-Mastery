"""Reference solution — Problem 07: Maximum Product Subarray

Pattern:    1D DP with two-value state
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def max_product_subarray(nums: list[int]) -> int:
    if not nums:
        raise ValueError("nums must be non-empty")

    best = cur_max = cur_min = nums[0]

    for x in nums[1:]:
        # Both must be computed from the PREVIOUS pair, so capture cur_max
        # before it is overwritten.
        candidates = (x, cur_max * x, cur_min * x)
        cur_max = max(candidates)
        cur_min = min(candidates)
        best = max(best, cur_max)

    return best
