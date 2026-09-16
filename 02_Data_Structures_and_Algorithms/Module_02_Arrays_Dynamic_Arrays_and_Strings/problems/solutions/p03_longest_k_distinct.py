"""Reference solution — Problem 03: Longest Substring With At Most K Distinct Characters

Pattern:    Sliding window (variable)
Complexity: Time O(n), Space O(k)
"""

from __future__ import annotations


def longest_k_distinct(s: str, k: int) -> int:
    if k <= 0 or not s:
        return 0

    counts: dict[str, int] = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1

        while len(counts) > k:
            leaving = s[left]
            counts[leaving] -= 1
            # The delete is essential: without it len(counts) never shrinks and
            # the window can never become valid again.
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        best = max(best, right - left + 1)

    return best
