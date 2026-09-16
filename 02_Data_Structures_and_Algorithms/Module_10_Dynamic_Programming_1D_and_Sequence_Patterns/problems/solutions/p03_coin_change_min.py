"""Reference solution — Problem 03: Coin Change (Fewest Coins)

Pattern:    Unbounded knapsack DP
Complexity: Time O(amount * len(coins)), Space O(amount)
"""

from __future__ import annotations


def coin_change_min(coins: list[int], amount: int) -> int:
    INF = float("inf")
    best: list[float] = [INF] * (amount + 1)
    best[0] = 0                 # zero coins make zero

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1

    return -1 if best[amount] == INF else int(best[amount])
