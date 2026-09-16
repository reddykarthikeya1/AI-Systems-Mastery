"""Reference solution — Problem 01: K-th Largest Element

Pattern:    Min-heap of size k
Complexity: Time O(n log k), Space O(k)
"""

from __future__ import annotations


def kth_largest(nums: list[int], k: int) -> int:
    import heapq

    n = len(nums)
    if not 1 <= k <= n:
        raise ValueError(f"k={k} is out of range for {n} elements")

    # A MIN-heap of size k: the root is the weakest of the current best k, so
    # it is exactly what to evict. A max-heap would give the wrong element.
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
