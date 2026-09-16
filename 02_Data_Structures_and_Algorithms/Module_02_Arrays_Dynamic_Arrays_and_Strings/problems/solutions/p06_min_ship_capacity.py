"""Reference solution — Problem 06: Least Ship Capacity To Deliver In D Days

Pattern:    Binary search on the answer
Complexity: Time O(n log(sum)), Space O(1)
"""

from __future__ import annotations


def min_ship_capacity(weights: list[int], days: int) -> int:
    def days_needed(capacity: int) -> int:
        used = 1
        load = 0
        for w in weights:
            if load + w > capacity:
                used += 1        # start a new day
                load = 0
            load += w
        return used

    # A single package must fit, so the answer is at least max(weights); one day
    # for everything is always enough, so it is at most sum(weights).
    lo, hi = max(weights), sum(weights)

    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid             # feasible - try smaller
        else:
            lo = mid + 1         # infeasible - must go bigger
    return lo
