"""Problem 07 — Count Of Smaller Numbers After Self

Pattern:    Fenwick tree (BIT)
Difficulty: Hard
Target:     Time O(n log n), Space O(n)

For each index, count how many numbers to its **right** are strictly smaller.

Constraints
- ``0 <= len(nums) <= 10**5``  -> O(n log n) required
- ``-10**4 <= nums[i] <= 10**4``

Example
    count_smaller_after([5, 2, 6, 1]) -> [2, 1, 1, 0]

Example:
    >>> count_smaller_after([5, 2, 6, 1])
    [2, 1, 1, 0]

Hints — read one at a time, and try again between each.

    Hint 1: The brute force is O(n^2). What is it repeating? A count over a suffix that barely changes.
    Hint 2: Walk the array from RIGHT to left, maintaining a frequency structure of the values seen so far. For each element you need 'how many seen values are less than this one' - a prefix sum over frequencies.
    Hint 3: A Fenwick tree (binary indexed tree) does point-update and prefix-sum in O(log n). Compress the values to ranks first so the tree is only as large as the number of distinct values.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def count_smaller_after(nums: list[int]) -> list[int]:
    raise NotImplementedError("implement count_smaller_after")
