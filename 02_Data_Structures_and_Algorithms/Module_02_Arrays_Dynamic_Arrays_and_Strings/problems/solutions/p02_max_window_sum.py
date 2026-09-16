"""Reference solution — Problem 02: Maximum Sum Of A Fixed-Size Window

Pattern:    Sliding window (fixed)
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def max_window_sum(nums: list[int], k: int) -> int:
    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError(f"window size {k} is invalid for an array of length {n}")

    total = sum(nums[:k])
    best = total
    for i in range(k, n):
        # O(1) per step: one element enters, one leaves.
        total += nums[i] - nums[i - k]
        best = max(best, total)
    return best
