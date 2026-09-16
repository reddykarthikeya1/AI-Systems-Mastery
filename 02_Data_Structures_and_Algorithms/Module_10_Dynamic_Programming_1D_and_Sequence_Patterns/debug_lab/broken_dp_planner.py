#!/usr/bin/env python3
"""1D dynamic programming planner. Exits 0, four wrong plans.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import math

RULE = "=" * 68


def coin_change_min(coins: list[int], amount: int) -> int:
    best = [0] * (amount + 1)
    for a in range(1, amount + 1):
        options = [best[a - c] + 1 for c in coins if c <= a]
        best[a] = min(options) if options else 0
    return best[amount]


def house_robber(nums: list[int]) -> int:
    skip, take = 0, 0
    for x in nums:
        skip, take = take, skip + x
    return max(skip, take)


def lis(nums: list[int]) -> int:
    if not nums:
        return 0
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] <= nums[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)


def max_product_subarray(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur * x)
        best = max(best, cur)
    return best


def main() -> None:
    print(RULE)
    print("1D DP PLANNER")
    print(RULE)

    print()
    print("[1] Fewest coins to make an amount")
    cases = [([1, 2, 5], 11, 3), ([2], 3, "impossible"), ([1, 3, 4], 6, 2),
             ([7, 11], 5, "impossible"), ([5], 0, 0)]
    for coins, amount, expected in cases:
        print(f"      coins={coins} amount={amount:<3} -> {coin_change_min(coins, amount)} "
              f"(expected {expected})")

    print()
    print("[2] Maximum non-adjacent sum")
    for nums, expected in (([1, 2, 3, 1], 4), ([2, 7, 9, 3, 1], 12), ([5], 5),
                           ([2, 1, 1, 2], 4)):
        print(f"      {nums} -> {house_robber(nums)} (expected {expected})")

    print()
    print("[3] Longest strictly increasing subsequence")
    for nums, expected in (([10, 9, 2, 5, 3, 7, 101, 18], 4), ([7, 7, 7, 7], 1),
                           ([1, 2, 2, 3], 3), ([2, 2], 1)):
        print(f"      {nums} -> {lis(nums)} (expected {expected})")

    print()
    print("[4] Maximum product subarray")
    for nums in ([2, 3, -2, 4], [-2, 3, -4], [-1, -2, -3, -4], [-2, 0, -1]):
        brute = max(
            math.prod(nums[i : j + 1])
            for i in range(len(nums))
            for j in range(i, len(nums))
        )
        print(f"      {nums} -> {max_product_subarray(nums)} (expected {brute})")

    print()
    print(RULE)
    print("Planning complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
