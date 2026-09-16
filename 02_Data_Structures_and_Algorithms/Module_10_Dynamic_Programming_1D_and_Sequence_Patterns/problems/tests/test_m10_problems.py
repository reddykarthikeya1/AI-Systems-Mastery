"""Problem-bank suite for Module_10_Dynamic_Programming_1D_and_Sequence_Patterns.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_climb_stairs import climb_stairs
from p02_house_robber import house_robber
from p03_coin_change_min import coin_change_min
from p04_lis import lis
from p05_word_break import word_break
from p06_decode_ways import decode_ways
from p07_max_product_subarray import max_product_subarray
from p08_stock_with_cooldown import stock_with_cooldown


def test_p01_climb_stairs():
    """Climbing Stairs — 1D DP / Fibonacci recurrence (Easy)."""
    assert climb_stairs(0) == 1
    assert climb_stairs(1) == 1
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(4) == 5
    assert climb_stairs(10) == 89
    with pytest.raises(ValueError):
        climb_stairs(-1)
    # Cross-check against an exhaustive enumeration for small n.
    def brute(k):
        if k < 0:
            return 0
        if k == 0:
            return 1
        return brute(k - 1) + brute(k - 2)
    for k in range(0, 16):
        assert climb_stairs(k) == brute(k), k
    # Scale: O(2^n) recursion would never finish this.
    assert climb_stairs(100_000) > 0

def test_p02_house_robber():
    """House Robber — 1D DP with a skip constraint (Medium)."""
    assert house_robber([1, 2, 3, 1]) == 4
    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert house_robber([]) == 0
    assert house_robber([5]) == 5
    # Two houses: take the larger.
    assert house_robber([2, 1]) == 2
    assert house_robber([1, 2]) == 2
    # All zeros.
    assert house_robber([0, 0, 0]) == 0
    # Adjacent large values force a skip.
    assert house_robber([100, 1, 1, 100]) == 200
    # Cross-check against brute-force over all valid subsets.
    import itertools
    for data in ([1, 2, 3, 1], [2, 7, 9, 3, 1], [5, 1, 2, 6], [4, 4, 4, 4, 4]):
        best = 0
        for r in range(len(data) + 1):
            for combo in itertools.combinations(range(len(data)), r):
                if all(b - a > 1 for a, b in zip(combo, combo[1:])):
                    best = max(best, sum(data[i] for i in combo))
        assert house_robber(data) == best, data

def test_p03_coin_change_min():
    """Coin Change (Fewest Coins) — Unbounded knapsack DP (Medium)."""
    assert coin_change_min([1, 2, 5], 11) == 3
    assert coin_change_min([2], 3) == -1
    assert coin_change_min([1], 0) == 0
    # Zero amount always needs zero coins.
    assert coin_change_min([5], 0) == 0
    # The case greedy gets wrong: 3+3 beats 4+1+1.
    assert coin_change_min([1, 3, 4], 6) == 2
    # Exact single coin.
    assert coin_change_min([1, 2, 5], 5) == 1
    # Impossible because every coin is too large.
    assert coin_change_min([7, 11], 5) == -1
    # Only 1s available.
    assert coin_change_min([1], 25) == 25
    # Coin larger than int32 must not break anything.
    assert coin_change_min([1, 2147483647], 3) == 3
    # Cross-check against BFS over amounts.
    from collections import deque
    def brute(cs, amt):
        if amt == 0:
            return 0
        seen = {0}
        q = deque([(0, 0)])
        while q:
            total, steps = q.popleft()
            for c in cs:
                nt = total + c
                if nt == amt:
                    return steps + 1
                if nt < amt and nt not in seen:
                    seen.add(nt)
                    q.append((nt, steps + 1))
        return -1
    for cs, amt in (([1, 3, 4], 6), ([2, 5], 11), ([3, 7], 5), ([1, 5, 6, 9], 11)):
        assert coin_change_min(cs, amt) == brute(cs, amt), (cs, amt)

def test_p04_lis():
    """Longest Increasing Subsequence — Patience sorting / binary search DP (Hard)."""
    assert lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis([0, 1, 0, 3, 2, 3]) == 4
    assert lis([]) == 0
    assert lis([5]) == 1
    # All equal: strictly increasing means length 1.
    assert lis([7, 7, 7, 7]) == 1
    # Already sorted, and reverse sorted.
    assert lis([1, 2, 3, 4, 5]) == 5
    assert lis([5, 4, 3, 2, 1]) == 1
    # Negatives.
    assert lis([-2, -1, 0]) == 3
    # Cross-check against the O(n^2) DP.
    def brute(a):
        if not a:
            return 0
        best = [1] * len(a)
        for i in range(len(a)):
            for j in range(i):
                if a[j] < a[i]:
                    best[i] = max(best[i], best[j] + 1)
        return max(best)
    for data in (
        [10, 9, 2, 5, 3, 7, 101, 18],
        [4, 10, 4, 3, 8, 9],
        [1, 3, 6, 7, 9, 4, 10, 5, 6],
        [7, 7, 7],
        [2, 1, 3, 1, 4],
    ):
        assert lis(data) == brute(data), data

def test_p05_word_break():
    """Word Break — 1D DP over string prefixes (Medium)."""
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    # A single word.
    assert word_break("a", ["a"]) is True
    assert word_break("a", ["b"]) is False
    # Words may be reused.
    assert word_break("aaaa", ["a"]) is True
    assert word_break("aaaaa", ["aa"]) is False
    assert word_break("aaaa", ["aa"]) is True
    # Greedy longest-first would fail here: it takes "aaa" then cannot, # finish, whereas "aa" + "aa" works.
    assert word_break("aaaa", ["aaa", "aa"]) is True
    # Dictionary word longer than the string.
    assert word_break("ab", ["abcd"]) is False
    # Scale: 300 characters with a small dictionary.
    assert word_break("ab" * 150, ["a", "b"]) is True

def test_p06_decode_ways():
    """Decode Ways — 1D DP with a two-character lookback (Medium)."""
    assert decode_ways("12") == 2
    assert decode_ways("226") == 3
    assert decode_ways("06") == 0
    assert decode_ways("0") == 0
    assert decode_ways("1") == 1
    # "10" has exactly one decoding: "J". Not two.
    assert decode_ways("10") == 1
    assert decode_ways("100") == 0
    # 27 is out of range, so only the single-digit split works.
    assert decode_ways("27") == 1
    assert decode_ways("26") == 2
    # A zero that cannot be consumed by a valid pair.
    assert decode_ways("301") == 0
    assert decode_ways("2101") == 1
    # All ones behaves like Fibonacci.
    assert decode_ways("11111") == 8

def test_p07_max_product_subarray():
    """Maximum Product Subarray — 1D DP with two-value state (Medium)."""
    assert max_product_subarray([2, 3, -2, 4]) == 6
    assert max_product_subarray([-2, 0, -1]) == 0
    # Two negatives multiply to a positive - the case a max-only state, # gets wrong.
    assert max_product_subarray([-2, 3, -4]) == 24
    assert max_product_subarray([-1, -2, -3]) == 6
    assert max_product_subarray([5]) == 5
    assert max_product_subarray([-5]) == -5
    # A zero resets the running products.
    assert max_product_subarray([-2, 0, -1, -3]) == 3
    assert max_product_subarray([0, 0, 0]) == 0
    # An odd number of negatives means dropping one of them.
    assert max_product_subarray([-1, -2, -3, -4]) == 24
    with pytest.raises(ValueError):
        max_product_subarray([])
    # Cross-check against brute force.
    import math
    for data in (
        [2, 3, -2, 4], [-2, 3, -4], [-1, -2, -3, -4],
        [0, 2, -3, 0, 4, -1, -2], [1, -1, 1, -1],
    ):
        brute = max(
            math.prod(data[i : j + 1])
            for i in range(len(data))
            for j in range(i, len(data))
        )
        assert max_product_subarray(data) == brute, data

def test_p08_stock_with_cooldown():
    """Best Time To Buy And Sell Stock With Cooldown — DP as a state machine (Hard)."""
    assert stock_with_cooldown([1, 2, 3, 0, 2]) == 3
    assert stock_with_cooldown([1]) == 0
    assert stock_with_cooldown([]) == 0
    # Monotonically falling: never trade.
    assert stock_with_cooldown([5, 4, 3, 2, 1]) == 0
    # One clean trade.
    assert stock_with_cooldown([1, 5]) == 4
    # The cooldown makes buying every day impossible, so a rising, # sequence is one single trade.
    assert stock_with_cooldown([1, 2, 3, 4, 5]) == 4
    # Flat prices yield nothing.
    assert stock_with_cooldown([3, 3, 3]) == 0
    # One long hold beats splitting into two trades here: buying at 1, # and selling at 7 yields 6, while 1->3 then 4->7 yields only 5
    # because the cooldown costs the day at price 2.
    assert stock_with_cooldown([6, 1, 3, 2, 4, 7]) == 6
    # Cross-check against exhaustive search on small inputs.
    import functools
    def brute(ps):
        @functools.cache
        def go(i, holding, cooling):
            if i >= len(ps):
                return 0
            best = go(i + 1, holding, False)          # do nothing
            if holding:
                best = max(best, ps[i] + go(i + 1, False, True))
            elif not cooling:
                best = max(best, -ps[i] + go(i + 1, True, False))
            return best
        return go(0, False, False)
    for data in ([1, 2, 3, 0, 2], [6, 1, 3, 2, 4, 7], [1, 2, 4], [2, 1, 4, 5, 2, 9, 7]):
        assert stock_with_cooldown(data) == brute(tuple(data)), data
