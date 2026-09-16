"""Reference solution — Problem 04: Largest Rectangle In A Histogram

Pattern:    Monotonic stack
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def largest_rectangle(heights: list[int]) -> int:
    best = 0
    stack: list[int] = []           # indices, heights increasing

    # The trailing 0 sentinel forces every remaining bar to be settled, so the
    # settle logic lives in exactly one place.
    for i, h in enumerate([*heights, 0]):
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            # Left boundary is the new stack top (exclusive); right is i.
            left = stack[-1] if stack else -1
            width = i - left - 1
            best = max(best, heights[top] * width)
        stack.append(i)

    return best
