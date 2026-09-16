"""Reference solution — Problem 05: Partition Equal Subset Sum

Pattern:    Subset-sum DP
Complexity: Time O(n * total/2), Space O(total/2)
"""

from __future__ import annotations


def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False        # an odd total cannot split evenly

    target = total // 2
    achievable = [False] * (target + 1)
    achievable[0] = True    # the empty subset sums to zero

    for x in nums:
        # Downward again: upward would let x be counted more than once.
        for s in range(target, x - 1, -1):
            if achievable[s - x]:
                achievable[s] = True
        if achievable[target]:
            return True     # early exit once the target is reachable

    return achievable[target]
