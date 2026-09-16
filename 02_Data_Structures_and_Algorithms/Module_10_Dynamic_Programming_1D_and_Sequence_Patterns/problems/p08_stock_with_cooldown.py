"""Problem 08 — Best Time To Buy And Sell Stock With Cooldown

Pattern:    DP as a state machine
Difficulty: Hard
Target:     Time O(n), Space O(1)

You may buy and sell as often as you like, but after selling you must wait one
day before buying again. You may hold at most one share. Return the maximum
profit.

Constraints
- ``0 <= len(prices) <= 5000``
- ``0 <= prices[i] <= 1000``

Example
    stock_with_cooldown([1, 2, 3, 0, 2]) -> 3     (buy 1, sell 2, cooldown, buy 0, sell 2)

Hints — read one at a time, and try again between each.

    Hint 1: Anything with modes - holding, free to buy, cooling down - is a state machine, and the states ARE the DP.
    Hint 2: Three states per day: HOLD (own a share), SOLD (just sold today, so tomorrow is a cooldown), REST (own nothing and free to buy).
    Hint 3: Transitions: hold = max(hold, rest - price); sold = hold + price; rest = max(rest, previous sold). Compute all three from the PREVIOUS day's values, not from each other.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def stock_with_cooldown(prices: list[int]) -> int:
    raise NotImplementedError("implement stock_with_cooldown")
