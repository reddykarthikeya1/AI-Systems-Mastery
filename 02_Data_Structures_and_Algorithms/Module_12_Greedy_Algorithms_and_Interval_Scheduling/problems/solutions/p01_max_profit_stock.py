"""Reference solution — Problem 01: Best Time To Buy And Sell Stock

Pattern:    Greedy running minimum
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def max_profit_stock(prices: list[int]) -> int:
    cheapest = float("inf")
    best = 0
    for price in prices:
        # Compute the profit against the minimum from a STRICTLY earlier day,
        # then fold today's price in.
        if price - cheapest > best:
            best = int(price - cheapest)
        if price < cheapest:
            cheapest = price
    return best
