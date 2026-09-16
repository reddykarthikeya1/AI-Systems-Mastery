"""Problem 03 — Worst-Case Binary Search Comparisons

Pattern:    Complexity analysis
Difficulty: Easy
Target:     Time O(1), Space O(1)

Return the maximum number of comparisons a correct binary search performs on a
sorted array of ``n`` elements, where each comparison halves the remaining
search space.

Constraints
- ``0 <= n <= 10**18``

Example
    max_binary_search_comparisons(1)  -> 1
    max_binary_search_comparisons(8)  -> 4

Note that an array of a *quintillion* elements needs only 60 comparisons. That
number is the entire reason binary search matters.

Hints — read one at a time, and try again between each.

    Hint 1: Each comparison at worst halves the candidate range.
    Hint 2: Ask how many times you can halve n before reaching zero.
    Hint 3: That is floor(log2(n)) + 1 for n >= 1. Use bit_length() to avoid floating-point error at 10**18.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def max_binary_search_comparisons(n: int) -> int:
    raise NotImplementedError("implement max_binary_search_comparisons")
