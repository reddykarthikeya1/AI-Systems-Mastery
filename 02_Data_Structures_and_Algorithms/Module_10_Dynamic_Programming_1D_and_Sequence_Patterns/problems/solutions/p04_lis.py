"""Reference solution — Problem 04: Longest Increasing Subsequence

Pattern:    Patience sorting / binary search DP
Complexity: Time O(n log n), Space O(n)
"""

from __future__ import annotations


def lis(nums: list[int]) -> int:
    import bisect

    # tails[k] = smallest possible tail of an increasing subsequence of length
    # k+1. Always sorted, which is what makes the binary search valid.
    tails: list[int] = []

    for x in nums:
        # bisect_left gives STRICTLY increasing; bisect_right would allow equal
        # values and compute the longest non-decreasing subsequence instead.
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x

    return len(tails)
