"""Problem 06 — Longest Common Subsequence

Pattern:    2D sequence DP
Difficulty: Medium
Target:     Time O(n*m), Space O(min(n, m))

Return the length of the longest subsequence common to both strings. A
subsequence keeps relative order but need not be contiguous.

Constraints
- ``0 <= len(a), len(b) <= 1000``

Example
    lcs("abcde", "ace") -> 3      ("ace")
    lcs("abc", "def")   -> 0

Hints — read one at a time, and try again between each.

    Hint 1: State: length of the LCS of the first i characters of a and the first j of b.
    Hint 2: If the characters match, that character joins the LCS: 1 + the value diagonally back.
    Hint 3: If not, drop one character from either string and take the better: max(above, left). Note this is NOT the same as edit distance, even though the table has the same shape.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def lcs(a: str, b: str) -> int:
    raise NotImplementedError("implement lcs")
