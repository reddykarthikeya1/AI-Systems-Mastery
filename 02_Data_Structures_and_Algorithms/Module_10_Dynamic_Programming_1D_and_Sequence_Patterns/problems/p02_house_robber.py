"""Problem 02 — House Robber

Pattern:    1D DP with a skip constraint
Difficulty: Medium
Target:     Time O(n), Space O(1)

You may not rob two adjacent houses. Return the maximum total you can take.

Constraints
- ``0 <= len(nums) <= 100``
- ``0 <= nums[i] <= 400``

Example
    house_robber([1, 2, 3, 1]) -> 4     (houses 0 and 2)
    house_robber([2, 7, 9, 3, 1]) -> 12 (houses 0, 2, 4)

Example:
    >>> house_robber([1, 2, 3, 1])
    4
    >>> house_robber([2, 7, 9, 3, 1])
    12

Hints — read one at a time, and try again between each.

    Hint 1: At each house you have exactly two choices: rob it, or skip it.
    Hint 2: If you rob house i you add nums[i] to the best total from house i-2. If you skip it, your total is the best from house i-1.
    Hint 3: best(i) = max(best(i-1), best(i-2) + nums[i]). Again only two previous values matter, so O(1) space.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def house_robber(nums: list[int]) -> int:
    raise NotImplementedError("implement house_robber")
