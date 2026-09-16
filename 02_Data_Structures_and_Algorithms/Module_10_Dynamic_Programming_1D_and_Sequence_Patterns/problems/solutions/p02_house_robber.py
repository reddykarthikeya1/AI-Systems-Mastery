"""Reference solution — Problem 02: House Robber

Pattern:    1D DP with a skip constraint
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def house_robber(nums: list[int]) -> int:
    # `skip` is the best total not using the previous house; `take` is the best
    # total that may use it. Two rolling values, no array.
    skip, take = 0, 0
    for x in nums:
        skip, take = take, max(take, skip + x)
    return take
