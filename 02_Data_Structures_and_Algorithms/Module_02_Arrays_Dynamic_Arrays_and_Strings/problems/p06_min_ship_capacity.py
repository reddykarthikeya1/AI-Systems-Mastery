"""Problem 06 — Least Ship Capacity To Deliver In D Days

Pattern:    Binary search on the answer
Difficulty: Medium
Target:     Time O(n log(sum)), Space O(1)

Packages must be shipped **in the given order**. Each day you load consecutive
packages without exceeding the ship's capacity. Return the smallest capacity
that gets everything shipped within ``days`` days.

Constraints
- ``1 <= len(weights) <= 5 * 10**4``
- ``1 <= weights[i] <= 500``
- ``1 <= days <= len(weights)``

Example
    min_ship_capacity([1,2,3,4,5,6,7,8,9,10], 5) -> 15

This is the canonical "binary search on the answer" problem. Notice that the
input size is small but the *answer* ranges up to the total weight — that
mismatch is the recognition signal.

Hints — read one at a time, and try again between each.

    Hint 1: You cannot compute the capacity directly. But given a candidate capacity, can you check whether it works?
    Hint 2: Yes: one greedy pass, filling each day until the next package would overflow. That is O(n).
    Hint 3: Feasibility is monotone - a bigger ship can always do what a smaller one could - so binary search the capacity. The lower bound is max(weights) (a package must fit on its own); the upper bound is sum(weights).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def min_ship_capacity(weights: list[int], days: int) -> int:
    raise NotImplementedError("implement min_ship_capacity")
