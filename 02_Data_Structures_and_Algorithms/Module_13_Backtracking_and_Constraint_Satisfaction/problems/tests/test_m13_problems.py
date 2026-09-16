"""Problem-bank suite for Module_13_Backtracking_and_Constraint_Satisfaction.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_subsets import subsets
from p02_permutations import permutations
from p03_subsets_with_dups import subsets_with_dups
from p04_combination_sum import combination_sum
from p05_generate_parentheses import generate_parentheses
from p06_word_search import word_search
from p07_n_queens import n_queens
from p08_palindrome_partition import palindrome_partition


def test_p01_subsets():
    """All Subsets — Backtracking (Medium)."""
    assert subsets([1, 2, 3]) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert subsets([]) == [[]]
    assert subsets([1]) == [[], [1]]
    assert subsets([1, 2]) == [[], [1], [1, 2], [2]]
    # There must be exactly 2^n subsets, all distinct.
    for n in range(0, 9):
        got = subsets(list(range(n)))
        assert len(got) == 2 ** n, n
        assert len({tuple(x) for x in got}) == 2 ** n, n
    # Every subset must be a real subset, and each element sorted.
    data = [4, 1, 7]
    got = subsets(data)
    assert all(set(sub) <= set(data) for sub in got)
    assert all(sub == sorted(sub) for sub in got)

def test_p02_permutations():
    """All Permutations — Backtracking with a used set (Medium)."""
    assert permutations([1, 2, 3]) == [
        [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1],
    ]
    assert permutations([1]) == [[1]]
    assert permutations([1, 2]) == [[1, 2], [2, 1]]
    # There must be exactly n! permutations, all distinct.
    import math
    for n in range(1, 7):
        got = permutations(list(range(n)))
        assert len(got) == math.factorial(n), n
        assert len({tuple(x) for x in got}) == math.factorial(n), n
    # Cross-check against itertools.
    import itertools
    for data in ([1, 2, 3], [5, 1, 9], [2, 4]):
        expected = sorted(list(p) for p in itertools.permutations(sorted(data)))
        assert permutations(data) == expected, data

def test_p03_subsets_with_dups():
    """Subsets With Duplicates — Backtracking with duplicate skipping (Medium)."""
    assert subsets_with_dups([1, 2, 2]) == [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    assert subsets_with_dups([]) == [[]]
    assert subsets_with_dups([1, 1]) == [[], [1], [1, 1]]
    # No duplicates: identical to the plain power set.
    assert subsets_with_dups([1, 2, 3]) == subsets([1, 2, 3])
    # All identical: n+1 subsets, one of each length.
    assert subsets_with_dups([2, 2, 2]) == [[], [2], [2, 2], [2, 2, 2]]
    # The results must be unique.
    for data in ([1, 2, 2], [4, 4, 4, 1, 4], [1, 1, 2, 2], [0]):
        got = subsets_with_dups(data)
        assert len({tuple(x) for x in got}) == len(got), data
    # Cross-check against dedup-after-the-fact.
    import itertools
    for data in ([1, 2, 2], [1, 1, 2, 2], [3, 3, 3]):
        expected = sorted(
            {tuple(sorted(c)) for r in range(len(data) + 1)
             for c in itertools.combinations(sorted(data), r)}
        )
        assert [tuple(x) for x in subsets_with_dups(data)] == expected, data

def test_p04_combination_sum():
    """Combination Sum — Backtracking with reuse (Medium)."""
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    # No combination reaches the target.
    assert combination_sum([2], 1) == []
    assert combination_sum([3, 5], 1) == []
    # Exact single candidate.
    assert combination_sum([7], 7) == [[7]]
    # Unlimited reuse of one candidate.
    assert combination_sum([2], 6) == [[2, 2, 2]]
    # Every result must sum to the target and be sorted.
    for cands, tgt in (([2, 3, 6, 7], 7), ([2, 3, 5], 8), ([1, 2], 4)):
        got = combination_sum(cands, tgt)
        assert all(sum(c) == tgt for c in got), (cands, tgt)
        assert all(c == sorted(c) for c in got), (cands, tgt)
        assert len({tuple(c) for c in got}) == len(got), (cands, tgt)

def test_p05_generate_parentheses():
    """Generate Valid Parentheses — Backtracking with validity pruning (Medium)."""
    assert generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert generate_parentheses(1) == ["()"]
    assert generate_parentheses(0) == [""]
    assert generate_parentheses(2) == ["(())", "()()"]
    with pytest.raises(ValueError):
        generate_parentheses(-1)
    # The count is the nth Catalan number.
    import math
    for n in range(0, 8):
        expected = math.comb(2 * n, n) // (n + 1)
        assert len(generate_parentheses(n)) == expected, n
    # Every output must be balanced and the right length.
    for n in range(0, 7):
        for text in generate_parentheses(n):
            assert len(text) == 2 * n
            depth = 0
            for ch in text:
                depth += 1 if ch == "(" else -1
                assert depth >= 0, text
            assert depth == 0, text

def test_p06_word_search():
    """Word Search In A Grid — Backtracking on a grid (Medium)."""
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert word_search(board, "ABCCED") is True
    assert word_search(board, "SEE") is True
    # The second B would have to reuse the first cell.
    assert word_search(board, "ABCB") is False
    assert word_search(board, "") is False
    assert word_search([["A"]], "A") is True
    assert word_search([["A"]], "B") is False
    assert word_search([["A"]], "AA") is False
    # Diagonal movement is not allowed.
    assert word_search([["A", "B"], ["C", "D"]], "AD") is False
    assert word_search([["A", "B"], ["C", "D"]], "AB") is True
    assert word_search([["A", "B"], ["C", "D"]], "ABDC") is True
    # The board must be intact afterwards.
    snapshot = [row[:] for row in board]
    word_search(board, "ABCCED")
    word_search(board, "NOPE")
    assert board == snapshot, "word_search must restore the board"

def test_p07_n_queens():
    """N-Queens — Backtracking with constraint pruning (Hard)."""
    assert n_queens(1) == 1
    # No solution exists for 2 or 3.
    assert n_queens(2) == 0
    assert n_queens(3) == 0
    assert n_queens(4) == 2
    assert n_queens(5) == 10
    assert n_queens(6) == 4
    assert n_queens(7) == 40
    assert n_queens(8) == 92
    assert n_queens(9) == 352
    # The empty board.
    assert n_queens(0) == 1
    with pytest.raises(ValueError):
        n_queens(-1)

def test_p08_palindrome_partition():
    """Palindrome Partitioning — Backtracking with a validity check (Hard)."""
    assert palindrome_partition("aab") == [["a", "a", "b"], ["aa", "b"]]
    assert palindrome_partition("a") == [["a"]]
    # No multi-character palindrome exists, so only singletons.
    assert palindrome_partition("abc") == [["a", "b", "c"]]
    # All identical characters: every cut pattern works.
    got = palindrome_partition("aaa")
    assert got == [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]
    # Every piece of every partition must be a palindrome, and the, # pieces must reconstruct the original string.
    for text in ("aab", "aaa", "abba", "racecar", "abcba"):
        for parts in palindrome_partition(text):
            assert "".join(parts) == text, (text, parts)
            assert all(p == p[::-1] for p in parts), (text, parts)
    # A whole-string palindrome must appear as a single-piece partition.
    assert ["racecar"] in palindrome_partition("racecar")
    assert ["abba"] in palindrome_partition("abba")
