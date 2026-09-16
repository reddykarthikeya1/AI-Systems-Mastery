"""Reference solution — Problem 07: Gas Station Circuit

Pattern:    Greedy with a restart point
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def gas_station(gas: list[int], cost: list[int]) -> int:
    if len(gas) != len(cost):
        raise ValueError("gas and cost must be the same length")

    # If there is not enough fuel overall, no starting point can work.
    if sum(gas) < sum(cost):
        return -1

    start = 0
    tank = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        tank += g - c
        if tank < 0:
            # Nothing from `start`..i can be a valid start, so skip past i.
            start = i + 1
            tank = 0
    return start
