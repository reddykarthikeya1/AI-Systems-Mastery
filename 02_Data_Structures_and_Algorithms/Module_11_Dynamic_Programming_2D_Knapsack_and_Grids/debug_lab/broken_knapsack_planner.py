#!/usr/bin/env python3
"""2D DP allocation planner. Exits 0, and over-promises capacity.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import itertools

RULE = "=" * 68


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    best = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(w, capacity + 1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    target = total // 2
    achievable = [False] * (target + 1)
    achievable[0] = True
    for x in nums:
        for s in range(x, target + 1):
            if achievable[s - x]:
                achievable[s] = True
    return achievable[target]


def min_path_sum(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    best = list(grid[0])
    for r in range(1, rows):
        for c in range(cols):
            if c == 0:
                best[c] += grid[r][c]
            else:
                best[c] = grid[r][c] + min(best[c], best[c - 1])
    return best[-1]


def lcs(a: str, b: str) -> int:
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], prev[j - 1])
        prev = cur
    return prev[m]


def main() -> None:
    print(RULE)
    print("RESOURCE ALLOCATION PLANNER")
    print(RULE)

    print()
    print("[1] 0/1 knapsack (each item available ONCE)")
    cases = [([1, 3, 4, 5], [1, 4, 5, 7], 7), ([1], [10], 3), ([2, 3], [10, 12], 6),
             ([2, 2, 3], [3, 4, 5], 5)]
    for ws, vs, cap in cases:
        brute = 0
        for r in range(len(ws) + 1):
            for combo in itertools.combinations(range(len(ws)), r):
                if sum(ws[i] for i in combo) <= cap:
                    brute = max(brute, sum(vs[i] for i in combo))
        print(f"      weights={ws} values={vs} cap={cap} -> {knapsack_01(ws, vs, cap)} "
              f"(expected {brute})")

    print()
    print("[2] Equal-sum partition")
    for nums in ([1, 5, 11, 5], [1, 2, 3, 5], [1, 1], [1, 3], [2, 2, 1, 1]):
        total = sum(nums)
        brute = total % 2 == 0 and any(
            sum(c) == total // 2
            for r in range(len(nums) + 1)
            for c in itertools.combinations(nums, r)
        )
        print(f"      {nums} -> {can_partition(nums)} (expected {brute})")

    print()
    print("[3] Minimum grid path sum")
    for grid, expected in (([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
                           ([[1, 2, 3], [4, 5, 6]], 12),
                           ([[1, 2], [1, 1]], 3)):
        print(f"      {grid} -> {min_path_sum(grid)} (expected {expected})")

    print()
    print("[4] Longest common subsequence")
    for a, b, expected in (("abcde", "ace", 3), ("abc", "abc", 3), ("abcd", "dcba", 1),
                           ("abcdefg", "aceg", 4), ("aa", "aaa", 2)):
        print(f"      {a!r} vs {b!r} -> {lcs(a, b)} (expected {expected})")

    print()
    print(RULE)
    print("Allocation complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
