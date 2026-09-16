"""Module 02 Demo: Two Pointers and Sliding Window Production Demos."""
from __future__ import annotations

import time
from collections import Counter


def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """LeetCode 167: Two Sum II - Input Array Is Sorted (O(N) Time, O(1) Space)."""
    left, right = 0, len(numbers) - 1
    while left < right:
        curr = numbers[left] + numbers[right]
        if curr == target:
            return [left + 1, right + 1]
        elif curr < target:
            left += 1
        else:
            right -= 1
    return []


def three_sum(nums: list[int]) -> list[list[int]]:
    """LeetCode 15: 3Sum (O(N^2) Time, O(1) Auxiliary Space)."""
    nums.sort()
    res: list[list[int]] = []
    n = len(nums)
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
    return res


def max_area(height: list[int]) -> int:
    """LeetCode 11: Container With Most Water (O(N) Time, O(1) Space)."""
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water


def trap_rain_water(height: list[int]) -> int:
    """LeetCode 42: Trapping Rain Water (O(N) Time, O(1) Space)."""
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water


def length_of_longest_substring(s: str) -> int:
    """LeetCode 3: Longest Substring Without Repeating Characters (O(N) Time, O(Sigma) Space)."""
    last_seen: dict[str, int] = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len


def min_window_substring(s: str, t: str) -> str:
    """LeetCode 76: Minimum Window Substring (O(|S| + |T|) Time, O(|S| + |T|) Space)."""
    if not t or not s:
        return ""
    target_counts = Counter(t)
    window_counts: dict[str, int] = {}
    have, need = 0, len(target_counts)
    res_len = float("inf")
    res_indices = (-1, -1)
    left = 0
    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            have += 1
        while have == need:
            if right - left + 1 < res_len:
                res_len = right - left + 1
                res_indices = (left, right)
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                have -= 1
            left += 1
    start_idx, end_idx = res_indices
    return s[start_idx : end_idx + 1] if res_len != float("inf") else ""


def run_demos():
    print("Executing Two Pointers & Sliding Window Production Benchmarks...")
    t0 = time.perf_counter()

    # 1. Two Sum II
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    # 2. 3Sum
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    # 3. Container With Most Water
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    # 4. Trapping Rain Water
    assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    # 5. Longest Substring Without Repeating Characters
    assert length_of_longest_substring("abcabcbb") == 3
    # 6. Minimum Window Substring
    assert min_window_substring("ADOBECODEBANC", "ABC") == "BANC"

    elapsed = (time.perf_counter() - t0) * 1000
    print(f"All Two Pointers & Sliding Window tests passed successfully in {elapsed:.3f} ms!")


if __name__ == "__main__":
    run_demos()
