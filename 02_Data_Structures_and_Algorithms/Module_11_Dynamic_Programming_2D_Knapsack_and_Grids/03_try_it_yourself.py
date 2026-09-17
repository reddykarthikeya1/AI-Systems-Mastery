"""Beginner playground for Module 11 - 2D Dynamic Programming, Knapsack & Grids.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Grid Unique Paths Transition
def unique_paths(m, n):
    dp = [1] * n
    for r in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]

assert unique_paths(3, 3) == 6
assert unique_paths(1, 1) == 1
assert unique_paths(3, 7) == 28
print(f"Unique paths on 3x3 grid: {unique_paths(3, 3)}, 3x7 grid: {unique_paths(3, 7)}")

# -------------------------------------------- 2. 0/1 Knapsack Decision Boundary
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for cap in range(capacity, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[capacity]

max_val = knapsack([2, 3, 4, 5], [3, 4, 5, 6], 5)
assert max_val == 7, "Items with w=2 (v=3) and w=3 (v=4) give total v=7"
assert knapsack([10], [100], 5) == 0, "Item exceeds capacity"
print(f"Max knapsack value for capacity 5: {max_val}")

# -------------------------------------------- 3. Longest Common Subsequence (LCS)
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

assert lcs("abcde", "ace") == 3, "Common subsequence is 'ace'"
assert lcs("abc", "def") == 0
assert lcs("ezupkr", "ubmrapg") == 2
print(f"LCS of 'abcde' and 'ace': {lcs('abcde', 'ace')}")

print()
print("All checks passed.")
