"""Reference solution — Problem 07: Count-Min Sketch: Frequency Estimation

Pattern:    Count-Min sketch
Complexity: Time O((n + q) * depth), Space O(width * depth)
"""

from __future__ import annotations


def count_min_estimate(items: list[str], queries: list[str], width: int = 2048, depth: int = 4) -> list[int]:
    import hashlib

    if width < 1 or depth < 1:
        raise ValueError("width and depth must both be positive")

    table = [[0] * width for _ in range(depth)]

    def slots(item: str) -> list[int]:
        return [
            int.from_bytes(
                hashlib.sha256(f"{row}:{item}".encode()).digest()[:8], "big"
            ) % width
            for row in range(depth)
        ]

    for item in items:
        for row, col in enumerate(slots(item)):
            table[row][col] += 1

    # The MINIMUM across rows: a collision can only inflate a counter, so the
    # smallest row is closest to the truth and never below it.
    return [min(table[row][col] for row, col in enumerate(slots(q))) for q in queries]
