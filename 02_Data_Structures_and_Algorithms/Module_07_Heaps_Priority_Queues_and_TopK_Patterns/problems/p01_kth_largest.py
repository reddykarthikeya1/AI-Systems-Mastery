"""Problem 01 — K-th Largest Element

Pattern:    Min-heap of size k
Difficulty: Medium
Target:     Time O(n log k), Space O(k)

Return the ``k``-th largest element (1-indexed, counting duplicates as distinct
positions). Raise ``ValueError`` if ``k`` is out of range.

Constraints
- ``1 <= k <= len(nums) <= 10**5``
- target O(n log k), better than sorting

Example:
    >>> kth_largest([3, 2, 1, 5, 6, 4], 2)
    5
    >>> kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)
    4

Hints — read one at a time, and try again between each.

    Hint 1: Sorting gives O(n log n) and the answer at index -k. Fine, but not the target.
    Hint 2: Keep only the k largest seen so far. Which heap lets you find and evict the WEAKEST member of that set in O(log k)?
    Hint 3: A min-heap of size k. Push each element; when the heap exceeds k, pop the smallest. At the end the root is the k-th largest.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def kth_largest(nums: list[int], k: int) -> int:
    raise NotImplementedError("implement kth_largest")
