"""Problem-bank suite for Module_01_Complexity_Analysis_and_Memory_Layout.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_classify_growth import classify_growth
from p02_amortized_copies import total_copies_for_appends
from p03_binary_search_steps import max_binary_search_comparisons
from p04_pair_iterations import count_pair_iterations
from p05_fits_budget import fits_budget
from p06_row_major import row_major_index


def test_p01_classify_growth():
    """Classify Empirical Growth Rate — Complexity analysis (Easy)."""
    assert classify_growth([(1000, 0.001), (2000, 0.001), (4000, 0.001)]) == "O(1)"
    assert classify_growth([(1000, 0.001), (2000, 0.002), (4000, 0.004)]) == "O(n)"
    assert classify_growth([(1000, 0.001), (2000, 0.004), (4000, 0.016)]) == "O(n^2)"
    # Noise must not flip the classification.
    assert classify_growth([(100, 0.0010), (200, 0.0021), (400, 0.0039)]) == "O(n)"
    # A single measurement carries no growth information.
    assert classify_growth([(100, 0.001)]) == "O(1)"

def test_p02_amortized_copies():
    """Total Copies Under Geometric Growth — Amortized analysis (Medium)."""
    assert total_copies_for_appends(0) == 0
    assert total_copies_for_appends(1) == 0
    assert total_copies_for_appends(2) == 1
    assert total_copies_for_appends(5) == 7
    assert total_copies_for_appends(5, initial_capacity=8) == 0
    # The defining property: total copies stay linear in n, so the, # per-append average is bounded by a constant.
    for n in (1000, 100_000, 10**9):
        assert total_copies_for_appends(n) < 2 * n
    # And it must be computed, not simulated - this would hang if the, # implementation looped per element.
    assert total_copies_for_appends(10**9) > 0

def test_p03_binary_search_steps():
    """Worst-Case Binary Search Comparisons — Complexity analysis (Easy)."""
    assert max_binary_search_comparisons(0) == 0
    assert max_binary_search_comparisons(1) == 1
    assert max_binary_search_comparisons(2) == 2
    assert max_binary_search_comparisons(7) == 3
    assert max_binary_search_comparisons(8) == 4
    assert max_binary_search_comparisons(10**6) == 20
    # The headline: a quintillion elements, 60 comparisons.
    assert max_binary_search_comparisons(10**18) == 60

def test_p04_pair_iterations():
    """Count Distinct Pair Iterations — Complexity analysis (Easy)."""
    assert count_pair_iterations(0) == 0
    assert count_pair_iterations(1) == 0
    assert count_pair_iterations(2) == 1
    assert count_pair_iterations(4) == 6
    assert count_pair_iterations(1000) == 499_500
    # Must be exact, not floating point, at this magnitude.
    assert count_pair_iterations(10**9) == 499_999_999_500_000_000
    assert isinstance(count_pair_iterations(10**9), int)
    # Cross-check the closed form against a real nested loop.
    for n in range(8):
        brute = sum(1 for i in range(n) for _ in range(i + 1, n))
        assert count_pair_iterations(n) == brute

def test_p05_fits_budget():
    """Does This Complexity Fit The Constraint? — Complexity analysis (Medium)."""
    assert fits_budget(10**9, "O(1)") is True
    assert fits_budget(10**9, "O(log n)") is True
    assert fits_budget(10**8, "O(n)") is True
    assert fits_budget(10**9, "O(n)") is False
    assert fits_budget(100_000, "O(n log n)") is True
    assert fits_budget(100_000, "O(n^2)") is False
    assert fits_budget(5_000, "O(n^2)") is True
    assert fits_budget(400, "O(n^3)") is True
    assert fits_budget(10_000, "O(n^3)") is False
    assert fits_budget(20, "O(2^n)") is True
    assert fits_budget(100, "O(2^n)") is False
    assert fits_budget(10, "O(n!)") is True
    assert fits_budget(30, "O(n!)") is False
    # A typo must raise, not quietly return False.
    with pytest.raises(ValueError):
        fits_budget(10, "O(n^4)")
    with pytest.raises(ValueError):
        fits_budget(0, "O(n)")
    # These must return fast rather than build a huge integer.
    assert fits_budget(10**9, "O(2^n)") is False
    assert fits_budget(10**9, "O(n!)") is False

def test_p06_row_major():
    """Row-Major Memory Layout — Memory layout (Easy)."""
    assert row_major_index(3, 4, 0, 0) == 0
    assert row_major_index(3, 4, 0, 3) == 3
    assert row_major_index(3, 4, 1, 0) == 4
    assert row_major_index(3, 4, 1, 2) == 6
    assert row_major_index(3, 4, 2, 3) == 11
    # Every cell maps to a distinct offset, and they tile 0..rows*cols-1.
    seen = {row_major_index(3, 4, r, c) for r in range(3) for c in range(4)}
    assert seen == set(range(12))
    # Out-of-range must raise, not wrap around into another row.
    with pytest.raises(IndexError):
        row_major_index(3, 4, 0, 4)
    with pytest.raises(IndexError):
        row_major_index(3, 4, 3, 0)
    with pytest.raises(IndexError):
        row_major_index(3, 4, -1, 0)
