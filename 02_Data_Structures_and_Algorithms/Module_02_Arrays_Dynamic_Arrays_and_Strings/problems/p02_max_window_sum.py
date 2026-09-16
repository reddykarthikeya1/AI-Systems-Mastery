"""Problem 02 — Maximum Sum Of A Fixed-Size Window

Pattern:    Sliding window (fixed)
Difficulty: Easy
Target:     Time O(n), Space O(1)

Return the maximum sum of any contiguous subarray of length exactly ``k``.

Raise ``ValueError`` if ``k`` is not a valid window size for this array.

Constraints
- ``1 <= len(nums) <= 10**5``  -> O(n) required
- values may be negative

Example
    max_window_sum([2, 1, 5, 1, 3, 2], 3) -> 9

Hints — read one at a time, and try again between each.

    Hint 1: Summing every window independently is O(n*k). What do two adjacent windows have in common?
    Hint 2: They share k-1 elements. Moving right adds one element and drops one.
    Hint 3: Maintain a running total: total += nums[i] - nums[i - k]. That is the whole technique.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def max_window_sum(nums: list[int], k: int) -> int:
    raise NotImplementedError("implement max_window_sum")
