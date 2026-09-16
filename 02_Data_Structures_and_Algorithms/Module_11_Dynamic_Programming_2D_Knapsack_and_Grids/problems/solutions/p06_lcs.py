"""Reference solution — Problem 06: Longest Common Subsequence

Pattern:    2D sequence DP
Complexity: Time O(n*m), Space O(min(n, m))
"""

from __future__ import annotations


def lcs(a: str, b: str) -> int:
    n, m = len(a), len(b)
    prev = [0] * (m + 1)

    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1        # the matched character joins
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur

    return prev[m]
