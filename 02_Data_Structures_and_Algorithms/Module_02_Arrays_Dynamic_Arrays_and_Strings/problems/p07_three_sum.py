"""Problem 07 — Three Sum

Pattern:    Sorting + two pointers
Difficulty: Medium
Target:     Time O(n^2), Space O(1) beyond the output

Return all **unique** triples that sum to zero. Each triple must be sorted
ascending, and the list of triples must be sorted too.

Constraints
- ``0 <= len(nums) <= 3000``  -> O(n^2) is the target
- ``-10**5 <= nums[i] <= 10**5``

Example
    three_sum([-1, 0, 1, 2, -1, -4]) -> [[-1, -1, 2], [-1, 0, 1]]

Hints — read one at a time, and try again between each.

    Hint 1: Sorting first makes both the deduplication and the inner search easy.
    Hint 2: Fix the first element, then the remaining task is two-sum on a sorted array - which is two pointers from both ends, in O(n).
    Hint 3: Deduplicate in three places: skip a repeated first element, and after recording a hit advance both pointers past their duplicates. Missing any of the three yields duplicate triples.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def three_sum(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError("implement three_sum")
