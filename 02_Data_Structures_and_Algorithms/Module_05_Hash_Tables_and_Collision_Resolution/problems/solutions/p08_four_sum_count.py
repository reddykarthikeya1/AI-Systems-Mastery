"""Reference solution — Problem 08: Four Sum Count (Two Hash Maps)

Pattern:    Meet in the middle with a hash map
Complexity: Time O(n^2), Space O(n^2)
"""

from __future__ import annotations


def four_sum_count(a: list[int], b: list[int], c: list[int], d: list[int]) -> int:
    # Meet in the middle: two O(n^2) passes instead of one O(n^4) nest.
    ab: dict[int, int] = {}
    for x in a:
        for y in b:
            ab[x + y] = ab.get(x + y, 0) + 1

    total = 0
    for z in c:
        for w in d:
            # Counts multiply: every matching pair on the left combines with
            # every matching pair on the right.
            total += ab.get(-(z + w), 0)
    return total
