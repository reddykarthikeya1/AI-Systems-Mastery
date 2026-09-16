#!/usr/bin/env python3
"""Configuration enumerator. Exits 0, and returns the same answer many times.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import math

RULE = "=" * 68


def subsets(nums):
    out = []
    path = []

    def backtrack(start):
        out.append(path)
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return out


def permutations(nums):
    ordered = sorted(nums)
    n = len(ordered)
    used = [False] * n
    out = []
    path = []

    def backtrack():
        if len(path) == n:
            out.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(ordered[i])
            backtrack()
            path.pop()

    backtrack()
    return out


def combination_sum(candidates, target):
    ordered = sorted(candidates)
    out = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            out.append(path[:])
            return
        for i in range(start, len(ordered)):
            if ordered[i] > remaining:
                break
            path.append(ordered[i])
            backtrack(i + 1, remaining - ordered[i])
            path.pop()

    backtrack(0, target)
    return sorted(out)


def n_queens(n):
    cols, diag = set(), set()
    count = 0

    def place(row):
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or (row - col) in diag:
                continue
            cols.add(col)
            diag.add(row - col)
            place(row + 1)
            cols.remove(col)
            diag.remove(row - col)

    place(0)
    return count


def main() -> None:
    print(RULE)
    print("CONFIGURATION ENUMERATOR")
    print(RULE)

    print()
    print("[1] All subsets")
    for nums in ([1, 2], [1, 2, 3]):
        got = subsets(nums)
        distinct = len({tuple(x) for x in got})
        print(f"      {nums} -> {got}")
        print(f"          produced {len(got)} subsets, {distinct} distinct "
              f"(expected {2 ** len(nums)} of each)")

    print()
    print("[2] All permutations")
    for nums in ([1, 2], [1, 2, 3]):
        got = permutations(nums)
        print(f"      {nums} -> produced {len(got)}, expected {math.factorial(len(nums))}")
        print(f"          {got}")

    print()
    print("[3] Combination sum (candidates may be REUSED)")
    cases = [([2, 3, 6, 7], 7, [[2, 2, 3], [7]]),
             ([2], 6, [[2, 2, 2]]),
             ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]])]
    for candidates, target, expected in cases:
        print(f"      {candidates} target={target}")
        print(f"          reported {combination_sum(candidates, target)}")
        print(f"          expected {expected}")

    print()
    print("[4] N-Queens solution counts")
    known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    for n in range(1, 9):
        print(f"      n={n} -> {n_queens(n):<5} (known {known[n]})")

    print()
    print(RULE)
    print("Enumeration complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
