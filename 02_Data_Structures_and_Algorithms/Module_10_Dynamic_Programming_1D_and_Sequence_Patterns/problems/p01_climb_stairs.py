"""Problem 01 — Climbing Stairs

Pattern:    1D DP / Fibonacci recurrence
Difficulty: Easy
Target:     Time O(n), Space O(1)

You climb 1 or 2 steps at a time. Return the number of distinct ways to reach
step ``n``.

Constraints
- ``0 <= n <= 10**5`` — a naive recursion is O(2^n) and hopeless

Example
    climb_stairs(2) -> 2      (1+1, 2)
    climb_stairs(3) -> 3      (1+1+1, 1+2, 2+1)

Hints — read one at a time, and try again between each.

    Hint 1: To reach step n you arrived from step n-1 or step n-2. Those are the only options.
    Hint 2: So ways(n) = ways(n-1) + ways(n-2) - the Fibonacci recurrence.
    Hint 3: You only ever need the last two values, so keep two variables instead of an array. That takes the space from O(n) to O(1).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def climb_stairs(n: int) -> int:
    raise NotImplementedError("implement climb_stairs")
