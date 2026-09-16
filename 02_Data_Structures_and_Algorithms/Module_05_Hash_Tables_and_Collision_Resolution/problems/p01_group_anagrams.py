"""Problem 01 — Group Anagrams

Pattern:    Hash map with a canonical key
Difficulty: Medium
Target:     Time O(total characters), Space O(total characters)

Group the words that are anagrams of one another.

Return the groups sorted by their first element, and each group in the order the
words appeared in the input. This makes the output deterministic and testable.

Constraints
- ``0 <= len(words) <= 10**4``
- lowercase letters only

Example
    ["eat","tea","tan","ate","nat","bat"]
    -> [["bat"], ["eat","tea","ate"], ["tan","nat"]]

Hints — read one at a time, and try again between each.

    Hint 1: Two words are anagrams exactly when some canonical form of them is equal. What canonical form?
    Hint 2: Sorted letters works: 'eat' and 'tea' both become 'aet'. A 26-element count tuple works too, and is O(n) per word instead of O(n log n).
    Hint 3: Use that canonical form as a dict key and append the original word to the bucket.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def group_anagrams(words: list[str]) -> list[list[str]]:
    raise NotImplementedError("implement group_anagrams")
