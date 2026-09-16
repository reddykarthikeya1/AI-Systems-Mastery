"""Reference solution — Problem 07: Subarray Sums Divisible By K

Pattern:    Prefix sums + modular arithmetic
Complexity: Time O(n), Space O(k)
"""

from __future__ import annotations


def subarrays_div_by_k(nums: list[int], k: int) -> int:
    # {remainder: how many prefixes had it}. Seed remainder 0 once for the
    # empty prefix, which is what makes subarrays starting at index 0 count.
    counts = {0: 1}
    running = 0
    total = 0

    for x in nums:
        running += x
        # Python's % is already non-negative for positive k; C/Java would need
        # ((r % k) + k) % k here.
        r = running % k
        total += counts.get(r, 0)
        counts[r] = counts.get(r, 0) + 1

    return total
