"""Reference solution — Problem 08: Partition Labels

Pattern:    Greedy with last-occurrence bounds
Complexity: Time O(n), Space O(alphabet)
"""

from __future__ import annotations


def partition_labels(s: str) -> list[int]:
    # Last index of every letter, so a part's minimum extent is known up front.
    last = {ch: i for i, ch in enumerate(s)}

    out: list[int] = []
    start = 0
    end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            # Every letter in s[start..i] is fully contained here.
            out.append(i - start + 1)
            start = i + 1
    return out
