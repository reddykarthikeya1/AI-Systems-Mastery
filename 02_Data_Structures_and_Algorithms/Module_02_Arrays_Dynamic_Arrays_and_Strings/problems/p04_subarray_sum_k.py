"""Problem 04 — Count Subarrays Summing To K

Pattern:    Prefix sums + hash map
Difficulty: Medium
Target:     Time O(n), Space O(n)

Return the number of contiguous subarrays whose elements sum to exactly ``k``.

Constraints
- ``1 <= len(nums) <= 2 * 10**4``  -> O(n) expected
- ``-1000 <= nums[i] <= 1000`` — **values may be negative**
- ``-10**7 <= k <= 10**7``

Example
    subarray_sum_k([1, 1, 1], 2)  -> 2
    subarray_sum_k([1, 2, 3], 3)  -> 2

Read the previous problem again, then read this one. They look like the same
shape, and a sliding window is **wrong** here. Work out why before you start —
that reasoning is the point of this problem.

Example:
    >>> subarray_sum_k([1, 1, 1], 2)
    2
    >>> subarray_sum_k([1, 2, 3], 3)
    2

Hints — read one at a time, and try again between each.

    Hint 1: A sliding window needs validity to be monotone in the window's width. With negative numbers, growing the window can make the sum smaller, so there is no direction to shrink in. The window approach has no valid move.
    Hint 2: Instead: sum(i..j) == prefix[j+1] - prefix[i]. You want that to equal k.
    Hint 3: Rearranged, you need prefix[i] == prefix[j+1] - k. So walk the array keeping a count of every prefix sum seen so far, and add up the matches. Seed the map with {0: 1} so subarrays starting at index 0 are counted.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def subarray_sum_k(nums: list[int], k: int) -> int:
    raise NotImplementedError("implement subarray_sum_k")
