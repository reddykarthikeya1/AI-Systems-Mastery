"""Problem 06 — Isomorphic Strings

Pattern:    Two-way hash mapping
Difficulty: Easy
Target:     Time O(n), Space O(alphabet)

Return True if ``s`` can be transformed into ``t`` by replacing characters,
where the replacement is a **bijection**: each character maps to exactly one
character, and no two characters map to the same one.

Constraints
- ``0 <= len(s), len(t) <= 5 * 10**4``

Example
    ("egg", "add")     -> True
    ("foo", "bar")     -> False
    ("badc", "baba")   -> False

Example:
    >>> is_isomorphic("egg", "add")
    True
    >>> is_isomorphic("foo", "bar")
    False

Hints — read one at a time, and try again between each.

    Hint 1: Map each character of s to the corresponding character of t as you scan.
    Hint 2: One map is not enough. 'badc' -> 'baba' satisfies a single forward map but maps both d and c onto a.
    Hint 3: Keep both directions and check both. Any conflict in either direction means not isomorphic.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def is_isomorphic(s: str, t: str) -> bool:
    raise NotImplementedError("implement is_isomorphic")
