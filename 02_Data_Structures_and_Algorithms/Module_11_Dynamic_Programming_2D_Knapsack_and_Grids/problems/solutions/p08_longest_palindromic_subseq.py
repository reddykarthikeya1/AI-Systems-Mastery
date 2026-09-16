"""Reference solution — Problem 08: Longest Palindromic Subsequence

Pattern:    Interval DP
Complexity: Time O(n^2), Space O(n^2)
"""

from __future__ import annotations


def longest_palindromic_subseq(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0

    # Interval DP. best[i][j] covers s[i..j] inclusive.
    best = [[0] * n for _ in range(n)]
    for i in range(n):
        best[i][i] = 1              # a single character is a palindrome

    # Fill by increasing interval length so the shorter ones are already done.
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                inner = best[i + 1][j - 1] if length > 2 else 0
                best[i][j] = inner + 2
            else:
                best[i][j] = max(best[i + 1][j], best[i][j - 1])

    return best[0][n - 1]
