"""Reference solution — Problem 04: 0/1 Knapsack

Pattern:    0/1 knapsack DP
Complexity: Time O(n*capacity), Space O(capacity)
"""

from __future__ import annotations


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    if len(weights) != len(values):
        raise ValueError("weights and values must be the same length")

    best = [0] * (capacity + 1)

    for w, v in zip(weights, values):
        # DOWNWARD is essential. Upward would read a best[c - w] that already
        # includes this item, turning 0/1 into unbounded knapsack.
        for c in range(capacity, w - 1, -1):
            candidate = best[c - w] + v
            if candidate > best[c]:
                best[c] = candidate

    return best[capacity]
