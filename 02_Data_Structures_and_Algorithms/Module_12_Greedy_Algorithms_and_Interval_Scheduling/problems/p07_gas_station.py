"""Problem 07 — Gas Station Circuit

Pattern:    Greedy with a restart point
Difficulty: Medium
Target:     Time O(n), Space O(1)

There are ``n`` stations in a circle. ``gas[i]`` is the fuel available at
station ``i``, and ``cost[i]`` the fuel needed to reach station ``i+1``. Starting
with an empty tank, return the index of the only station from which you can
complete the circuit, or ``-1`` if none exists.

Constraints
- ``1 <= len(gas) == len(cost) <= 10**5``  -> O(n) expected

Example
    gas_station([1,2,3,4,5], [3,4,5,1,2]) -> 3
    gas_station([2,3,4], [3,4,3])         -> -1

Example:
    >>> gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    3
    >>> gas_station([2, 3, 4], [3, 4, 3])
    -1

Hints — read one at a time, and try again between each.

    Hint 1: First, a feasibility check: if total gas is less than total cost, no start can work.
    Hint 2: Given that it IS feasible, one pass suffices. Track the running tank from the current candidate start.
    Hint 3: If the tank ever goes negative at station i, then no station from the current candidate up to i can be a valid start - so the next candidate is i+1 and the tank resets. That is the whole insight.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def gas_station(gas: list[int], cost: list[int]) -> int:
    raise NotImplementedError("implement gas_station")
