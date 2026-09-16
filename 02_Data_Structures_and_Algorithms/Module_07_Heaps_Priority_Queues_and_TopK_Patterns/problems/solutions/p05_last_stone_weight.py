"""Reference solution — Problem 05: Last Stone Weight

Pattern:    Max-heap simulation
Complexity: Time O(n log n), Space O(n)
"""

from __future__ import annotations


def last_stone_weight(stones: list[int]) -> int:
    import heapq

    heap = [-w for w in stones]      # negate for max-heap behaviour
    heapq.heapify(heap)

    while len(heap) > 1:
        heaviest = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if heaviest != second:
            # Only push a real stone back; a 0 would be a phantom.
            heapq.heappush(heap, -(heaviest - second))

    return -heap[0] if heap else 0
