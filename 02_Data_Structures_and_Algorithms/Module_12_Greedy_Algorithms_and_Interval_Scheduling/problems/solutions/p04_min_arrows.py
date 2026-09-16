"""Reference solution — Problem 04: Minimum Arrows To Burst Balloons

Pattern:    Sort by END, then greedy
Complexity: Time O(n log n), Space O(1)
"""

from __future__ import annotations


def min_arrows(balloons: list[tuple[int, int]]) -> int:
    if not balloons:
        return 0

    arrows = 0
    last_shot = float("-inf")
    # Sort by END: firing at the earliest end bursts that balloon and as many
    # others as possible.
    for start, end in sorted(balloons, key=lambda b: b[1]):
        if start > last_shot:
            arrows += 1
            last_shot = end
    return arrows
