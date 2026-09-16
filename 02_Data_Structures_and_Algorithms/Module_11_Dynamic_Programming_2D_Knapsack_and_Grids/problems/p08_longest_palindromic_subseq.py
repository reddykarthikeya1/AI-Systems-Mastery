"""Problem 08 — Longest Palindromic Subsequence

Pattern:    Interval DP
Difficulty: Hard
Target:     Time O(n^2), Space O(n^2)

Return the length of the longest palindromic **subsequence** (not substring —
the characters need not be contiguous).

Constraints
- ``0 <= len(s) <= 1000``

Example
    longest_palindromic_subseq("bbbab") -> 4     ("bbbb")
    longest_palindromic_subseq("cbbd")  -> 2     ("bb")

Hints — read one at a time, and try again between each.

    Hint 1: There is a one-line answer: it is the LCS of s with its own reverse. Convince yourself why that works.
    Hint 2: Or solve it directly as interval DP: best[i][j] is the answer for the substring s[i..j].
    Hint 3: If the ends match, best[i][j] = 2 + best[i+1][j-1]; otherwise max(best[i+1][j], best[i][j-1]). Fill by increasing interval LENGTH, so every shorter interval is ready when you need it.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def longest_palindromic_subseq(s: str) -> int:
    raise NotImplementedError("implement longest_palindromic_subseq")
