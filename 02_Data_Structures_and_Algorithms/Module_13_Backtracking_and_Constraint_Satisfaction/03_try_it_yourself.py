"""Module 13: Interactive Backtracking CLI Sandbox."""
from __future__ import annotations


def demo():
    print("\n=== DEMO: Generating All Subsets ===")
    nums = [1, 2, 3]
    res = []
    subset = []
    def dfs(i):
        if i >= len(nums):
            res.append(subset.copy())
            return
        subset.append(nums[i])
        dfs(i + 1)
        subset.pop()
        dfs(i + 1)
    dfs(0)
    print(f"All 2^3={len(res)} subsets of {nums}:", res)


if __name__ == "__main__":
    demo()
