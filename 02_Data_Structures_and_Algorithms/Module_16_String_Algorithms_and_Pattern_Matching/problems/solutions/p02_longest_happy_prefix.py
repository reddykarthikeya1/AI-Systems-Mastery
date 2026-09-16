"""Reference solution - Problem 02: Longest Prefix That Is Also a Suffix

Pattern:    KMP prefix function
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def longest_happy_prefix(s: str) -> str:
    if len(s) < 2:
        return ""
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return s[:pi[-1]]
