"""Problem 02 — Next Greater Element

Pattern:    Monotonic stack
Difficulty: Medium
Target:     Time O(n), Space O(n)

For each element, return the next element to its right that is strictly greater,
or ``-1`` if there is none.

Constraints
- ``0 <= len(nums) <= 10**5``  -> O(n) required
- values may repeat

Example
    next_greater([2, 1, 2, 4, 3]) -> [4, 2, 4, -1, -1]

Hints — read one at a time, and try again between each.

    Hint 1: The brute force scans right from every index. What work does it repeat?
    Hint 2: Keep a stack of indices whose answer is still unknown, with their values decreasing from bottom to top.
    Hint 3: When a new value arrives, it is the answer for every stacked index whose value is smaller - pop them all and record it. Each index is pushed once and popped at most once, so the total work is O(n) even though a while sits inside the for.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def next_greater(nums: list[int]) -> list[int]:
    raise NotImplementedError("implement next_greater")
