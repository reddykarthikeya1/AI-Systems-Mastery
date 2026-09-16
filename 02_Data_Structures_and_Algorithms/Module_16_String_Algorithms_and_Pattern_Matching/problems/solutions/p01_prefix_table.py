"""Reference solution - Problem 01: Build the KMP Prefix Table

Pattern:    KMP prefix function
Complexity: Time O(m), Space O(m)
"""

from __future__ import annotations


def build_prefix_table(pattern: str) -> list[int]:
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi
