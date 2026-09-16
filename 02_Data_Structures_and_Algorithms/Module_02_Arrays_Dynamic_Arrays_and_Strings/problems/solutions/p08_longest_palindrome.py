"""Reference solution — Problem 08: Longest Palindromic Substring

Pattern:    Expand around centre
Complexity: Time O(n^2), Space O(1)
"""

from __future__ import annotations


def longest_palindrome(s: str) -> str:
    if not s:
        return ""

    best_start, best_len = 0, 1

    def expand(left: int, right: int) -> None:
        nonlocal best_start, best_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # The loop overshoots by one on each side.
        length = right - left - 1
        if length > best_len:
            best_len = length
            best_start = left + 1

    for i in range(len(s)):
        expand(i, i)          # odd length, centred on a character
        expand(i, i + 1)      # even length, centred on a gap

    return s[best_start : best_start + best_len]
