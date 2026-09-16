"""Problem-bank suite for Module_11_Dynamic_Programming_2D_Knapsack_and_Grids.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_unique_paths import unique_paths
from p02_min_path_sum import min_path_sum
from p03_edit_distance import edit_distance
from p04_knapsack_01 import knapsack_01
from p05_can_partition import can_partition
from p06_lcs import lcs
from p07_unique_paths_obstacles import unique_paths_obstacles
from p08_longest_palindromic_subseq import longest_palindromic_subseq


def test_p01_unique_paths():
    """Unique Paths In A Grid — 2D grid DP (Medium)."""
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    assert unique_paths(1, 1) == 1
    # A single row or column has exactly one path.
    assert unique_paths(1, 10) == 1
    assert unique_paths(10, 1) == 1
    assert unique_paths(2, 2) == 2
    # Symmetric in its arguments.
    assert unique_paths(3, 7) == unique_paths(7, 3)
    with pytest.raises(ValueError):
        unique_paths(0, 5)
    # It is a binomial coefficient: C(m+n-2, m-1).
    import math
    for m in range(1, 9):
        for n in range(1, 9):
            assert unique_paths(m, n) == math.comb(m + n - 2, m - 1), (m, n)

def test_p02_min_path_sum():
    """Minimum Path Sum — 2D grid DP (Medium)."""
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert min_path_sum([[1, 2, 3], [4, 5, 6]]) == 12
    assert min_path_sum([[5]]) == 5
    # A single row or column is just the total.
    assert min_path_sum([[1, 2, 3]]) == 6
    assert min_path_sum([[1], [2], [3]]) == 6
    # Negative values are handled by the same recurrence.
    assert min_path_sum([[1, -1], [-1, 1]]) == 1
    with pytest.raises(ValueError):
        min_path_sum([])
    # Cross-check against exhaustive path enumeration.
    import itertools
    def brute(g):
        rows, cols = len(g), len(g[0])
        best = None
        for moves in itertools.permutations('D' * (rows - 1) + 'R' * (cols - 1)):
            r = c = 0
            total = g[0][0]
            for mv in moves:
                if mv == 'D':
                    r += 1
                else:
                    c += 1
                total += g[r][c]
            best = total if best is None else min(best, total)
        return best if best is not None else g[0][0]
    for g in ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], [[2, 1], [1, 9]], [[1, 2, 3], [4, 5, 6]]):
        assert min_path_sum(g) == brute(g), g

def test_p03_edit_distance():
    """Edit Distance — 2D sequence DP (Hard)."""
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    # Empty strings.
    assert edit_distance("", "") == 0
    assert edit_distance("abc", "") == 3
    assert edit_distance("", "abc") == 3
    # Identical strings cost nothing.
    assert edit_distance("same", "same") == 0
    # A single operation of each kind.
    assert edit_distance("cat", "cats") == 1
    assert edit_distance("cats", "cat") == 1
    assert edit_distance("cat", "bat") == 1
    # Symmetric: insertions and deletions mirror each other.
    for x, y in (("horse", "ros"), ("abc", "yabd"), ("kitten", "sitting")):
        assert edit_distance(x, y) == edit_distance(y, x), (x, y)
    assert edit_distance("kitten", "sitting") == 3
    # The distance never exceeds the longer length.
    for x, y in (("abcdef", "uvwxyz"), ("a", "bcdefg")):
        assert edit_distance(x, y) <= max(len(x), len(y))

def test_p04_knapsack_01():
    """0/1 Knapsack — 0/1 knapsack DP (Hard)."""
    assert knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    assert knapsack_01([], [], 10) == 0
    assert knapsack_01([5], [10], 4) == 0
    assert knapsack_01([5], [10], 5) == 10
    assert knapsack_01([1, 2, 3], [6, 10, 12], 5) == 22
    # Zero capacity takes nothing.
    assert knapsack_01([1, 2], [5, 5], 0) == 0
    with pytest.raises(ValueError):
        knapsack_01([1], [1, 2], 5)
    # THE key case: one item may be taken only once. Unbounded knapsack
    # would answer 30 here (three copies of the weight-1 item).
    assert knapsack_01([1], [10], 3) == 10
    assert knapsack_01([2, 3], [10, 12], 6) == 22
    # Cross-check against exhaustive subset enumeration.
    import itertools
    cases = [
        ([1, 3, 4, 5], [1, 4, 5, 7], 7),
        ([2, 2, 3], [3, 4, 5], 5),
        ([4, 5, 6], [10, 20, 30], 10),
        ([1, 1, 1, 1], [1, 2, 3, 4], 2),
    ]
    for ws, vs, cap in cases:
        brute = 0
        for r in range(len(ws) + 1):
            for combo in itertools.combinations(range(len(ws)), r):
                if sum(ws[i] for i in combo) <= cap:
                    brute = max(brute, sum(vs[i] for i in combo))
        assert knapsack_01(ws, vs, cap) == brute, (ws, vs, cap)

def test_p05_can_partition():
    """Partition Equal Subset Sum — Subset-sum DP (Medium)."""
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False
    # A single element can never be split.
    assert can_partition([1]) is False
    assert can_partition([2]) is False
    # Two equal elements split trivially.
    assert can_partition([3, 3]) is True
    # Odd total short-circuits.
    assert can_partition([1, 1, 1]) is False
    assert can_partition([2, 2, 2]) is False
    # One number used twice would wrongly succeed here.
    assert can_partition([1, 1]) is True
    assert can_partition([1, 3]) is False
    # Cross-check against exhaustive subsets.
    import itertools
    for data in ([1, 5, 11, 5], [1, 2, 3, 5], [2, 2, 1, 1], [3, 3, 3, 4, 5], [1, 2, 5]):
        total = sum(data)
        brute = total % 2 == 0 and any(
            sum(c) == total // 2
            for r in range(len(data) + 1)
            for c in itertools.combinations(data, r)
        )
        assert can_partition(data) is brute, data

def test_p06_lcs():
    """Longest Common Subsequence — 2D sequence DP (Medium)."""
    assert lcs("abcde", "ace") == 3
    assert lcs("abc", "abc") == 3
    assert lcs("abc", "def") == 0
    assert lcs("", "") == 0
    assert lcs("abc", "") == 0
    # A subsequence need not be contiguous.
    assert lcs("abcdefg", "aceg") == 4
    # Reversed strings share only single characters.
    assert lcs("abcd", "dcba") == 1
    # Repeated characters.
    assert lcs("aaaa", "aa") == 2
    # Symmetric.
    for x, y in (("abcde", "ace"), ("abcdefg", "aceg"), ("xyz", "xz")):
        assert lcs(x, y) == lcs(y, x), (x, y)
    # The LCS never exceeds the shorter string.
    for x, y in (("abc", "abcdef"), ("a", "bbbb")):
        assert lcs(x, y) <= min(len(x), len(y))

def test_p07_unique_paths_obstacles():
    """Unique Paths With Obstacles — 2D grid DP with blocked cells (Medium)."""
    assert unique_paths_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert unique_paths_obstacles([[0, 1], [0, 0]]) == 1
    # Blocked start and blocked end.
    assert unique_paths_obstacles([[1]]) == 0
    assert unique_paths_obstacles([[1, 0], [0, 0]]) == 0
    assert unique_paths_obstacles([[0, 0], [0, 1]]) == 0
    # A single open cell.
    assert unique_paths_obstacles([[0]]) == 1
    # A full wall.
    assert unique_paths_obstacles([[0, 0, 0], [1, 1, 1], [0, 0, 0]]) == 0
    # No obstacles: must match plain unique_paths.
    for r in range(1, 6):
        for c in range(1, 6):
            clear = [[0] * c for _ in range(r)]
            assert unique_paths_obstacles(clear) == unique_paths(r, c), (r, c)

def test_p08_longest_palindromic_subseq():
    """Longest Palindromic Subsequence — Interval DP (Hard)."""
    assert longest_palindromic_subseq("bbbab") == 4
    assert longest_palindromic_subseq("cbbd") == 2
    assert longest_palindromic_subseq("") == 0
    assert longest_palindromic_subseq("a") == 1
    # No repeated character: any single one is the best.
    assert longest_palindromic_subseq("abcd") == 1
    # Already a palindrome.
    assert longest_palindromic_subseq("racecar") == 7
    assert longest_palindromic_subseq("aaaa") == 4
    # Even-length core.
    assert longest_palindromic_subseq("abba") == 4
    # It equals the LCS of the string with its reverse.
    for text in ("bbbab", "cbbd", "agbdba", "character", "abcdefgh"):
        assert longest_palindromic_subseq(text) == lcs(text, text[::-1]), text
