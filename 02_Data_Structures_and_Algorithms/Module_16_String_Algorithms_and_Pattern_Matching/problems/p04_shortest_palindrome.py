"""Problem 04 - Shortest Palindrome by Prepending

Pattern:    KMP on s + sep + reversed(s)
Difficulty: Hard
Target:     Time O(n), Space O(n)

You may only add characters to the **front** of ``s``. Return the
shortest palindrome you can make.

Constraints
- ``0 <= len(s) <= 5 * 10**4``

Example
    shortest_palindrome("aacecaaa") -> "aaacecaaa"
    shortest_palindrome("abcd")     -> "dcbabcd"
    shortest_palindrome("")         -> ""

The question is really "what is the longest palindromic *prefix* of s" - that
part stays put, and the rest is mirrored in front of it. Finding that prefix in
linear time is the trick worth learning.

Example:
    >>> shortest_palindrome("aacecaaa")
    'aaacecaaa'
    >>> shortest_palindrome("abcd")
    'dcbabcd'

Hints - read one at a time, and try again between each.

    Hint 1: If the longest palindromic prefix has length k, the answer is `reversed(s[k:]) + s`.
    Hint 2: A prefix of `s` that is a palindrome is a prefix of `s` that is also a suffix of `reversed(s)`.
    Hint 3: So build the prefix table of `s + separator + reversed(s)` and read its last entry. The separator must be a character that appears in neither, or the match can run across the join.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def shortest_palindrome(s: str) -> str:
    raise NotImplementedError("implement shortest_palindrome")
