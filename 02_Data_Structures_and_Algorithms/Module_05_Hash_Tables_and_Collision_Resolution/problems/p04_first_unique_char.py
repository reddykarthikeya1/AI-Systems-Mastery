"""Problem 04 — First Unique Character

Pattern:    Frequency counting
Difficulty: Easy
Target:     Time O(n), Space O(alphabet)

Return the index of the first character that appears exactly once, or ``-1`` if
there is none.

Constraints
- ``0 <= len(s) <= 10**5``
- lowercase letters

Example
    "leetcode"   -> 0
    "loveleetcode" -> 2
    "aabb"       -> -1

Example:
    >>> first_unique_char("leetcode")
    0
    >>> first_unique_char("aabb")
    -1

Hints — read one at a time, and try again between each.

    Hint 1: You cannot know a character is unique until you have seen the whole string. So one pass is not enough.
    Hint 2: Count every character first.
    Hint 3: Then scan again in order and return the first index whose count is 1. The second scan must go in string order, not dict order.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def first_unique_char(s: str) -> int:
    raise NotImplementedError("implement first_unique_char")
