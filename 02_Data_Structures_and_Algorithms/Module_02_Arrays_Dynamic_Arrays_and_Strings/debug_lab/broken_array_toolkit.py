#!/usr/bin/env python3
"""An array toolkit. Exits 0, and four of its five answers are wrong.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

RULE = "=" * 68


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        seen[x] = i
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
    return []


def max_window_sum(nums: list[int], k: int) -> int:
    best = 0
    total = sum(nums[:k])
    best = max(best, total)
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]
        best = max(best, total)
    return best


def subarray_sum_k(nums: list[int], k: int) -> int:
    counts: dict[int, int] = {}
    running = 0
    total = 0
    for x in nums:
        running += x
        total += counts.get(running - k, 0)
        counts[running] = counts.get(running, 0) + 1
    return total


def longest_k_distinct(s: str, k: int) -> int:
    if k <= 0 or not s:
        return 0
    counts: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) >= k:
            leaving = s[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1
        best = max(best, right - left + 1)
    return best


def min_ship_capacity(weights: list[int], days: int) -> int:
    def days_needed(capacity: int) -> int:
        used = 1
        load = 0
        for w in weights:
            if load + w > capacity:
                used += 1
                load = 0
            load += w
        return used

    lo, hi = 1, sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


def main() -> None:
    print(RULE)
    print("ARRAY TOOLKIT REPORT")
    print(RULE)

    print()
    print("[1] Two-sum index lookup")
    cases = [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([5, 1, 10], 10), ([3, 3], 6)]
    for nums, target in cases:
        result = two_sum(nums, target)
        if result:
            i, j = result
            check = nums[i] + nums[j]
            print(f"      {nums} target={target:<3} -> indices {result} "
                  f"values {nums[i]}+{nums[j]}={check} distinct={i != j}")
        else:
            print(f"      {nums} target={target:<3} -> no pair found")

    print()
    print("[2] Maximum sum of a fixed window")
    for nums, k in (([2, 1, 5, 1, 3, 2], 3), ([-4, -2, -7, -3], 2), ([-1, -1], 1)):
        print(f"      {nums} k={k} -> {max_window_sum(nums, k)}")

    print()
    print("[3] Count of subarrays summing to k")
    for nums, k in (([1, 1, 1], 2), ([1, 2, 3], 3), ([1, 2, 3], 1), ([3], 3)):
        brute = sum(
            1
            for i in range(len(nums))
            for j in range(i, len(nums))
            if sum(nums[i : j + 1]) == k
        )
        print(f"      {nums} k={k} -> reported {subarray_sum_k(nums, k)}, "
              f"brute force {brute}")

    print()
    print("[4] Longest substring with at most k distinct characters")
    for s, k in (("eceba", 2), ("aa", 1), ("abcadcacacaca", 3), ("abaccc", 2)):
        brute = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                if len(set(s[i : j + 1])) <= k:
                    brute = max(brute, j - i + 1)
        print(f"      {s!r:<16} k={k} -> reported {longest_k_distinct(s, k)}, "
              f"brute force {brute}")

    print()
    print("[5] Minimum ship capacity")
    for weights, days in (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), ([3, 2, 2, 4, 1, 4], 3),
                          ([1, 1, 9], 3), ([2, 2, 10], 3)):
        cap = min_ship_capacity(weights, days)
        def days_for(c: int, ws: list[int] = weights) -> int:
            used, load = 1, 0
            for w in ws:
                if load + w > c:
                    used += 1
                    load = 0
                load += w
            return used
        print(f"      {weights} days={days} -> capacity {cap} "
              f"(needs {days_for(cap)} days; heaviest package is {max(weights)})")

    print()
    print(RULE)
    print("Report complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
