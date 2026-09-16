"""Reference solution — Problem 04: K Closest Points To The Origin

Pattern:    Max-heap of size k
Complexity: Time O(n log k), Space O(k)
"""

from __future__ import annotations


def k_closest_points(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    import heapq

    n = len(points)
    if not 1 <= k <= n:
        raise ValueError(f"k={k} is out of range for {n} points")

    # Squared distance: same ordering, integer arithmetic, no sqrt.
    # A MAX-heap of size k (negated) so the worst of the current best k is at
    # the root and can be evicted in O(log k).
    heap: list[tuple[int, int, int]] = []
    for x, y in points:
        d = x * x + y * y
        heapq.heappush(heap, (-d, -x, -y))
        if len(heap) > k:
            heapq.heappop(heap)

    survivors = [(-nx, -ny) for _, nx, ny in heap]
    survivors.sort(key=lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1]))
    return survivors
