"""Problem 03 — Daily Temperatures

Pattern:    Monotonic stack
Difficulty: Medium
Target:     Time O(n), Space O(n)

For each day, return how many days you must wait for a warmer temperature.
Return 0 where no warmer day follows.

Constraints
- ``1 <= len(temps) <= 10**5``  -> O(n) required

Example
    [73, 74, 75, 71, 69, 72, 76, 73] -> [1, 1, 4, 2, 1, 1, 0, 0]

Hints — read one at a time, and try again between each.

    Hint 1: Same shape as 'next greater element', but the answer is a distance rather than a value.
    Hint 2: So the stack still holds indices - you need them to compute i - j.
    Hint 3: When temps[i] resolves a stacked index j, the answer for j is i - j.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def daily_temperatures(temps: list[int]) -> list[int]:
    raise NotImplementedError("implement daily_temperatures")
