"""Module 02 Demo: Prefix Sum & Kadane's Algorithm Production Demos."""
from __future__ import annotations

import time


def max_sub_array(nums: list[int]) -> int:
    """LeetCode 53: Maximum Subarray via Kadane's Algorithm (O(N) Time, O(1) Space)."""
    current_sum = nums[0]
    max_sum = nums[0]
    for x in nums[1:]:
        current_sum = max(x, current_sum + x)
        max_sum = max(max_sum, current_sum)
    return max_sum


def product_except_self(nums: list[int]) -> list[int]:
    """LeetCode 238: Product of Array Except Self (O(N) Time, O(1) Auxiliary Space)."""
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """LeetCode 560: Subarray Sum Equals K (O(N) Time, O(N) Space)."""
    prefix_counts = {0: 1}
    current_sum = 0
    total_count = 0
    for num in nums:
        current_sum += num
        total_count += prefix_counts.get(current_sum - k, 0)
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
    return total_count


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """LeetCode 56: Merge Intervals (O(N log N) Time, O(N) Space)."""
    intervals.sort(key=lambda x: x[0])
    merged: list[list[int]] = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged


def rotate_matrix(matrix: list[list[int]]) -> None:
    """LeetCode 48: Rotate Image Clockwise by 90 Degrees In-Place (O(N^2) Time, O(1) Space)."""
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse rows
    for i in range(n):
        matrix[i].reverse()


def run_demos():
    print("Executing Prefix Sum, Kadane & In-Place Matrix Benchmarks...")
    t0 = time.perf_counter()

    # 1. Maximum Subarray
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    # 2. Product Except Self
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    # 3. Subarray Sum Equals K
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2
    assert subarray_sum_equals_k([1, -1, 0], 0) == 3
    # 4. Merge Intervals
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    # 5. Rotate Matrix
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_matrix(mat)
    assert mat == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    elapsed = (time.perf_counter() - t0) * 1000
    print(f"All Prefix Sum & Kadane tests passed successfully in {elapsed:.3f} ms!")


if __name__ == "__main__":
    run_demos()
