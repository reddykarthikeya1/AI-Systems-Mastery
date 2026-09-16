"""Problem 08 — Longest Palindromic Substring

Pattern:    Expand around centre
Difficulty: Medium
Target:     Time O(n^2), Space O(1)

Return the longest palindromic substring of ``s``. If several have the same
maximum length, return the one that starts earliest.

Constraints
- ``0 <= len(s) <= 1000``  -> O(n^2) is acceptable
- lowercase and uppercase letters and digits

Example
    longest_palindrome("babad") -> "bab"
    longest_palindrome("cbbd")  -> "bb"

Hints — read one at a time, and try again between each.

    Hint 1: Every palindrome has a centre. How many centres does a string of length n have?
    Hint 2: 2n - 1: each character, and each gap between characters. Odd-length palindromes centre on a character, even-length ones on a gap.
    Hint 3: For each centre, expand outward while the characters match, and keep the longest span. Handling only the odd case is the usual bug - it fails on 'cbbd'.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def longest_palindrome(s: str) -> str:
    raise NotImplementedError("implement longest_palindrome")
