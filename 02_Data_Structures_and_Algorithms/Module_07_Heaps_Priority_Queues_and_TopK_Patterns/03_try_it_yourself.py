"""Module 07: Interactive Heaps CLI Sandbox."""
from __future__ import annotations

import heapq


def demo():
    print("\n=== DEMO: Min-Heap Priority Queue ===")
    nums = [15, 3, 22, 1, 9, 30]
    print("Original numbers:", nums)
    heapq.heapify(nums)
    print("Heapified array representation:", nums)
    print("Popping elements in priority order:")
    while nums:
        print("  Popped:", heapq.heappop(nums))


if __name__ == "__main__":
    demo()
