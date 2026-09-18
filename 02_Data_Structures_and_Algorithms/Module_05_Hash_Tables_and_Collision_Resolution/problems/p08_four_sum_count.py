"""Problem 08 — Four Sum Count (Two Hash Maps)

Pattern:    Meet in the middle with a hash map
Difficulty: Hard
Target:     Time O(n^2), Space O(n^2)

Given four equal-length lists, count the tuples ``(i, j, k, l)`` such that
``a[i] + b[j] + c[k] + d[l] == 0``.

Constraints
- ``1 <= n <= 200``  -> O(n^4) is 1.6 * 10^9 and too slow; O(n^2) is the target
- values fit in an int

Example
    a=[1,2], b=[-2,-1], c=[-1,2], d=[0,2] -> 2

Example:
    >>> four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2])
    2

Hints — read one at a time, and try again between each.

    Hint 1: Four nested loops is O(n^4). Split the problem in half.
    Hint 2: Count every pairwise sum of a and b in a dict. Then for every pairwise sum of c and d, look up its negation.
    Hint 3: The counts multiply: if sum X occurs p times in the first half and -X occurs q times in the second, that contributes p * q tuples.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def four_sum_count(a: list[int], b: list[int], c: list[int], d: list[int]) -> int:
    raise NotImplementedError("implement four_sum_count")
