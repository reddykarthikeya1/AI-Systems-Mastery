"""Reference solution — Problem 05: Word Break

Pattern:    1D DP over string prefixes
Complexity: Time O(n * longest_word), Space O(n)
"""

from __future__ import annotations


def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)              # O(1) membership, not O(len(dict))
    n = len(s)
    reachable = [False] * (n + 1)
    reachable[0] = True                 # the empty prefix is segmentable

    # Bound the inner loop by the longest word: no point testing longer slices.
    longest = max((len(w) for w in words), default=0)

    for i in range(1, n + 1):
        for j in range(max(0, i - longest), i):
            if reachable[j] and s[j:i] in words:
                reachable[i] = True
                break

    return reachable[n]
