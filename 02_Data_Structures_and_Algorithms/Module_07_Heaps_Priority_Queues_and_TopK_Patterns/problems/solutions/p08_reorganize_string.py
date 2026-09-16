"""Reference solution — Problem 08: Reorganize String

Pattern:    Greedy with a max-heap
Complexity: Time O(n log 26), Space O(n)
"""

from __future__ import annotations


def reorganize_string(s: str) -> str:
    import heapq

    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1

    # Impossible exactly when one character cannot be spaced out.
    if max(counts.values()) > (len(s) + 1) // 2:
        return ""

    heap = [(-c, ch) for ch, c in counts.items()]
    heapq.heapify(heap)

    out: list[str] = []
    prev: tuple[int, str] | None = None     # held aside for exactly one step

    while heap:
        neg_count, ch = heapq.heappop(heap)
        out.append(ch)
        # Re-admit the previous character now that one slot separates them.
        if prev is not None:
            heapq.heappush(heap, prev)
            prev = None
        remaining = neg_count + 1           # negated, so += 1 decrements
        if remaining != 0:
            prev = (remaining, ch)

    return "".join(out)
