"""Problem 01 — Classify Empirical Growth Rate

Pattern:    Complexity analysis
Difficulty: Easy
Target:     Time O(k), Space O(k) for k measurements

Given measured ``(input_size, elapsed_seconds)`` pairs from the same
algorithm, classify its growth as ``"O(1)"``, ``"O(n)"`` or ``"O(n^2)"``.

The sizes double each step. Compare consecutive *ratios* of elapsed time:
a doubling of ``n`` multiplies runtime by roughly 1 for O(1), 2 for O(n), and
4 for O(n^2).

Constraints
- ``2 <= len(timings) <= 20``, sizes strictly increasing and doubling
- times are positive floats, possibly noisy

Example
    classify_growth([(1000, 0.001), (2000, 0.002), (4000, 0.004)])  -> "O(n)"

Hints — read one at a time, and try again between each.

    Hint 1: Compute the ratio of consecutive elapsed times, not the times themselves.
    Hint 2: Average the ratios so one noisy measurement cannot flip the answer.
    Hint 3: Bucket the mean ratio: below ~1.5 is constant, below ~3 is linear, otherwise quadratic. Midpoints between 1, 2 and 4 give the boundaries.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def classify_growth(timings: list[tuple[int, float]]) -> str:
    raise NotImplementedError("implement classify_growth")
