# -*- coding: utf-8 -*-
"""LeetCode problems for Modules 01, 02, and 03."""

PROBLEMS_MOD01_03 = [
    # -------------------------------------------------------------------------
    # MODULE 01: Complexity Analysis & Binary Search
    # -------------------------------------------------------------------------
    {
        "id": "lc_704_binary_search",
        "module_num": 1,
        "title": "Binary Search (LeetCode #704)",
        "difficulty": "Easy",
        "pattern": "Two Pointers / Divide and Conquer",
        "time_complexity": "O(\log N)",
        "space_complexity": "O(1)",
        "description": """Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

You must write an algorithm with $O(\log n)$ runtime complexity.

### Constraints
- $1 \le \text{nums.length} \le 10^4$
- $-10^4 < \text{nums}[i], \text{target} < 10^4$
- All integers in `nums` are unique.
- `nums` is sorted in ascending order.""",
        "starter_code": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # Implement logarithmic binary search
        pass
""",
        "reference_solution": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
""",
        "visible_testcases": [
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "expected": 4},
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "expected": -1}
        ],
        "hidden_testcases": [
            {"input": {"nums": [5], "target": 5}, "expected": 0},
            {"input": {"nums": [5], "target": -5}, "expected": -1},
            {"input": {"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "target": 1}, "expected": 0},
            {"input": {"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "target": 10}, "expected": 9},
            {"input": {"nums": [-100, -50, 0, 50, 100], "target": -50}, "expected": 1},
            {"input": {"nums": [1], "target": 1}, "expected": 0},
            {"input": {"nums": [1], "target": 2}, "expected": -1},
            {"input": {"nums": [1, 3], "target": 1}, "expected": 0},
            {"input": {"nums": [1, 3], "target": 3}, "expected": 1},
            {"input": {"nums": [1, 3], "target": 0}, "expected": -1},
            {"input": {"nums": [1, 3], "target": 4}, "expected": -1},
            {"input": {"nums": [-5, -2, 0, 4, 8, 12, 19], "target": 19}, "expected": 6},
            {"input": {"nums": [-5, -2, 0, 4, 8, 12, 19], "target": -5}, "expected": 0}
        ],
        "explanation": "Standard binary search with two pointers (left and right). At each step, compute mid to halve the search interval, achieving logarithmic $O(\log N)$ time and $O(1)$ auxiliary space."
    },
    {
        "id": "lc_33_search_rotated_array",
        "module_num": 1,
        "title": "Search in Rotated Sorted Array (LeetCode #33)",
        "difficulty": "Medium",
        "pattern": "Modified Binary Search",
        "time_complexity": "O(\log N)",
        "space_complexity": "O(1)",
        "description": """There is an integer array `nums` sorted in ascending order (with distinct values). Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with $O(\log n)$ runtime complexity.""",
        "starter_code": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1
""",
        "visible_testcases": [
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}, "expected": 4},
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}, "expected": -1}
        ],
        "hidden_testcases": [
            {"input": {"nums": [1], "target": 0}, "expected": -1},
            {"input": {"nums": [1], "target": 1}, "expected": 0},
            {"input": {"nums": [3, 1], "target": 1}, "expected": 1},
            {"input": {"nums": [5, 1, 3], "target": 5}, "expected": 0},
            {"input": {"nums": [4, 5, 6, 7, 8, 1, 2, 3], "target": 8}, "expected": 4},
            {"input": {"nums": [3, 1], "target": 3}, "expected": 0}
        ],
        "explanation": "At least one half of the rotated array is always strictly sorted. We identify which half is sorted by comparing nums[left] with nums[mid], then check if target lies within that sorted range."
    },
    {
        "id": "lc_153_find_min_rotated",
        "module_num": 1,
        "title": "Find Minimum in Rotated Sorted Array (LeetCode #153)",
        "difficulty": "Medium",
        "pattern": "Inflection Point Binary Search",
        "time_complexity": "O(\log N)",
        "space_complexity": "O(1)",
        "description": """Suppose an array of length `n` sorted in ascending order is rotated between 1 and `n` times.
Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

You must write an algorithm that runs in $O(\log n)$ time.""",
        "starter_code": """class Solution:
    def findMin(self, nums: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def findMin(self, nums: list[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return nums[left]
""",
        "visible_testcases": [
            {"input": {"nums": [3, 4, 5, 1, 2]}, "expected": 1},
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2]}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"nums": [11, 13, 15, 17]}, "expected": 11},
            {"input": {"nums": [2, 1]}, "expected": 1},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [3, 1, 2]}, "expected": 1},
            {"input": {"nums": [1, 2]}, "expected": 1}
        ],
        "explanation": "Compare nums[mid] to nums[right]. If nums[mid] > nums[right], the minimum must be in the right subarray (excluding mid). Otherwise, it is in the left subarray including mid."
    },
    {
        "id": "lc_74_search_2d_matrix",
        "module_num": 1,
        "title": "Search a 2D Matrix (LeetCode #74)",
        "difficulty": "Medium",
        "pattern": "2D Flattened Binary Search",
        "time_complexity": "O(\log(M \times N))",
        "space_complexity": "O(1)",
        "description": """You are given an `m x n` integer matrix `matrix` with the following two properties:
1. Each row is sorted in non-decreasing order.
2. The first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `True` if `target` is in `matrix` or `False` otherwise.
You must write a solution in $O(\log(m \cdot n))$ time.""",
        "starter_code": """class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1
        while left <= right:
            mid = (left + right) // 2
            val = matrix[mid // n][mid % n]
            if val == target:
                return True
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1
        return False
""",
        "visible_testcases": [
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 3}, "expected": True},
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 13}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"matrix": [[1]], "target": 1}, "expected": True},
            {"input": {"matrix": [[1]], "target": 2}, "expected": False},
            {"input": {"matrix": [[1, 3]], "target": 3}, "expected": True},
            {"input": {"matrix": [[1, 4, 7, 11], [12, 13, 14, 15], [16, 17, 18, 19]], "target": 19}, "expected": True},
            {"input": {"matrix": [[1]], "target": 0}, "expected": False},
            {"input": {"matrix": [[1], [3]], "target": 1}, "expected": True},
            {"input": {"matrix": [[1], [3]], "target": 2}, "expected": False},
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 60}, "expected": True}
        ],
        "explanation": "Treat the M x N matrix as a single flattened 1D array of length M*N. Any 1D index `idx` maps directly to 2D coordinates via row = idx // N and col = idx % N."
    },
    {
        "id": "lc_278_first_bad_version",
        "module_num": 1,
        "title": "First Bad Version (LeetCode #278)",
        "difficulty": "Easy",
        "pattern": "Lower Bound Predicate Binary Search",
        "time_complexity": "O(\log N)",
        "space_complexity": "O(1)",
        "description": """Suppose you have `n` versions `[1, 2, ..., n]` and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API `isBadVersion(version)` which returns whether `version` is bad. Implement a function to find the first bad version with minimum API calls.""",
        "starter_code": """class Solution:
    def firstBadVersion(self, n: int, isBadVersion) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def firstBadVersion(self, n: int, isBadVersion) -> int:
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1
        return left
""",
        "visible_testcases": [
            {"input": {"n": 5, "first_bad": 4}, "expected": 4},
            {"input": {"n": 1, "first_bad": 1}, "expected": 1}
        ],
        "hidden_testcases": [
            {"input": {"n": 100, "first_bad": 50}, "expected": 50},
            {"input": {"n": 1000, "first_bad": 1}, "expected": 1},
            {"input": {"n": 10000, "first_bad": 9999}, "expected": 9999}
        ],
        "explanation": "Binary search on monotonic predicate: if `isBadVersion(mid)` is True, the first bad version is at or to the left of `mid` (right = mid). Otherwise it is strictly to the right (left = mid + 1)."
    },
    {
        "id": "lc_875_koko_eating_bananas",
        "module_num": 1,
        "title": "Koko Eating Bananas (LeetCode #875)",
        "difficulty": "Medium",
        "pattern": "Binary Search on Answer Space",
        "time_complexity": "O(N \log(\max(P)))",
        "space_complexity": "O(1)",
        "description": """Koko loves to eat bananas. There are `n` piles of bananas, the `i-th` pile has `piles[i]` bananas. The guards will come back in `h` hours.

Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile and eats `k` bananas from it. If the pile has less than `k` bananas, she eats all of them and will not eat any more bananas during this hour.

Return the minimum integer `k` such that she can eat all the bananas within `h` hours.""",
        "starter_code": """class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        import math
        left, right = 1, max(piles)
        ans = right
        while left <= right:
            mid = (left + right) // 2
            hours = sum(math.ceil(p / mid) for p in piles)
            if hours <= h:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        return ans
""",
        "visible_testcases": [
            {"input": {"piles": [3, 6, 7, 11], "h": 8}, "expected": 4},
            {"input": {"piles": [30, 11, 23, 4, 20], "h": 5}, "expected": 30},
            {"input": {"piles": [30, 11, 23, 4, 20], "h": 6}, "expected": 23}
        ],
        "hidden_testcases": [
            {"input": {"piles": [312884470], "h": 312884469}, "expected": 2},
            {"input": {"piles": [1, 1, 1, 1], "h": 4}, "expected": 1},
            {"input": {"piles": [1000000000], "h": 2}, "expected": 500000000},
            {"input": {"piles": [312884470], "h": 312884470}, "expected": 1},
            {"input": {"piles": [1], "h": 1}, "expected": 1}
        ],
        "explanation": "Search space is the speed k from 1 to max(piles). The feasibility function `sum(ceil(p/k)) <= h` is monotonic: if speed k works, all speeds > k also work. We use binary search to locate the minimum feasible speed."
    },

    # -------------------------------------------------------------------------
    # MODULE 02: Arrays, Dynamic Arrays & Strings
    # -------------------------------------------------------------------------
    {
        "id": "lc_1_two_sum",
        "module_num": 2,
        "title": "Two Sum (LeetCode #1)",
        "difficulty": "Easy",
        "pattern": "Hash Map Complement",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.""",
        "starter_code": """class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        pass
""",
        "reference_solution": """class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            comp = target - num
            if comp in seen:
                return [seen[comp], i]
            seen[num] = i
        return []
""",
        "visible_testcases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]}
        ],
        "hidden_testcases": [
            {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]},
            {"input": {"nums": [-1, -2, -3, -4, -5], "target": -8}, "expected": [2, 4]},
            {"input": {"nums": [100, 200, 300, 400], "target": 700}, "expected": [2, 3]},
            {"input": {"nums": [0, 4, 3, 0], "target": 0}, "expected": [0, 3]}
        ],
        "explanation": "Iterate through nums while storing seen numbers and their indices in a hash map. For each number, check if `target - num` already exists in the table in $O(1)$ amortized time."
    },
    {
        "id": "lc_121_best_time_stock",
        "module_num": 2,
        "title": "Best Time to Buy and Sell Stock (LeetCode #121)",
        "difficulty": "Easy",
        "pattern": "Prefix Minimum / One-Pass Greedy",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit. If no profit can be achieved, return `0`.""",
        "starter_code": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float('inf')
        max_profit = 0
        for p in prices:
            if p < min_price:
                min_price = p
            elif p - min_price > max_profit:
                max_profit = p - min_price
        return max_profit
""",
        "visible_testcases": [
            {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "expected": 5},
            {"input": {"prices": [7, 6, 4, 3, 1]}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"prices": [1]}, "expected": 0},
            {"input": {"prices": [2, 4, 1]}, "expected": 2},
            {"input": {"prices": [3, 2, 6, 5, 0, 3]}, "expected": 4},
            {"input": {"prices": [1, 2, 3, 4, 5]}, "expected": 4}
        ],
        "explanation": "Maintain the running minimum price seen so far. At each day, calculate profit if sold today (current_price - min_price) and update max_profit."
    },
    {
        "id": "lc_15_3sum",
        "module_num": 2,
        "title": "3Sum (LeetCode #15)",
        "difficulty": "Medium",
        "pattern": "Sorting + Two Pointers",
        "time_complexity": "O(N^2)",
        "space_complexity": "O(1)",
        "is_unordered": True,
        "description": """Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.""",
        "starter_code": """class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        n = len(nums)
        for i in range(n - 2):
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
""",
        "visible_testcases": [
            {"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "expected": [[-1, -1, 2], [-1, 0, 1]]},
            {"input": {"nums": [0, 1, 1]}, "expected": []},
            {"input": {"nums": [0, 0, 0]}, "expected": [[0, 0, 0]]}
        ],
        "hidden_testcases": [
            {"input": {"nums": [-2, 0, 1, 1, 2]}, "expected": [[-2, 0, 2], [-2, 1, 1]]},
            {"input": {"nums": [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]}, "expected": [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]},
            {"input": {"nums": [0, 0, 0, 0]}, "expected": [[0, 0, 0]]},
            {"input": {"nums": [-1, 0, 1, 0]}, "expected": [[-1, 0, 1]]},
            {"input": {"nums": [-1, -1, 2]}, "expected": [[-1, -1, 2]]}
        ],
        "explanation": "Sort array first ($O(N \log N)$). Iterate through each candidate first element, skipping duplicates. Use two pointers inward on the remainder of the array to find pairs summing to $-nums[i]$."
    },
    {
        "id": "lc_11_container_most_water",
        "module_num": 2,
        "title": "Container With Most Water (LeetCode #11)",
        "difficulty": "Medium",
        "pattern": "Two Pointers Squeeze",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.""",
        "starter_code": """class Solution:
    def maxArea(self, height: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        max_water = 0
        while left < right:
            h = min(height[left], height[right])
            max_water = max(max_water, h * (right - left))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_water
""",
        "visible_testcases": [
            {"input": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "expected": 49},
            {"input": {"height": [1, 1]}, "expected": 1}
        ],
        "hidden_testcases": [
            {"input": {"height": [4, 3, 2, 1, 4]}, "expected": 16},
            {"input": {"height": [1, 2, 1]}, "expected": 2},
            {"input": {"height": [2, 3, 4, 5, 18, 17, 6]}, "expected": 17}
        ],
        "explanation": "Start pointers at both ends to maximize width. The water volume is bounded by the shorter line: $\text{area} = \min(h[l], h[r]) \times (r - l)$. Advancing the shorter line is the only way to potentially find a larger area."
    },
    {
        "id": "lc_238_product_except_self",
        "module_num": 2,
        "title": "Product of Array Except Self (LeetCode #238)",
        "difficulty": "Medium",
        "pattern": "Prefix & Suffix Accumulation",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

You must write an algorithm that runs in $O(n)$ time and without using the division operation.""",
        "starter_code": """class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        pass
""",
        "reference_solution": """class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
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
""",
        "visible_testcases": [
            {"input": {"nums": [1, 2, 3, 4]}, "expected": [24, 12, 8, 6]},
            {"input": {"nums": [-1, 1, 0, -3, 3]}, "expected": [0, 0, 9, 0, 0]}
        ],
        "hidden_testcases": [
            {"input": {"nums": [2, 3]}, "expected": [3, 2]},
            {"input": {"nums": [0, 0]}, "expected": [0, 0]},
            {"input": {"nums": [4, 5, 1, 8, 2]}, "expected": [80, 64, 320, 40, 160]}
        ],
        "explanation": "For any index i, the product except nums[i] equals (prefix product up to i-1) * (suffix product from i+1 to n-1). Pass forwards to build prefix, then backwards with a running suffix variable."
    },
    {
        "id": "lc_3_longest_substring_no_repeat",
        "module_num": 2,
        "title": "Longest Substring Without Repeating Characters (LeetCode #3)",
        "difficulty": "Medium",
        "pattern": "Sliding Window with Hash Map",
        "time_complexity": "O(N)",
        "space_complexity": "O(\min(N, \Sigma))",
        "description": """Given a string `s`, find the length of the longest substring without repeating characters.""",
        "starter_code": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_idx = {}
        left = 0
        max_len = 0
        for right, ch in enumerate(s):
            if ch in char_idx and char_idx[ch] >= left:
                left = char_idx[ch] + 1
            char_idx[ch] = right
            max_len = max(max_len, right - left + 1)
        return max_len
""",
        "visible_testcases": [
            {"input": {"s": "abcabcbb"}, "expected": 3},
            {"input": {"s": "bbbbb"}, "expected": 1},
            {"input": {"s": "pwwkew"}, "expected": 3}
        ],
        "hidden_testcases": [
            {"input": {"s": ""}, "expected": 0},
            {"input": {"s": " "}, "expected": 1},
            {"input": {"s": "dvdf"}, "expected": 3},
            {"input": {"s": "tmmzuxt"}, "expected": 5},
            {"input": {"s": "au"}, "expected": 2},
            {"input": {"s": "abba"}, "expected": 2},
            {"input": {"s": "abcdefghijklmnopqrstuvwxyz"}, "expected": 26}
        ],
        "explanation": "Sliding window [left, right]. Store the last seen index of each character. When a duplicate is encountered inside the current window, shift `left` directly to last_index + 1."
    },
    {
        "id": "lc_42_trapping_rain_water",
        "module_num": 2,
        "title": "Trapping Rain Water (LeetCode #42)",
        "difficulty": "Hard",
        "pattern": "Two Pointers / Prefix Maximum",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.""",
        "starter_code": """class Solution:
    def trap(self, height: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def trap(self, height: list[int]) -> int:
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
""",
        "visible_testcases": [
            {"input": {"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}, "expected": 6},
            {"input": {"height": [4, 2, 0, 3, 2, 5]}, "expected": 9}
        ],
        "hidden_testcases": [
            {"input": {"height": []}, "expected": 0},
            {"input": {"height": [3]}, "expected": 0},
            {"input": {"height": [5, 4, 1, 2]}, "expected": 1},
            {"input": {"height": [2, 0, 2]}, "expected": 2},
            {"input": {"height": [1]}, "expected": 0},
            {"input": {"height": [1, 2]}, "expected": 0},
            {"input": {"height": [3, 0, 0, 2, 0, 4]}, "expected": 10}
        ],
        "explanation": "Water trapped at index i is determined by $\min(\text{left\_max}, \text{right\_max}) - \text{height}[i]$. By advancing whichever boundary has the smaller max, we guarantee the water height at that position is strictly dictated by that boundary."
    },

    # -------------------------------------------------------------------------
    # MODULE 03: Linked Lists & Pointer Manipulation
    # -------------------------------------------------------------------------
    {
        "id": "lc_206_reverse_linked_list",
        "module_num": 3,
        "title": "Reverse Linked List (LeetCode #206)",
        "difficulty": "Easy",
        "pattern": "Three Pointers Iterative",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """Given the `head` of a singly linked list, reverse the list, and return the reversed list.""",
        "starter_code": """# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass
""",
        "reference_solution": """class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev
""",
        "visible_testcases": [
            {"input": {"head": [1, 2, 3, 4, 5]}, "expected": [5, 4, 3, 2, 1]},
            {"input": {"head": [1, 2]}, "expected": [2, 1]},
            {"input": {"head": []}, "expected": []}
        ],
        "hidden_testcases": [
            {"input": {"head": [1]}, "expected": [1]},
            {"input": {"head": [10, 20, 30, 40]}, "expected": [40, 30, 20, 10]},
            {"input": {"head": [9, 8, 7]}, "expected": [7, 8, 9]}
        ],
        "explanation": "Maintain `prev` initialized to None and `curr` to head. At each node, save `curr.next`, reverse pointer `curr.next = prev`, then advance `prev` and `curr`."
    },
    {
        "id": "lc_21_merge_two_sorted_lists",
        "module_num": 3,
        "title": "Merge Two Sorted Lists (LeetCode #21)",
        "difficulty": "Easy",
        "pattern": "Dummy Node Merge",
        "time_complexity": "O(N + M)",
        "space_complexity": "O(1)",
        "description": """You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.""",
        "starter_code": """class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        pass
""",
        "reference_solution": """class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(-1)
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 if list1 else list2
        return dummy.next
""",
        "visible_testcases": [
            {"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "expected": [1, 1, 2, 3, 4, 4]},
            {"input": {"list1": [], "list2": []}, "expected": []},
            {"input": {"list1": [], "list2": [0]}, "expected": [0]}
        ],
        "hidden_testcases": [
            {"input": {"list1": [5], "list2": [1, 2, 3, 4]}, "expected": [1, 2, 3, 4, 5]},
            {"input": {"list1": [2], "list2": [1]}, "expected": [1, 2]},
            {"input": {"list1": [1], "list2": []}, "expected": [1]},
            {"input": {"list1": [1, 3, 5], "list2": [2, 4, 6]}, "expected": [1, 2, 3, 4, 5, 6]},
            {"input": {"list1": [1, 1, 1], "list2": [2, 2, 2]}, "expected": [1, 1, 1, 2, 2, 2]}
        ],
        "explanation": "Create a dummy sentinel head. At each step compare current values of list1 and list2, attach the smaller node to tail.next, and advance. Attach any remaining non-empty list at the end."
    },
    {
        "id": "lc_141_linked_list_cycle",
        "module_num": 3,
        "title": "Linked List Cycle (LeetCode #141)",
        "difficulty": "Easy",
        "pattern": "Floyd's Tortoise and Hare",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Return `True` if there is a cycle in the linked list. Otherwise, return `False`.""",
        "starter_code": """class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
""",
        "visible_testcases": [
            {"input": {"head": [3, 2, 0, -4]}, "expected": False},
            {"input": {"head": [1, 2]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"head": []}, "expected": False},
            {"input": {"head": [1]}, "expected": False},
            {"input": {"head": [], "pos": -1}, "expected": False},
            {"input": {"head": [1], "pos": -1}, "expected": False},
            {"input": {"head": [1], "pos": 0}, "expected": True},
            {"input": {"head": [1, 2], "pos": 0}, "expected": True},
            {"input": {"head": [3, 2, 0, -4], "pos": 1}, "expected": True}
        ],
        "explanation": "Slow pointer moves 1 step, fast pointer moves 2 steps. If a cycle exists, the fast pointer will eventually overlap with the slow pointer inside the cycle."
    },
    {
        "id": "lc_19_remove_nth_node_from_end",
        "module_num": 3,
        "title": "Remove Nth Node From End of List (LeetCode #19)",
        "difficulty": "Medium",
        "pattern": "Two Pointers Fast/Slow Offset",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """Given the `head` of a linked list, remove the `n-th` node from the end of the list and return its head.""",
        "starter_code": """class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        pass
""",
        "reference_solution": """class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = dummy
        slow = dummy
        for _ in range(n):
            fast = fast.next
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next
""",
        "visible_testcases": [
            {"input": {"head": [1, 2, 3, 4, 5], "n": 2}, "expected": [1, 2, 3, 5]},
            {"input": {"head": [1], "n": 1}, "expected": []},
            {"input": {"head": [1, 2], "n": 1}, "expected": [1]}
        ],
        "hidden_testcases": [
            {"input": {"head": [1, 2], "n": 2}, "expected": [2]},
            {"input": {"head": [1, 2, 3], "n": 3}, "expected": [2, 3]},
            {"input": {"head": [1, 2, 3, 4, 5], "n": 5}, "expected": [2, 3, 4, 5]}
        ],
        "explanation": "Advance fast pointer n steps ahead. Then advance both fast and slow until fast reaches the last node. slow.next is now pointing to the node that needs deletion."
    },
    {
        "id": "lc_143_reorder_list",
        "module_num": 3,
        "title": "Reorder List (LeetCode #143)",
        "difficulty": "Medium",
        "pattern": "Find Middle + Reverse + Interleave",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given the head of a singly linked-list: $L_0 \to L_1 \to \dots \to L_{n-1} \to L_n$.
Reorder the list to be: $L_0 \to L_n \to L_1 \to L_{n-1} \to L_2 \to L_{n-2} \to \dots$
You may not modify the values in the list's nodes. Only nodes themselves may be changed.""",
        "starter_code": """class Solution:
    def reorderList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pass
""",
        "reference_solution": """class Solution:
    def reorderList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        # 1. Find middle with slow/fast
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 2. Reverse second half
        prev, curr = None, slow.next
        slow.next = None
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        # 3. Interleave first and reversed second
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first = tmp1
            second = tmp2
        return head
""",
        "visible_testcases": [
            {"input": {"head": [1, 2, 3, 4]}, "expected": [1, 4, 2, 3]},
            {"input": {"head": [1, 2, 3, 4, 5]}, "expected": [1, 5, 2, 4, 3]}
        ],
        "hidden_testcases": [
            {"input": {"head": [1]}, "expected": [1]},
            {"input": {"head": [1, 2]}, "expected": [1, 2]},
            {"input": {"head": [1, 2, 3]}, "expected": [1, 3, 2]}
        ],
        "explanation": "Divide the problem into 3 standard subroutines: 1. Find middle node using slow/fast pointers. 2. Reverse the second half in-place. 3. Merge/interleave the two halves."
    },
    {
        "id": "lc_23_merge_k_sorted_lists",
        "module_num": 3,
        "title": "Merge k Sorted Lists (LeetCode #23)",
        "difficulty": "Hard",
        "pattern": "Min-Heap / Priority Queue",
        "time_complexity": "O(N \log K)",
        "space_complexity": "O(K)",
        "description": """You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.""",
        "starter_code": """class Solution:
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        pass
""",
        "reference_solution": """class Solution:
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        import heapq
        dummy = ListNode(0)
        curr = dummy
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))
        while heap:
            val, i, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next
""",
        "visible_testcases": [
            {"input": {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]}, "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
            {"input": {"lists": []}, "expected": []},
            {"input": {"lists": [[]]}, "expected": []}
        ],
        "hidden_testcases": [
            {"input": {"lists": [[-1, 1], [-2, 2], [-3, 3]]}, "expected": [-3, -2, -1, 1, 2, 3]},
            {"input": {"lists": [[1], [0]]}, "expected": [0, 1]},
            {"input": {"lists": [[], [1]]}, "expected": [1]}
        ],
        "explanation": "Maintain a min-heap storing (node.val, list_index, node). At each step pop the minimum element, append it to the merged list, and push node.next into the heap."
    }
]
