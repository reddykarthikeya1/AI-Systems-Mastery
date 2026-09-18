"""Problem 08 — Reorganize String

Pattern:    Greedy with a max-heap
Difficulty: Hard
Target:     Time O(n log 26), Space O(n)

Rearrange ``s`` so that no two adjacent characters are equal. Return any valid
arrangement, or ``""`` if it is impossible.

Constraints
- ``1 <= len(s) <= 500``
- lowercase letters

Example
    reorganize_string("aab")  -> "aba"
    reorganize_string("aaab") -> ""

Example:
    >>> reorganize_string("aab")
    'aba'
    >>> reorganize_string("aaab")
    ''

Hints — read one at a time, and try again between each.

    Hint 1: When is it impossible? Think about the most frequent character and how many slots it needs.
    Hint 2: It is impossible exactly when some character's count exceeds (len(s) + 1) // 2.
    Hint 3: Otherwise, greedily place the most frequent remaining character that is not the one you just placed. A max-heap of (count, char) gives you that in O(log 26); hold the just-placed character aside for one step.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def reorganize_string(s: str) -> str:
    raise NotImplementedError("implement reorganize_string")
