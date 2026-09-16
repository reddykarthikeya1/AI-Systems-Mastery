"""Reference solution — Problem 02: Merge K Sorted Lists

Pattern:    Min-heap k-way merge
Complexity: Time O(N log k), Space O(k)
"""

from __future__ import annotations


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    import heapq

    # (value, list_index, element_index). The list index breaks ties so the
    # tuple comparison never has to compare two lists.
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

    return out
