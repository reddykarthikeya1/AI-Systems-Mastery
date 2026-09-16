"""Problem-bank suite for Module_02_Arrays_Dynamic_Arrays_and_Strings.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_two_sum import two_sum
from p02_max_window_sum import max_window_sum
from p03_longest_k_distinct import longest_k_distinct
from p04_subarray_sum_k import subarray_sum_k
from p05_product_except_self import product_except_self
from p06_min_ship_capacity import min_ship_capacity
from p07_three_sum import three_sum
from p08_longest_palindrome import longest_palindrome


def test_p01_two_sum():
    """Two Sum — Hash map complement (Easy)."""
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    # Negative numbers and a negative target.
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]
    # A lone 5 must not pair with itself to reach 10.
    assert two_sum([5, 1, 10], 10) == []
    # But two distinct 5s must be found.
    assert two_sum([5, 1, 5], 10) == [0, 2]
    # Large input: an O(n^2) solution would be far too slow here.
    big = list(range(10_000))
    assert two_sum(big, 19_997) == [9998, 9999]

def test_p02_max_window_sum():
    """Maximum Sum Of A Fixed-Size Window — Sliding window (fixed) (Easy)."""
    assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9
    assert max_window_sum([2, 3, 4, 1, 5], 1) == 5
    assert max_window_sum([1, 2, 3], 3) == 6
    # All negative: the answer is negative, not 0. A solution that
    # initialises `best = 0` fails here and nowhere else.
    assert max_window_sum([-4, -2, -7, -3], 2) == -6
    # Invalid window sizes must raise.
    with pytest.raises(ValueError):
        max_window_sum([1, 2, 3], 4)
    with pytest.raises(ValueError):
        max_window_sum([1, 2, 3], 0)
    # O(n) required: this would be ~10^9 operations if summed per window.
    big = list(range(100_000))
    assert max_window_sum(big, 1000) == sum(range(99_000, 100_000))

def test_p03_longest_k_distinct():
    """Longest Substring With At Most K Distinct Characters — Sliding window (variable) (Medium)."""
    assert longest_k_distinct("eceba", 2) == 3
    assert longest_k_distinct("aa", 1) == 2
    assert longest_k_distinct("abcadcacacaca", 3) == 11
    # k = 0 admits nothing, the empty string has no substring.
    assert longest_k_distinct("abc", 0) == 0
    assert longest_k_distinct("", 3) == 0
    # k larger than the alphabet present: the whole string qualifies.
    assert longest_k_distinct("abc", 10) == 3
    # Single repeated character.
    assert longest_k_distinct("aaaa", 1) == 4
    # O(n) required.
    big = "abcd" * 25_000
    assert longest_k_distinct(big, 2) == 2

def test_p04_subarray_sum_k():
    """Count Subarrays Summing To K — Prefix sums + hash map (Medium)."""
    assert subarray_sum_k([1, 1, 1], 2) == 2
    assert subarray_sum_k([1, 2, 3], 3) == 2
    # Negative numbers - the case a sliding window cannot handle.
    assert subarray_sum_k([1, -1, 0], 0) == 3
    assert subarray_sum_k([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
    # Zeros create many overlapping answers.
    assert subarray_sum_k([0, 0, 0], 0) == 6
    # A subarray starting at index 0 must be counted, this is the
    # assertion that fails when the {0: 1} seed is missing.
    assert subarray_sum_k([1, 2, 3], 1) == 1
    assert subarray_sum_k([5], 5) == 1
    assert subarray_sum_k([5], 3) == 0
    # Cross-check against brute force on random-ish data.
    data = [2, -1, 3, -2, 4, -3, 1, 0, 2, -2]
    for target in range(-4, 6):
        brute = sum(
            1
            for i in range(len(data))
            for j in range(i, len(data))
            if sum(data[i : j + 1]) == target
        )
        assert subarray_sum_k(data, target) == brute, target

def test_p05_product_except_self():
    """Product Of Array Except Self — Prefix/suffix products (Medium)."""
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([2, 3]) == [3, 2]
    # One zero: every other slot becomes 0, and the zero's own slot, # holds the product of the rest. Division-based solutions break here.
    assert product_except_self([1, 0, 3, 4]) == [0, 12, 0, 0]
    # Two zeros: everything is 0.
    assert product_except_self([0, 0, 3]) == [0, 0, 0]
    # Negative values must keep their signs straight.
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    # Cross-check against a brute force.
    data = [3, 1, -2, 4, 5]
    brute = [
        __import__('math').prod(data[:i] + data[i + 1 :]) for i in range(len(data))
    ]
    assert product_except_self(data) == brute
    # O(n) required.
    big = [1] * 100_000
    assert product_except_self(big) == [1] * 100_000

def test_p06_min_ship_capacity():
    """Least Ship Capacity To Deliver In D Days — Binary search on the answer (Medium)."""
    assert min_ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert min_ship_capacity([3, 2, 2, 4, 1, 4], 3) == 6
    assert min_ship_capacity([1, 2, 3, 1, 1], 4) == 3
    # One day: the ship must carry everything at once.
    assert min_ship_capacity([1, 2, 3], 1) == 6
    # As many days as packages: capacity is the largest single package.
    assert min_ship_capacity([5, 3, 8, 1], 4) == 8
    # A single package.
    assert min_ship_capacity([7], 1) == 7
    # The answer must satisfy the constraint, and one less must not -, # that pair of checks is what 'minimum' actually means.
    def _days(ws, cap):
        used, load = 1, 0
        for w in ws:
            if load + w > cap:
                used += 1
                load = 0
            load += w
        return used
    ws, d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5
    ans = min_ship_capacity(ws, d)
    assert _days(ws, ans) <= d
    assert _days(ws, ans - 1) > d

def test_p07_three_sum():
    """Three Sum — Sorting + two pointers (Medium)."""
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([]) == []
    assert three_sum([0]) == []
    assert three_sum([0, 1, 1]) == []
    # All zeros must produce exactly one triple, not many.
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
    # Heavy duplication is where dedup bugs show up.
    assert three_sum([-2, 0, 0, 2, 2]) == [[-2, 0, 2]]
    # No triple sums to zero.
    assert three_sum([1, 2, 3]) == []
    # Every returned triple must actually sum to zero and be sorted,, # and the whole list must be free of duplicates.
    data = [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 4, 4, 6, 6]
    res = three_sum(data)
    assert all(sum(t) == 0 for t in res)
    assert all(t == sorted(t) for t in res)
    assert len({tuple(t) for t in res}) == len(res)

def test_p08_longest_palindrome():
    """Longest Palindromic Substring — Expand around centre (Medium)."""
    assert longest_palindrome("babad") == "bab"
    # The even-length case: an odd-only solution returns "b" here.
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("") == ""
    assert longest_palindrome("a") == "a"
    assert longest_palindrome("ac") == "a"
    assert longest_palindrome("aaaa") == "aaaa"
    assert longest_palindrome("racecar") == "racecar"
    assert longest_palindrome("abacdfgdcaba") == "aba"
    # Case sensitivity: "Aa" is not a palindrome.
    assert longest_palindrome("Aa") == "A"
    # Cross-check against brute force.
    for text in ("abba", "abcba", "xyzzyx", "aabbaa", "abcdcba"):
        brute = ""
        for i in range(len(text)):
            for j in range(i + 1, len(text) + 1):
                sub = text[i:j]
                if sub == sub[::-1] and len(sub) > len(brute):
                    brute = sub
        assert longest_palindrome(text) == brute, text
