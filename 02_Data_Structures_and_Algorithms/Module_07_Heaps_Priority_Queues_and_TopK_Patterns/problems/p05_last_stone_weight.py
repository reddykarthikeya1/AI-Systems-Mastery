"""Problem 05 — Last Stone Weight

Pattern:    Max-heap simulation
Difficulty: Easy
Target:     Time O(n log n), Space O(n)

Repeatedly take the two heaviest stones and smash them: if they are equal both
are destroyed, otherwise the heavier one is replaced by the difference. Return
the weight of the last remaining stone, or 0 if none remain.

Constraints
- ``1 <= len(stones) <= 30``
- ``1 <= stones[i] <= 1000``

Example
    last_stone_weight([2, 7, 4, 1, 8, 1]) -> 1

Example:
    >>> last_stone_weight([2, 7, 4, 1, 8, 1])
    1

Hints — read one at a time, and try again between each.

    Hint 1: You repeatedly need the two largest of a changing collection. That is a max-heap.
    Hint 2: heapq is a min-heap, so store negated weights.
    Hint 3: Only push the difference back when it is non-zero - pushing a 0 leaves a phantom stone and changes the answer.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def last_stone_weight(stones: list[int]) -> int:
    raise NotImplementedError("implement last_stone_weight")
