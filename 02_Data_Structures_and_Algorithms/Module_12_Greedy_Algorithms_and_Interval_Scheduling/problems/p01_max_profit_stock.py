"""Problem 01 — Best Time To Buy And Sell Stock

Pattern:    Greedy running minimum
Difficulty: Easy
Target:     Time O(n), Space O(1)

Buy on one day and sell on a later day. Return the maximum profit, or ``0`` if
no profitable trade exists.

Constraints
- ``0 <= len(prices) <= 10**5``  -> O(n) required

Example
    max_profit_stock([7, 1, 5, 3, 6, 4]) -> 5     (buy at 1, sell at 6)
    max_profit_stock([7, 6, 4, 3, 1])    -> 0

Example:
    >>> max_profit_stock([7, 1, 5, 3, 6, 4])
    5
    >>> max_profit_stock([7, 6, 4, 3, 1])
    0

Hints — read one at a time, and try again between each.

    Hint 1: For each day, the best sale is that price minus the cheapest price seen so far.
    Hint 2: So one pass tracking the running minimum is enough.
    Hint 3: Update the minimum AFTER computing the profit for the day, or you allow buying and selling on the same day.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def max_profit_stock(prices: list[int]) -> int:
    raise NotImplementedError("implement max_profit_stock")
