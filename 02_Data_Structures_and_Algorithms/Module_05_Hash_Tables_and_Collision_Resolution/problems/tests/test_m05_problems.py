"""Problem-bank suite for Module_05_Hash_Tables_and_Collision_Resolution.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_group_anagrams import group_anagrams
from p02_top_k_frequent import top_k_frequent
from p03_longest_consecutive import longest_consecutive
from p04_first_unique_char import first_unique_char
from p05_contains_nearby_duplicate import contains_nearby_duplicate
from p06_is_isomorphic import is_isomorphic
from p07_subarrays_div_by_k import subarrays_div_by_k
from p08_four_sum_count import four_sum_count


def test_p01_group_anagrams():
    """Group Anagrams — Hash map with a canonical key (Medium)."""
    got = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert got == [["bat"], ["eat", "tea", "ate"], ["tan", "nat"]]
    assert group_anagrams([]) == []
    assert group_anagrams([""]) == [[""]]
    assert group_anagrams(["a"]) == [["a"]]
    # No anagrams at all.
    assert group_anagrams(["abc", "def"]) == [["abc"], ["def"]]
    # Identical words group together.
    assert group_anagrams(["ab", "ab"]) == [["ab", "ab"]]
    # Same letters, different multiplicities are NOT anagrams.
    assert group_anagrams(["aab", "abb"]) == [["aab"], ["abb"]]
    # Every input word appears exactly once across the groups.
    words = ["listen", "silent", "enlist", "google", "banana", "elgoog"]
    groups = group_anagrams(words)
    flat = [w for g in groups for w in g]
    assert sorted(flat) == sorted(words)
    assert len(groups) == 3

def test_p02_top_k_frequent():
    """Top K Frequent Elements — Counting + bucket sort (Medium)."""
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    # Ties broken by ascending value.
    assert top_k_frequent([1, 2, 3], 3) == [1, 2, 3]
    assert top_k_frequent([3, 2, 1], 2) == [1, 2]
    # All the same element.
    assert top_k_frequent([5, 5, 5], 1) == [5]
    # Negative values.
    assert top_k_frequent([-1, -1, 2], 1) == [-1]
    # k must be validated, not silently clamped.
    with pytest.raises(ValueError):
        top_k_frequent([1, 2], 3)
    # Ordering is strictly by descending frequency.
    data = [4, 4, 4, 4, 7, 7, 7, 9, 9, 1]
    assert top_k_frequent(data, 3) == [4, 7, 9]
    assert top_k_frequent(data, 4) == [4, 7, 9, 1]
    # O(n): a sort-everything solution is fine here, but this checks scale.
    big = [i % 1000 for i in range(100_000)]
    assert len(top_k_frequent(big, 10)) == 10

def test_p03_longest_consecutive():
    """Longest Consecutive Sequence — Hash set + sequence-start check (Medium)."""
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([1]) == 1
    # Duplicates must not inflate the length.
    assert longest_consecutive([1, 1, 1]) == 1
    assert longest_consecutive([1, 2, 2, 3]) == 3
    # No consecutive pair.
    assert longest_consecutive([10, 20, 30]) == 1
    # Negative and mixed signs.
    assert longest_consecutive([-3, -2, -1, 0, 1]) == 5
    assert longest_consecutive([-1, 1]) == 1
    # A long single run - this is where the run-start check earns its, # keep. Without it this input is quadratic.
    assert longest_consecutive(list(range(100_000))) == 100_000
    # And a reversed one, to be sure order does not matter.
    assert longest_consecutive(list(range(50_000, 0, -1))) == 50_000

def test_p04_first_unique_char():
    """First Unique Character — Frequency counting (Easy)."""
    assert first_unique_char("leetcode") == 0
    assert first_unique_char("loveleetcode") == 2
    assert first_unique_char("aabb") == -1
    assert first_unique_char("") == -1
    assert first_unique_char("z") == 0
    # The unique character is last.
    assert first_unique_char("aabbc") == 4
    # Only one character type, repeated.
    assert first_unique_char("aaaa") == -1
    # Must return the FIRST unique, not any unique.
    assert first_unique_char("abcabd") == 2

def test_p05_contains_nearby_duplicate():
    """Duplicate Within Distance K — Sliding window + hash set (Medium)."""
    assert contains_nearby_duplicate([1, 2, 3, 1], 3) is True
    assert contains_nearby_duplicate([1, 0, 1, 1], 1) is True
    assert contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2) is False
    # Exactly at the boundary distance.
    assert contains_nearby_duplicate([1, 2, 1], 2) is True
    assert contains_nearby_duplicate([1, 2, 1], 1) is False
    # k = 0 requires i == j, which the problem forbids.
    assert contains_nearby_duplicate([1, 1], 0) is False
    # Adjacent duplicates.
    assert contains_nearby_duplicate([1, 1], 1) is True
    # No duplicates at all.
    assert contains_nearby_duplicate([1, 2, 3], 10) is False
    assert contains_nearby_duplicate([5], 1) is False
    # Cross-check against brute force.
    data = [4, 1, 2, 4, 1, 9, 2, 2, 7, 1]
    for k in range(0, 11):
        brute = any(
            data[i] == data[j]
            for i in range(len(data))
            for j in range(i + 1, min(len(data), i + k + 1))
        )
        assert contains_nearby_duplicate(data, k) is brute, k

def test_p06_is_isomorphic():
    """Isomorphic Strings — Two-way hash mapping (Easy)."""
    assert is_isomorphic("egg", "add") is True
    assert is_isomorphic("foo", "bar") is False
    assert is_isomorphic("paper", "title") is True
    # The case a one-way map gets wrong.
    assert is_isomorphic("badc", "baba") is False
    assert is_isomorphic("ab", "aa") is False
    assert is_isomorphic("", "") is True
    assert is_isomorphic("a", "b") is True
    # Different lengths cannot be isomorphic.
    assert is_isomorphic("ab", "abc") is False
    # Identity mapping.
    assert is_isomorphic("abc", "abc") is True

def test_p07_subarrays_div_by_k():
    """Subarray Sums Divisible By K — Prefix sums + modular arithmetic (Medium)."""
    assert subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5) == 7
    assert subarrays_div_by_k([5], 5) == 1
    assert subarrays_div_by_k([5], 9) == 0
    # Zeros are divisible by everything.
    assert subarrays_div_by_k([0, 0, 0], 3) == 6
    # Negative values - the case naive remainder handling breaks on.
    assert subarrays_div_by_k([-1, 2, 9], 2) == 2
    assert subarrays_div_by_k([-5, -5], 5) == 3
    # Cross-check against brute force, including negatives.
    data = [3, -2, 7, -4, 1, 0, 5, -6]
    for k in (2, 3, 5, 7):
        brute = sum(
            1
            for i in range(len(data))
            for j in range(i, len(data))
            if sum(data[i : j + 1]) % k == 0
        )
        assert subarrays_div_by_k(data, k) == brute, k

def test_p08_four_sum_count():
    """Four Sum Count (Two Hash Maps) — Meet in the middle with a hash map (Hard)."""
    assert four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2]) == 2
    assert four_sum_count([0], [0], [0], [0]) == 1
    assert four_sum_count([1], [1], [1], [1]) == 0
    # Every combination works, so the count is n^4.
    assert four_sum_count([0, 0], [0, 0], [0, 0], [0, 0]) == 16
    # Counts must multiply, not merely be summed.
    assert four_sum_count([1, 1], [-1, -1], [0, 0], [0, 0]) == 16
    # Cross-check against the O(n^4) brute force.
    import itertools
    A, B, C, D = [2, -1, 0], [3, 1, -2], [-1, 4, 0], [-4, -3, 2]
    brute = sum(
        1 for w, x, y, z in itertools.product(A, B, C, D) if w + x + y + z == 0
    )
    assert four_sum_count(A, B, C, D) == brute
    # Scale: n = 200 means 1.6e9 for the brute force, 4e4 for this.
    n = 200
    big = list(range(n))
    negs = [-v for v in big]
    assert four_sum_count(big, negs, [0] * n, [0] * n) > 0
