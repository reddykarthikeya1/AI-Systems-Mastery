"""Reference solution - Problem 05: All Occurrences, Overlaps Included

Pattern:    Linear-time string search
Complexity: Time O(n + m), Space O(m)
"""

from __future__ import annotations


def find_all(text: str, pattern: str) -> list[int]:
    if not pattern:
        return []
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k

    found = []
    k = 0
    for i, character in enumerate(text):
        while k > 0 and character != pattern[k]:
            k = pi[k - 1]
        if character == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - len(pattern) + 1)
            k = pi[k - 1]
    return found
