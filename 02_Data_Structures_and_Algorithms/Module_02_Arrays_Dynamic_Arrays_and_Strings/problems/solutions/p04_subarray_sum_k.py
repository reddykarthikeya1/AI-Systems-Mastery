"""Reference solution — Problem 04: Count Subarrays Summing To K

Pattern:    Prefix sums + hash map
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def subarray_sum_k(nums: list[int], k: int) -> int:
    # {prefix_sum: how many times it has occurred}. The seed {0: 1} represents
    # the empty prefix, which is what makes a subarray starting at index 0
    # countable.
    counts: dict[int, int] = {0: 1}
    running = 0
    total = 0

    for x in nums:
        running += x
        # Any earlier prefix equal to running - k closes a subarray summing to k.
        total += counts.get(running - k, 0)
        counts[running] = counts.get(running, 0) + 1

    return total
