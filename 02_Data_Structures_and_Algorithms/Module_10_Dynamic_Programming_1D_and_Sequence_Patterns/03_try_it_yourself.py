"""Beginner playground for Module 10 - 1D Dynamic Programming & Sequence Patterns.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Memoization vs Tabulation Fibonacci
def fib(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1

assert fib(0) == 0
assert fib(1) == 1
assert fib(10) == 55
print(f"Fibonacci(10) in O(N) time: {fib(10)}")

# -------------------------------------------- 2. House Robber Choice Transition
def rob(nums):
    rob1, rob2 = 0, 0
    for n in nums:
        rob1, rob2 = rob2, max(rob2, rob1 + n)
    return rob2

assert rob([1, 2, 3, 1]) == 4, "Rob house 0 (1) + house 2 (3) = 4"
assert rob([2, 7, 9, 3, 1]) == 12, "2 + 9 + 1 = 12"
assert rob([5]) == 5
print(f"Max loot for [2, 7, 9, 3, 1]: {rob([2, 7, 9, 3, 1])}")

# -------------------------------------------- 3. Coin Change Minimum Count
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amount] if dp[amount] != float('inf') else -1

assert coin_change([1, 2, 5], 11) == 3, "5 + 5 + 1 = 3 coins"
assert coin_change([2], 3) == -1, "Impossible"
assert coin_change([1], 0) == 0
print(f"Fewest coins to make 11: {coin_change([1, 2, 5], 11)}")

print()
print("All checks passed.")
