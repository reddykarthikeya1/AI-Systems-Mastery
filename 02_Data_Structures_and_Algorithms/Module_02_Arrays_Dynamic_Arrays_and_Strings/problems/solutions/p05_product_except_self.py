"""Reference solution — Problem 05: Product Of Array Except Self

Pattern:    Prefix/suffix products
Complexity: Time O(n), Space O(1) beyond the output
"""

from __future__ import annotations


def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    out = [1] * n

    # Pass 1: out[i] = product of everything strictly left of i.
    prefix = 1
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]

    # Pass 2: multiply in the product of everything strictly right of i.
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]

    return out
