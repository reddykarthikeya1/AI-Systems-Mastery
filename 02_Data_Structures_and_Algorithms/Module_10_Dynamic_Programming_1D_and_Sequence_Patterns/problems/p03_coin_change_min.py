"""Problem 03 — Coin Change (Fewest Coins)

Pattern:    Unbounded knapsack DP
Difficulty: Medium
Target:     Time O(amount * len(coins)), Space O(amount)

Return the fewest coins that sum to ``amount``, or ``-1`` if it cannot be made.
Each coin may be used any number of times.

Constraints
- ``1 <= len(coins) <= 12``, ``1 <= coins[i] <= 2**31 - 1``
- ``0 <= amount <= 10**4``

Example
    coin_change_min([1, 2, 5], 11) -> 3    (5 + 5 + 1)
    coin_change_min([2], 3)        -> -1

A greedy "take the biggest coin first" is **wrong** here: with coins
``[1, 3, 4]`` and amount 6, greedy gives 4+1+1 = 3 coins while the optimum is
3+3 = 2. Problem 03's tests include that case.

Example:
    >>> coin_change_min([1, 2, 5], 11)
    3
    >>> coin_change_min([2], 3)
    -1

Hints — read one at a time, and try again between each.

    Hint 1: Greedy fails - see the note above. So you need to consider every coin at every amount.
    Hint 2: State: best[a] is the fewest coins summing to exactly a. Base case: best[0] = 0.
    Hint 3: Transition: best[a] = 1 + min(best[a - c]) over every coin c that fits. Iterate amounts outward from 1 so every subproblem is ready when needed.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def coin_change_min(coins: list[int], amount: int) -> int:
    raise NotImplementedError("implement coin_change_min")
