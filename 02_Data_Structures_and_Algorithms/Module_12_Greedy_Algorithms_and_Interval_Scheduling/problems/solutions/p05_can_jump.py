"""Reference solution — Problem 05: Jump Game

Pattern:    Greedy reachability
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, jump in enumerate(nums):
        # Standing beyond everything previously reachable means we never got here.
        if i > reach:
            return False
        reach = max(reach, i + jump)
        if reach >= len(nums) - 1:
            return True          # the end is already within reach
    return True
