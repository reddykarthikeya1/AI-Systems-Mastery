"""Reference solution — Problem 04: First Unique Character

Pattern:    Frequency counting
Complexity: Time O(n), Space O(alphabet)
"""

from __future__ import annotations


def first_unique_char(s: str) -> int:
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1

    # Second pass in STRING order - dict order would give an arbitrary answer.
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
