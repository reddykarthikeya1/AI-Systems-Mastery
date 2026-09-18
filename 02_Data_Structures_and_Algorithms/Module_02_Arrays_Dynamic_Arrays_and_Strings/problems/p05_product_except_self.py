"""Problem 05 — Product Of Array Except Self

Pattern:    Prefix/suffix products
Difficulty: Medium
Target:     Time O(n), Space O(1) beyond the output

Return an array ``out`` where ``out[i]`` is the product of every element of
``nums`` except ``nums[i]``.

You must not use division — the array may contain zeros, and dividing by one
would be undefined.

Constraints
- ``2 <= len(nums) <= 10**5``  -> O(n) required
- the product fits in a Python int

Example
    product_except_self([1, 2, 3, 4]) -> [24, 12, 8, 6]

Example:
    >>> product_except_self([1, 2, 3, 4])
    [24, 12, 8, 6]

Hints — read one at a time, and try again between each.

    Hint 1: out[i] is (product of everything left of i) * (product of everything right of i).
    Hint 2: Both of those can be built in one pass each.
    Hint 3: Do it in two sweeps over the output array itself: left-to-right filling in the prefix product, then right-to-left multiplying in the suffix. That needs no extra arrays beyond the output.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def product_except_self(nums: list[int]) -> list[int]:
    raise NotImplementedError("implement product_except_self")
