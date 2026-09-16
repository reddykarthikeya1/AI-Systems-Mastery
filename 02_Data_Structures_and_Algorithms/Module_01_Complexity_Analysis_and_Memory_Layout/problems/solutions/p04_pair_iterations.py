"""Reference solution — Problem 04: Count Distinct Pair Iterations

Pattern:    Complexity analysis
Complexity: Time O(1), Space O(1)
"""

from __future__ import annotations


def count_pair_iterations(n: int) -> int:
    if n <= 1:
        return 0
    # Integer division keeps this exact; n*(n-1)/2 would return a float and
    # lose precision above 2**53.
    return n * (n - 1) // 2
