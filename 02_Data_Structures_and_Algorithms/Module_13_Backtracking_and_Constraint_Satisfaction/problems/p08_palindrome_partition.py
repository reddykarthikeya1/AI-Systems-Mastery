"""Problem 08 — Palindrome Partitioning

Pattern:    Backtracking with a validity check
Difficulty: Hard
Target:     Time O(n * 2^n), Space O(n) excluding output

Return every way to cut ``s`` into pieces where each piece is a palindrome.
Return the partitions sorted.

Constraints
- ``1 <= len(s) <= 16``

Example
    palindrome_partition("aab") -> [["a", "a", "b"], ["aa", "b"]]

Hints — read one at a time, and try again between each.

    Hint 1: At each position, try every prefix of the remaining string.
    Hint 2: Only recurse on a prefix that is itself a palindrome - that check is the pruning, and without it you enumerate all 2^(n-1) cut positions.
    Hint 3: When the whole string is consumed, record path[:] - a copy, as always.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def palindrome_partition(s: str) -> list[list[str]]:
    raise NotImplementedError("implement palindrome_partition")
