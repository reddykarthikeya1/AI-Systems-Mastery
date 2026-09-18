"""Problem 04 — Find All Dictionary Words With A Prefix

Pattern:    Trie traversal
Difficulty: Medium
Target:     Time O(total chars + limit * len), Space O(total chars)

Return up to ``limit`` dictionary words starting with ``prefix``, in
lexicographic order.

Constraints
- ``0 <= len(words) <= 10**4``
- ``0 <= len(prefix) <= 100``

Example
    words_with_prefix(["cat","car","card","dog"], "car") -> ["car", "card"]

Example:
    >>> words_with_prefix(["cat", "car", "card", "dog"], "car")
    ['car', 'card']

Hints — read one at a time, and try again between each.

    Hint 1: Build a trie, walk to the prefix node, then collect every word beneath it.
    Hint 2: Walk children in sorted key order and the results come out lexicographically with no final sort.
    Hint 3: Stop as soon as you have `limit` results - that is what makes this usable for autocomplete, where the dictionary is huge and the limit is small.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def words_with_prefix(words: list[str], prefix: str, limit: int = 10) -> list[str]:
    raise NotImplementedError("implement words_with_prefix")
