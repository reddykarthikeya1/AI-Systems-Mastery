"""Problem 04 — Longest Increasing Subsequence

Pattern:    Patience sorting / binary search DP
Difficulty: Hard
Target:     Time O(n log n), Space O(n)

Return the length of the longest strictly increasing subsequence. Elements need
not be contiguous.

Constraints
- ``0 <= len(nums) <= 2500`` — the O(n^2) DP passes, but O(n log n) is the target
- ``-10**4 <= nums[i] <= 10**4``

Example
    lis([10, 9, 2, 5, 3, 7, 101, 18]) -> 4     (2, 3, 7, 101)

Example:
    >>> lis([10, 9, 2, 5, 3, 7, 101, 18])
    4

Hints — read one at a time, and try again between each.

    Hint 1: The O(n^2) DP is: best[i] = 1 + max(best[j]) over all j < i with nums[j] < nums[i]. Get that working first.
    Hint 2: For O(n log n), maintain `tails`, where tails[k] is the SMALLEST possible tail of an increasing subsequence of length k+1. That array is always sorted.
    Hint 3: For each x, binary search for the first tail >= x and overwrite it; append if x exceeds every tail. The answer is len(tails). Note `tails` is not itself a valid subsequence - only its length is meaningful.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def lis(nums: list[int]) -> int:
    raise NotImplementedError("implement lis")
