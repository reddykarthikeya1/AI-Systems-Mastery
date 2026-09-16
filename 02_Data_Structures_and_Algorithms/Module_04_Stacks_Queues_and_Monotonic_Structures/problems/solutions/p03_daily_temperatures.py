"""Reference solution — Problem 03: Daily Temperatures

Pattern:    Monotonic stack
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def daily_temperatures(temps: list[int]) -> list[int]:
    out = [0] * len(temps)
    stack: list[int] = []       # indices awaiting a warmer day

    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            out[j] = i - j      # the distance, which is why we store indices
        stack.append(i)

    return out
