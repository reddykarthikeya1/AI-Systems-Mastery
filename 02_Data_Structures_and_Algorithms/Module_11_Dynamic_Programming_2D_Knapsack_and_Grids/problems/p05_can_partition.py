"""Problem 05 — Partition Equal Subset Sum

Pattern:    Subset-sum DP
Difficulty: Medium
Target:     Time O(n * total/2), Space O(total/2)

Return True if ``nums`` can be split into two subsets with equal sums.

Constraints
- ``1 <= len(nums) <= 200``
- ``1 <= nums[i] <= 100``

Example
    can_partition([1, 5, 11, 5]) -> True     ([1,5,5] and [11])
    can_partition([1, 2, 3, 5])  -> False

Example:
    >>> can_partition([1, 5, 11, 5])
    True
    >>> can_partition([1, 2, 3, 5])
    False

Hints — read one at a time, and try again between each.

    Hint 1: If the total is odd, no split can be equal - answer False immediately.
    Hint 2: Otherwise you need a subset summing to exactly total // 2. That is subset-sum, which is 0/1 knapsack with values equal to weights.
    Hint 3: Use a boolean array over achievable sums, and iterate DOWNWARD for the same reason as the previous problem: upward lets one number be used twice.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def can_partition(nums: list[int]) -> bool:
    raise NotImplementedError("implement can_partition")
