"""Reference solution — Problem 03: Worst-Case Binary Search Comparisons

Pattern:    Complexity analysis
Complexity: Time O(1), Space O(1)
"""

from __future__ import annotations


def max_binary_search_comparisons(n: int) -> int:
    if n <= 0:
        return 0
    # n.bit_length() == floor(log2(n)) + 1 exactly, with no float rounding -
        # math.log2(10**18) is not exactly representable and would round wrong.
    return n.bit_length()
