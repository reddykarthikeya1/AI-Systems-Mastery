#!/usr/bin/env python3
"""Stack and monotonic-structure utilities. Exits 0. Four wrong answers.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

from collections import deque

RULE = "=" * 68


def balanced_brackets(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return True


def next_greater(nums: list[int]) -> list[int]:
    out = [-1] * len(nums)
    stack: list[int] = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] <= x:
            out[stack.pop()] = x
        stack.append(i)
    return out


def daily_temperatures(temps: list[int]) -> list[int]:
    out = [0] * len(temps)
    stack: list[int] = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            out[j] = i
        stack.append(i)
    return out


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()
    out: list[int] = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def main() -> None:
    print(RULE)
    print("MONOTONIC TOOLKIT")
    print(RULE)

    print()
    print("[1] Bracket validation")
    for s, expected in (("()", True), ("()[]{}", True), ("{[()]}", True),
                        ("([)]", False), ("(", False), ("([]", False), (")", False)):
        print(f"      {s!r:<10} -> {balanced_brackets(s)!s:<6} (expected {expected})")

    print()
    print("[2] Next greater element")
    for nums in ([2, 1, 2, 4, 3], [1, 1, 2], [2, 2, 2], [1, 2, 3]):
        brute = [
            next((nums[j] for j in range(i + 1, len(nums)) if nums[j] > nums[i]), -1)
            for i in range(len(nums))
        ]
        print(f"      {nums} -> {next_greater(nums)}   (expected {brute})")

    print()
    print("[3] Daily temperatures (days to wait)")
    for temps in ([73, 74, 75, 71, 69, 72, 76, 73], [30, 40, 50, 60], [50, 50, 51]):
        brute = [
            next((j - i for j in range(i + 1, len(temps)) if temps[j] > temps[i]), 0)
            for i in range(len(temps))
        ]
        print(f"      {temps} -> {daily_temperatures(temps)}")
        print(f"          expected {brute}")

    print()
    print("[4] Sliding window maximum")
    for nums, k in (([1, 3, -1, -3, 5, 3, 6, 7], 3), ([5, 4, 3, 2, 1], 2),
                    ([1, 2, 3, 4, 5], 2)):
        brute = [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]
        print(f"      {nums} k={k}")
        print(f"          reported {sliding_window_max(nums, k)}")
        print(f"          expected {brute}")

    print()
    print(RULE)
    print("Toolkit check complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
