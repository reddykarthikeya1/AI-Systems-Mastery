"""Reference solution - Problem 03: Is the String a Repeated Block?

Pattern:    String period
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def is_repeated_pattern(s: str) -> bool:
    n = len(s)
    if n < 2:
        return False
    pi = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    period = n - pi[-1]
    return period < n and n % period == 0
