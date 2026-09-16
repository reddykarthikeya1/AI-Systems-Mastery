"""Problem 04 — Largest Rectangle In A Histogram

Pattern:    Monotonic stack
Difficulty: Hard
Target:     Time O(n), Space O(n)

Bars of width 1 with the given heights stand side by side. Return the area of
the largest axis-aligned rectangle that fits inside the histogram.

Constraints
- ``0 <= len(heights) <= 10**5``  -> O(n) required
- ``0 <= heights[i] <= 10**4``

Example
    [2, 1, 5, 6, 2, 3] -> 10     (heights 5 and 6, width 2)

Hints — read one at a time, and try again between each.

    Hint 1: For each bar, the largest rectangle *with that bar as its shortest* extends left and right until it meets a strictly shorter bar.
    Hint 2: Those two boundaries are exactly 'previous smaller' and 'next smaller' - a monotonic stack of increasing heights.
    Hint 3: When a bar shorter than the stack top arrives, pop and settle: the popped bar's width runs from the new stack top (exclusive) to the current index (exclusive). Appending a sentinel 0 at the end flushes the stack without duplicating the settle logic.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def largest_rectangle(heights: list[int]) -> int:
    raise NotImplementedError("implement largest_rectangle")
