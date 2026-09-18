"""Problem 05 — Word Break

Pattern:    1D DP over string prefixes
Difficulty: Medium
Target:     Time O(n * longest_word), Space O(n)

Return True if ``s`` can be segmented into a sequence of one or more words from
``word_dict``. A word may be reused.

Constraints
- ``1 <= len(s) <= 300``
- ``1 <= len(word_dict) <= 1000``

Example
    word_break("leetcode", ["leet", "code"])       -> True
    word_break("catsandog", ["cats","dog","sand","and","cat"]) -> False

Example:
    >>> word_break("leetcode", ["leet", "code"])
    True
    >>> word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
    False

Hints — read one at a time, and try again between each.

    Hint 1: State: reachable[i] means the first i characters can be segmented.
    Hint 2: Base case: reachable[0] is True - the empty prefix is trivially segmentable.
    Hint 3: Transition: reachable[i] is True if some j < i has reachable[j] and s[j:i] is in the dictionary. Put the dictionary in a set, or the membership test is O(dictionary) per check.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def word_break(s: str, word_dict: list[str]) -> bool:
    raise NotImplementedError("implement word_break")
