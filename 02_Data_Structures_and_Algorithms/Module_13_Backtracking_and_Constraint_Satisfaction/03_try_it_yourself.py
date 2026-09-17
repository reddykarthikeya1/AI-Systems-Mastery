"""Beginner playground for Module 13 - Backtracking & Constraint Satisfaction.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import copy

# -------------------------------------------- 1. Subsets Generation via Include / Exclude Decisions
def subsets(nums):
    res = []
    def backtrack(idx, path):
        if idx == len(nums):
            res.append(path[:])
            return
        # Choice 1: Exclude
        backtrack(idx + 1, path)
        # Choice 2: Include
        path.append(nums[idx])
        backtrack(idx + 1, path)
        path.pop()  # Backtrack undo
    backtrack(0, [])
    return res

all_subsets = subsets([1, 2, 3])
assert len(all_subsets) == 8, "2^3 = 8 subsets"
assert [] in all_subsets and [1, 2, 3] in all_subsets
print(f"Generated {len(all_subsets)} subsets of [1, 2, 3]")

# -------------------------------------------- 2. Permutations via Swapping and Backtracking
def permutations(nums):
    res = []
    def backtrack(start):
        if start == len(nums):
            res.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # Backtrack
    backtrack(0)
    return res

perms = permutations([1, 2, 3])
assert len(perms) == 6, "3! = 6 permutations"
assert [1, 2, 3] in perms and [3, 2, 1] in perms
print(f"Generated {len(perms)} permutations of [1, 2, 3]")

# -------------------------------------------- 3. N-Queens Valid Placement Pruning
def solve_n_queens(n):
    cols, diag1, diag2 = set(), set(), set()
    solutions = 0
    def backtrack(r):
        nonlocal solutions
        if r == n:
            solutions += 1
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            backtrack(r + 1)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
    backtrack(0)
    return solutions

assert solve_n_queens(4) == 2, "4-Queens has exactly 2 valid boards"
assert solve_n_queens(1) == 1
print(f"4-Queens has {solve_n_queens(4)} valid solutions.")

print()
print("All checks passed.")
