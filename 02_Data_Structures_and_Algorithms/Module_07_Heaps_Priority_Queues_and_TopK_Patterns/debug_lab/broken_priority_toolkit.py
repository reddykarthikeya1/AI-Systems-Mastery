#!/usr/bin/env python3
"""Heap-based ranking and scheduling. Exits 0, four wrong answers.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import heapq
import statistics

RULE = "=" * 68


def kth_largest(nums: list[int], k: int) -> int:
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
    return -heap[0]


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    heap: list[tuple[int, int, int]] = []
    for li, lst in enumerate(lists):
        if lst:
            heap.append((lst[0], li, 0))
    heapq.heapify(heap)
    out: list[int] = []
    while heap:
        value, li, ei = heapq.heappop(heap)
        out.append(value)
        nxt = ei + 1
        if nxt < len(lists[li]):
            heapq.heappush(heap, (lists[li][nxt], li, nxt))
        else:
            break
    return out


def streaming_median(nums: list[int]) -> list[float]:
    lower: list[int] = []
    upper: list[int] = []
    out: list[float] = []
    for x in nums:
        heapq.heappush(lower, -x)
        heapq.heappush(upper, -heapq.heappop(lower))
        if len(upper) > len(lower):
            heapq.heappush(lower, -heapq.heappop(upper))
        if len(lower) >= len(upper):
            out.append(float(-lower[0]))
        else:
            out.append((-lower[0] + upper[0]) / 2.0)
    return out


def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0
    ends: list[int] = []
    for start, end in intervals:
        if ends and ends[0] <= start:
            heapq.heappop(ends)
        heapq.heappush(ends, end)
    return len(ends)


def main() -> None:
    print(RULE)
    print("PRIORITY TOOLKIT")
    print(RULE)

    print()
    print("[1] K-th largest element")
    for nums, k in (([3, 2, 1, 5, 6, 4], 2), ([7, 3, 9, 1], 1), ([7, 3, 9, 1], 4),
                    ([5, 5, 5], 2)):
        expected = sorted(nums, reverse=True)[k - 1]
        print(f"      {nums} k={k} -> {kth_largest(nums, k)} (expected {expected})")

    print()
    print("[2] Merge k sorted lists")
    for lists in ([[1, 4, 5], [1, 3, 4], [2, 6]], [[1, 2], [3, 4], [5, 6]],
                  [[1], [2], [3]]):
        expected = sorted(x for lst in lists for x in lst)
        got = merge_k_sorted(lists)
        print(f"      {lists}")
        print(f"          reported {got}")
        print(f"          expected {expected}")

    print()
    print("[3] Streaming median")
    for nums in ([2, 3, 4], [5, 4, 3, 2, 1], [1, 2]):
        expected = [float(statistics.median(nums[: i + 1])) for i in range(len(nums))]
        print(f"      {nums}")
        print(f"          reported {streaming_median(nums)}")
        print(f"          expected {expected}")

    print()
    print("[4] Minimum meeting rooms")
    for intervals in ([(0, 30), (5, 10), (15, 20)], [(15, 20), (0, 30), (5, 10)],
                      [(1, 10), (2, 9), (3, 8)], [(1, 2), (2, 3), (3, 4)]):
        points = sorted({t for iv in intervals for t in iv})
        expected = max(sum(1 for s, e in intervals if s <= t < e) for t in points)
        print(f"      {intervals} -> {min_meeting_rooms(intervals)} "
              f"(expected {expected})")

    print()
    print(RULE)
    print("Toolkit check complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
