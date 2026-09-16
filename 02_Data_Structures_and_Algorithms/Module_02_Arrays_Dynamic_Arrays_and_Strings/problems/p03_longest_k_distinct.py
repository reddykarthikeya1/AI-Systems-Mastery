"""Problem 03 — Longest Substring With At Most K Distinct Characters

Pattern:    Sliding window (variable)
Difficulty: Medium
Target:     Time O(n), Space O(k)

Return the length of the longest substring of ``s`` containing at most ``k``
distinct characters.

Constraints
- ``0 <= len(s) <= 10**5``  -> O(n) required
- ``0 <= k <= 128``

Example
    longest_k_distinct("eceba", 2) -> 3     ("ece")
    longest_k_distinct("aa", 1)    -> 2

Hints — read one at a time, and try again between each.

    Hint 1: The window's validity is monotone: adding a character can only increase the distinct count, removing one can only decrease it. That is what makes a sliding window correct here.
    Hint 2: Keep a count map of the characters currently inside the window.
    Hint 3: Grow to the right always; while the window has more than k distinct characters, shrink from the left and delete a key when its count hits 0. Forgetting the delete is the classic bug - len(counts) then never falls.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def longest_k_distinct(s: str, k: int) -> int:
    raise NotImplementedError("implement longest_k_distinct")
