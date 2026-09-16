"""Problem 05 - All Occurrences, Overlaps Included

Pattern:    Linear-time string search
Difficulty: Medium
Target:     Time O(n + m), Space O(m)

Return every starting index where ``pattern`` occurs in ``text``,
including overlapping occurrences. Return ``[]`` for an empty pattern.

Constraints
- ``0 <= len(text) <= 10**5``, ``0 <= len(pattern) <= 10**4``
- O(n*m) will time out on the scale test, which uses the adversarial input
  ``"a"*50000 + "b"`` searched for ``"a"*1000 + "b"``

Example
    find_all("aaaa", "aa")     -> [0, 1, 2]
    find_all("abababa", "aba") -> [0, 2, 4]
    find_all("abc", "")        -> []

``str.find`` in a loop is acceptable here and is genuinely linear in CPython -
but write it with the prefix table, because the point is to own the mechanism.

Hints - read one at a time, and try again between each.

    Hint 1: Run the same matching loop as KMP over the text, tracking how many pattern characters are currently matched.
    Hint 2: When the count reaches `len(pattern)`, record `i - len(pattern) + 1`.
    Hint 3: Then fall back to `pi[k-1]` rather than 0 - that is what makes overlapping matches appear.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def find_all(text: str, pattern: str) -> list[int]:
    raise NotImplementedError("implement find_all")
