"""Problem 01 — Two Sum

Pattern:    Hash map complement
Difficulty: Easy
Target:     Time O(n), Space O(n)

Return the indices of the two numbers that add up to ``target``.

Exactly one solution exists, and you may not use the same element twice. Return
the indices in ascending order.

Constraints
- ``2 <= len(nums) <= 10**4``  -> O(n) is expected, O(n^2) will not do
- ``-10**9 <= nums[i], target <= 10**9``

Example
    two_sum([2, 7, 11, 15], 9) -> [0, 1]

Hints — read one at a time, and try again between each.

    Hint 1: For each element you need to know whether target - x appeared earlier.
    Hint 2: 'Did I see X earlier, and at what index?' is exactly a dict lookup.
    Hint 3: Check the complement BEFORE inserting the current element, or a value equal to target/2 will match itself.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> list[int]:
    raise NotImplementedError("implement two_sum")
