"""Problem 02 — Merge K Sorted Lists

Pattern:    Min-heap k-way merge
Difficulty: Hard
Target:     Time O(N log k), Space O(k)

Merge ``k`` sorted lists into one sorted list.

Constraints
- ``0 <= k <= 10**4``, total elements up to ``10**5``
- target O(N log k) where N is the total number of elements — concatenating and
  sorting is O(N log N) and is not the answer being asked for

Example:
    >>> merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])
    [1, 1, 2, 3, 4, 4, 5, 6]

Hints — read one at a time, and try again between each.

    Hint 1: At any moment the next output element is the smallest of the k list heads. Finding that repeatedly is what a heap is for.
    Hint 2: Push one entry per list: (value, which_list, index_within_list).
    Hint 3: Pop the smallest, append it, then push the next element from the same list. Including the list index in the tuple also keeps the comparison total when values tie.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    raise NotImplementedError("implement merge_k_sorted")
