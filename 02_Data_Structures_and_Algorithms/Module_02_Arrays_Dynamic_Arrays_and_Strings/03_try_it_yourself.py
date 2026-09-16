"""Module 02: Interactive Foundations Interactive CLI Sandbox.

Run this script directly in your terminal to see algorithms visualised live:
    python 03_try_it_yourself.py
"""
from __future__ import annotations


def demo_two_pointers():
    print("\n" + "=" * 60)
    print("DEMO 1: Two Pointers Walking Towards Each Other")
    print("Target Sum = 10 in sorted array: [1, 2, 4, 6, 8, 9]")
    print("=" * 60)

    nums = [1, 2, 4, 6, 8, 9]
    target = 10
    left, right = 0, len(nums) - 1
    step = 1

    while left < right:
        curr = nums[left] + nums[right]
        # Visual representation
        display = []
        for i, val in enumerate(nums):
            if i == left and i == right:
                display.append(f"[{val}]*LR*")
            elif i == left:
                display.append(f"[{val}]*L*")
            elif i == right:
                display.append(f"[{val}]*R*")
            else:
                display.append(f" {val}  ")
        print(f"\nStep {step}:")
        print("  Array:  " + " ".join(display))
        print(f"  Left={nums[left]} (idx {left}), "
              f"Right={nums[right]} (idx {right}) -> Sum = {curr}")

        if curr == target:
            print(f"  --> MATCH FOUND! {nums[left]} + {nums[right]} = {target}")
            return
        elif curr < target:
            print(f"  --> Sum {curr} < {target}. Left pointer advances RIGHT.")
            left += 1
        else:
            print(f"  --> Sum {curr} > {target}. Right pointer advances LEFT.")
            right -= 1
        step += 1


def demo_sliding_window():
    print("\n" + "=" * 60)
    print("DEMO 2: Sliding Window of Size K=3")
    print("Array: [2, 1, 5, 1, 3, 2]")
    print("=" * 60)

    nums = [2, 1, 5, 1, 3, 2]
    k = 3
    window_sum = sum(nums[:k])
    max_sum = window_sum

    print(f"\nInitial Window [0..{k-1}]: {nums[:k]} -> Sum = {window_sum}")

    for i in range(k, len(nums)):
        leaving = nums[i - k]
        entering = nums[i]
        window_sum = window_sum - leaving + entering
        max_sum = max(max_sum, window_sum)

        # Visual string
        win_str = []
        for idx, val in enumerate(nums):
            if i - k + 1 <= idx <= i:
                win_str.append(f"|{val}|")
            else:
                win_str.append(f" {val} ")
        window = " ".join(win_str)
        print(f"Slide -> Drop {leaving}, Add {entering} | "
              f"Window {window} | Sum = {window_sum}")

    print(f"\nMaximum Window Sum Found: {max_sum}")


def demo_prefix_sum():
    print("\n" + "=" * 60)
    print("DEMO 3: Piggy Bank (Prefix Sum) Instant Range Queries")
    print("Daily Deposits: [2, 3, 1, 4, 5]")
    print("=" * 60)

    nums = [2, 3, 1, 4, 5]
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x

    print(f"Prefix Sums Array: {prefix}")
    print("Query: Total money deposited between Day 2 (idx 1, value 3) and Day 4 (idx 3, value 4):")
    total = prefix[4] - prefix[1]
    print(f"Calculation: prefix[4] - prefix[1] = {prefix[4]} - {prefix[1]} = {total}")


def main():
    print("\n=== Welcome to the Interactive Foundations DSA Interactive Sandbox! ===")
    demo_two_pointers()
    demo_sliding_window()
    demo_prefix_sum()
    print("\n=== All interactive simulations completed successfully! ===")


if __name__ == "__main__":
    main()
