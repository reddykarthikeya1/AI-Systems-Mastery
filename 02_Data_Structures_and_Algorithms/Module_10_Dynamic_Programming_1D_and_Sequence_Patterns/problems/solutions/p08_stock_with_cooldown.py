"""Reference solution — Problem 08: Best Time To Buy And Sell Stock With Cooldown

Pattern:    DP as a state machine
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def stock_with_cooldown(prices: list[int]) -> int:
    if not prices:
        return 0

    NEG = float("-inf")
    hold: float = -prices[0]    # bought on day 0
    sold: float = NEG           # cannot have sold before buying
    rest: float = 0             # own nothing, free to buy

    for price in prices[1:]:
        # All three read the PREVIOUS day's values, so snapshot them first.
        prev_hold, prev_sold, prev_rest = hold, sold, rest
        hold = max(prev_hold, prev_rest - price)
        sold = prev_hold + price
        rest = max(prev_rest, prev_sold)    # the cooldown day lands here

    return int(max(sold, rest, 0))
