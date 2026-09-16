"""Reference solution - Problem 04: Shortest Palindrome by Prepending

Pattern:    KMP on s + sep + reversed(s)
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def shortest_palindrome(s: str) -> str:
    if not s:
        return ""
    combined = s + "\x00" + s[::-1]
    pi = [0] * len(combined)
    k = 0
    for i in range(1, len(combined)):
        while k > 0 and combined[i] != combined[k]:
            k = pi[k - 1]
        if combined[i] == combined[k]:
            k += 1
        pi[i] = k
    keep = pi[-1]                  # longest palindromic prefix of s
    return s[keep:][::-1] + s
