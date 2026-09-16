"""Problem 02 — Top K Frequent Elements

Pattern:    Counting + bucket sort
Difficulty: Medium
Target:     Time O(n), Space O(n)

Return the ``k`` most frequent elements, ordered by descending frequency. Break
ties by ascending value so the output is deterministic.

Raise ``ValueError`` if ``k`` exceeds the number of distinct elements.

Constraints
- ``1 <= len(nums) <= 10**5``
- ``1 <= k <= number of distinct elements``

Example
    top_k_frequent([1, 1, 1, 2, 2, 3], 2) -> [1, 2]

Hints — read one at a time, and try again between each.

    Hint 1: Count frequencies first - that part is unavoidable and O(n).
    Hint 2: A heap of size k gives O(n log k). But note that no frequency can exceed len(nums).
    Hint 3: So you can bucket by frequency: bucket[f] holds every value seen f times. Walk the buckets from high to low and you get O(n) overall.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError("implement top_k_frequent")
