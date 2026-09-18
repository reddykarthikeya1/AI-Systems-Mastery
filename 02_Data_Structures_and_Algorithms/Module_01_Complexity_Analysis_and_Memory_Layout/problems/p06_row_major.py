"""Problem 06 — Row-Major Memory Layout

Pattern:    Memory layout
Difficulty: Easy
Target:     Time O(1), Space O(1)

A 2D array of shape ``(rows, cols)`` is stored in one flat contiguous buffer in
**row-major** order: all of row 0, then all of row 1, and so on.

Return the flat buffer offset of element ``(r, c)``. Raise ``IndexError`` for
out-of-range coordinates.

Constraints
- ``1 <= rows, cols <= 10**5``
- negative indices are **not** supported here; they must raise

Example
    row_major_index(3, 4, 1, 2) -> 6

Why this matters: iterating a row-major array along rows walks consecutive
addresses and every cache line you fetch is fully used. Iterating along columns
strides by ``cols`` elements and can waste most of each cache line. Same
asymptotic complexity, and often an order of magnitude difference in wall time.

Example:
    >>> row_major_index(3, 4, 1, 2)
    6

Hints — read one at a time, and try again between each.

    Hint 1: Row r starts at offset r * cols.
    Hint 2: Then add c to move along the row.
    Hint 3: Validate 0 <= r < rows and 0 <= c < cols BEFORE computing, so a bad index raises instead of returning a plausible offset.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def row_major_index(rows: int, cols: int, r: int, c: int) -> int:
    raise NotImplementedError("implement row_major_index")
