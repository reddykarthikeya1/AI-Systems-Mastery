"""Reference solution — Problem 01: Group Anagrams

Pattern:    Hash map with a canonical key
Complexity: Time O(total characters), Space O(total characters)
"""

from __future__ import annotations


def group_anagrams(words: list[str]) -> list[list[str]]:
    buckets: dict[tuple[int, ...], list[str]] = {}

    for word in words:
        # A 26-slot count tuple is a canonical form computable in O(len(word)),
        # versus O(len(word) log len(word)) for sorting the letters.
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord("a")] += 1
        buckets.setdefault(tuple(counts), []).append(word)

    return sorted(buckets.values(), key=lambda group: group[0])
