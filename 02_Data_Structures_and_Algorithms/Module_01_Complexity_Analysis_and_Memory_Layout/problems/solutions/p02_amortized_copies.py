"""Reference solution — Problem 02: Total Copies Under Geometric Growth

Pattern:    Amortized analysis
Complexity: Time O(log n), Space O(1)
"""

from __future__ import annotations


def total_copies_for_appends(n: int, initial_capacity: int = 1) -> int:
    if n <= 0:
        return 0

    copies = 0
    capacity = initial_capacity
    size = 0

    # Only ~log2(n) iterations, so n can be a billion without this being slow.
    while size < n:
        if size == capacity:
            copies += capacity      # every existing element moves
            capacity *= 2
        # Fill the rest of this capacity in one step rather than one at a time.
        take = min(capacity - size, n - size)
        size += take

    return copies
