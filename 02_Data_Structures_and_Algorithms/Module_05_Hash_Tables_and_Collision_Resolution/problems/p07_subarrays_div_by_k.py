"""Problem 07 — Subarray Sums Divisible By K

Pattern:    Prefix sums + modular arithmetic
Difficulty: Medium
Target:     Time O(n), Space O(k)

Return the number of contiguous subarrays whose sum is divisible by ``k``.

Constraints
- ``1 <= len(nums) <= 3 * 10**4``  -> O(n) expected
- ``-10**4 <= nums[i] <= 10**4``, values may be negative
- ``2 <= k <= 10**4``

Example
    subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5) -> 7

Example:
    >>> subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5)
    7

Hints — read one at a time, and try again between each.

    Hint 1: sum(i..j) is divisible by k exactly when prefix[j+1] and prefix[i] leave the same remainder mod k.
    Hint 2: So count how many prefixes fall into each remainder class, then every pair within a class contributes one subarray.
    Hint 3: Python's % already returns a non-negative remainder for a positive k, which handles the negative values for you - in C or Java you would have to normalise with ((r % k) + k) % k. Seed the counter with remainder 0 seen once, for the empty prefix.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def subarrays_div_by_k(nums: list[int], k: int) -> int:
    raise NotImplementedError("implement subarrays_div_by_k")
