"""Problem 04 — Minimum Arrows To Burst Balloons

Pattern:    Sort by END, then greedy
Difficulty: Medium
Target:     Time O(n log n), Space O(1)

Each balloon spans ``[start, end]``. A vertical arrow at ``x`` bursts every
balloon with ``start <= x <= end``. Return the minimum number of arrows needed
to burst them all.

Constraints
- ``0 <= len(balloons) <= 10**4``

Example
    min_arrows([(10,16), (2,8), (1,6), (7,12)]) -> 2

Hints — read one at a time, and try again between each.

    Hint 1: Same family as the previous problem. Where should an arrow go to burst as much as possible?
    Hint 2: At the earliest END among the balloons still unburst - any further right and you miss that balloon.
    Hint 3: So sort by end, fire at the first end, and skip every balloon that point already bursts.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def min_arrows(balloons: list[tuple[int, int]]) -> int:
    raise NotImplementedError("implement min_arrows")
