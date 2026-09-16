"""Reference solution — Problem 06: Row-Major Memory Layout

Pattern:    Memory layout
Complexity: Time O(1), Space O(1)
"""

from __future__ import annotations


def row_major_index(rows: int, cols: int, r: int, c: int) -> int:
    if not (0 <= r < rows) or not (0 <= c < cols):
        raise IndexError(f"({r}, {c}) is outside a {rows}x{cols} array")
    # Row-major: skip r complete rows, then walk c elements into this one.
    return r * cols + c
