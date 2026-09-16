"""Problem 07 — Maximum Product Subarray

Pattern:    1D DP with two-value state
Difficulty: Medium
Target:     Time O(n), Space O(1)

Return the largest product of any contiguous subarray.

Constraints
- ``1 <= len(nums) <= 2 * 10**4``
- values may be negative or zero

Example
    max_product_subarray([2, 3, -2, 4])  -> 6
    max_product_subarray([-2, 0, -1])    -> 0
    max_product_subarray([-2, 3, -4])    -> 24

This is the module's most instructive problem. Tracking only the running
*maximum* is not enough: a large **negative** product becomes the maximum the
moment it meets another negative. The state has to be two values.

Hints — read one at a time, and try again between each.

    Hint 1: The single-variable state that works for maximum SUM does not work for maximum PRODUCT. Ask what a negative number does to your running best.
    Hint 2: It flips it. So the smallest (most negative) product so far is a candidate for the largest, once multiplied by another negative.
    Hint 3: Track both the running max and the running min, and recompute both from the previous pair at each step. A zero resets both.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def max_product_subarray(nums: list[int]) -> int:
    raise NotImplementedError("implement max_product_subarray")
