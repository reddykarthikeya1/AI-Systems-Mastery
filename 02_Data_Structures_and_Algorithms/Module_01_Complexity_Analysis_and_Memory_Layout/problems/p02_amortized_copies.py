"""Problem 02 — Total Copies Under Geometric Growth

Pattern:    Amortized analysis
Difficulty: Medium
Target:     Time O(log n), Space O(1)

A dynamic array starts with ``initial_capacity`` slots. When it is full and
another element is appended, it allocates a buffer of **double** the capacity
and copies every existing element across.

Return the total number of element copies performed while appending ``n``
elements one at a time.

Constraints
- ``0 <= n <= 10**9`` — you cannot simulate element by element at the top end
- ``initial_capacity >= 1``

This is the measurement behind the claim that append is amortised O(1): the
total is O(n), so the per-append average is constant even though individual
appends cost O(n).

Example:
    >>> total_copies_for_appends(5, 1)
    7

(capacities 1,2,4,8; copies 1+2+4 = 7)

Hints — read one at a time, and try again between each.

    Hint 1: You never copy on an append that fits. Copies happen only at a resize.
    Hint 2: The copies at each resize are the capacity *before* doubling: initial, 2*initial, 4*initial, ...
    Hint 3: So the answer is a geometric series. Loop over resizes (there are only ~log2(n) of them), not over elements.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def total_copies_for_appends(n: int, initial_capacity: int = 1) -> int:
    raise NotImplementedError("implement total_copies_for_appends")
