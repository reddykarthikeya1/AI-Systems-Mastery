"""Reference solution — Problem 07: Three Sum

Pattern:    Sorting + two pointers
Complexity: Time O(n^2), Space O(1) beyond the output
"""

from __future__ import annotations


def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    out: list[list[int]] = []

    for i in range(n - 2):
        # Skip a repeated anchor, or we emit the same triple twice.
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        # Sorted, so once the anchor is positive no triple can sum to zero.
        if nums[i] > 0:
            break

        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                # Advance past duplicates on both sides.
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1

    return out
