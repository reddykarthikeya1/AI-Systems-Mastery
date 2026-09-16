"""Reference solution — Problem 02: Next Greater Element

Pattern:    Monotonic stack
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def next_greater(nums: list[int]) -> list[int]:
    out = [-1] * len(nums)
    stack: list[int] = []       # indices, values decreasing bottom -> top

    for i, x in enumerate(nums):
        # x resolves every pending index with a strictly smaller value.
        while stack and nums[stack[-1]] < x:
            out[stack.pop()] = x
        stack.append(i)

    # Whatever remains has no greater element to its right; already -1.
    return out
