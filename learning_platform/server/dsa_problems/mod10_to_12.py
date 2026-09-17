# -*- coding: utf-8 -*-
"""LeetCode problems for Modules 10, 11, and 12."""

PROBLEMS_MOD10_12 = [
    # -------------------------------------------------------------------------
    # MODULE 10: 1D Dynamic Programming & Sequences
    # -------------------------------------------------------------------------
    {
        "id": "lc_70_climbing_stairs",
        "module_num": 10,
        "title": "Climbing Stairs (LeetCode #70)",
        "difficulty": "Easy",
        "pattern": "Fibonacci DP / State Compression",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?""",
        "starter_code": """class Solution:
    def climbStairs(self, n: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
""",
        "visible_testcases": [
            {"input": {"n": 2}, "expected": 2},
            {"input": {"n": 3}, "expected": 3}
        ],
        "hidden_testcases": [
            {"input": {"n": 1}, "expected": 1},
            {"input": {"n": 4}, "expected": 5},
            {"input": {"n": 10}, "expected": 89},
            {"input": {"n": 5}, "expected": 8},
            {"input": {"n": 6}, "expected": 13}
        ],
        "explanation": "Recurrence relation $dp[i] = dp[i-1] + dp[i-2]$ with base cases $dp[1]=1, dp[2]=2$. Compute using two rolling variables in $O(N)$ time and $O(1)$ auxiliary space."
    },
    {
        "id": "lc_746_min_cost_climbing_stairs",
        "module_num": 10,
        "title": "Min Cost Climbing Stairs (LeetCode #746)",
        "difficulty": "Easy",
        "pattern": "1D Backward/Forward Transition",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given an integer array `cost` where `cost[i]` is the cost of `i-th` step on a staircase. Once you pay the cost, you can either climb one or two steps.
You can either start from step 0, or step 1. Return the minimum cost to reach the top floor.""",
        "starter_code": """class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        a, b = 0, 0
        for c in reversed(cost):
            a, b = c + min(a, b), a
        return min(a, b)
""",
        "visible_testcases": [
            {"input": {"cost": [10, 15, 20]}, "expected": 15},
            {"input": {"cost": [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]}, "expected": 6}
        ],
        "hidden_testcases": [
            {"input": {"cost": [0, 0, 0, 0]}, "expected": 0},
            {"input": {"cost": [10, 1]}, "expected": 1},
            {"input": {"cost": [10, 15]}, "expected": 10}
        ],
        "explanation": "Backward recurrence: $dp[i] = \text{cost}[i] + \min(dp[i+1], dp[i+2])$. Answer is $\min(dp[0], dp[1])$."
    },
    {
        "id": "lc_198_house_robber",
        "module_num": 10,
        "title": "House Robber (LeetCode #198)",
        "difficulty": "Medium",
        "pattern": "Non-Adjacent Decision DP",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected and will automatically contact the police if two adjacent houses were broken into on the same night.
Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.""",
        "starter_code": """class Solution:
    def rob(self, nums: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def rob(self, nums: list[int]) -> int:
        rob1, rob2 = 0, 0
        for n in nums:
            rob1, rob2 = rob2, max(rob1 + n, rob2)
        return rob2
""",
        "visible_testcases": [
            {"input": {"nums": [1, 2, 3, 1]}, "expected": 4},
            {"input": {"nums": [2, 7, 9, 3, 1]}, "expected": 12}
        ],
        "hidden_testcases": [
            {"input": {"nums": [0]}, "expected": 0},
            {"input": {"nums": [2, 1, 1, 2]}, "expected": 4},
            {"input": {"nums": [5]}, "expected": 5},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [1, 2]}, "expected": 2}
        ],
        "explanation": "At house i, choose either rob current house + max profit from two houses prior ($rob1 + n$), or skip current house and keep profit from previous house ($rob2$)."
    },
    {
        "id": "lc_322_coin_change",
        "module_num": 10,
        "title": "Coin Change (LeetCode #322)",
        "difficulty": "Medium",
        "pattern": "Unbounded Knapsack / Bottom-Up DP",
        "time_complexity": "O(A \times C)",
        "space_complexity": "O(A)",
        "description": """You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.
Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.
You may assume that you have an infinite number of each kind of coin.""",
        "starter_code": """class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])
        return dp[amount] if dp[amount] != float('inf') else -1
""",
        "visible_testcases": [
            {"input": {"coins": [1, 2, 5], "amount": 11}, "expected": 3},
            {"input": {"coins": [2], "amount": 3}, "expected": -1},
            {"input": {"coins": [1], "amount": 0}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"coins": [1], "amount": 2}, "expected": 2},
            {"input": {"coins": [186, 419, 83, 408], "amount": 6249}, "expected": 20},
            {"input": {"coins": [1], "amount": 1}, "expected": 1},
            {"input": {"coins": [2, 5, 10, 1], "amount": 27}, "expected": 4}
        ],
        "explanation": "Define $dp[a]$ as the minimum coins needed for amount $a$. For each coin $c$, $dp[a] = \min(dp[a], 1 + dp[a - c])$. Initialize $dp[0] = 0$."
    },
    {
        "id": "lc_300_longest_increasing_subsequence",
        "module_num": 10,
        "title": "Longest Increasing Subsequence (LeetCode #300)",
        "difficulty": "Medium",
        "pattern": "Patience Sorting / Binary Search DP",
        "time_complexity": "O(N \log N)",
        "space_complexity": "O(N)",
        "description": """Given an integer array `nums`, return the length of the longest strictly increasing subsequence.""",
        "starter_code": """class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        pass
""",
        "reference_solution": """import bisect

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails = []
        for x in nums:
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
            else:
                tails[idx] = x
        return len(tails)
""",
        "visible_testcases": [
            {"input": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, "expected": 4},
            {"input": {"nums": [0, 1, 0, 3, 2, 3]}, "expected": 4},
            {"input": {"nums": [7, 7, 7, 7, 7, 7, 7]}, "expected": 1}
        ],
        "hidden_testcases": [
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [4, 10, 4, 3, 8, 9]}, "expected": 3},
            {"input": {"nums": [0]}, "expected": 1},
            {"input": {"nums": [7, 7, 7, 7, 7]}, "expected": 1}
        ],
        "explanation": "Maintain array `tails` where `tails[i]` stores the smallest tail of all increasing subsequences of length $i+1$. Using `bisect_left` guarantees $O(N \log N)$ time."
    },
    {
        "id": "lc_139_word_break",
        "module_num": 10,
        "title": "Word Break (LeetCode #139)",
        "difficulty": "Medium",
        "pattern": "String Prefix Segmentation DP",
        "time_complexity": "O(N^2)",
        "space_complexity": "O(N)",
        "description": """Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of one or more dictionary words. Note that the same word in the dictionary may be reused multiple times.""",
        "starter_code": """class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[len(s)]
""",
        "visible_testcases": [
            {"input": {"s": "leetcode", "wordDict": ["leet", "code"]}, "expected": True},
            {"input": {"s": "applepenapple", "wordDict": ["apple", "pen"]}, "expected": True},
            {"input": {"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"s": "a", "wordDict": ["a"]}, "expected": True},
            {"input": {"s": "a", "wordDict": ["b"]}, "expected": False}
        ],
        "explanation": "$dp[i]$ is True if prefix $s[0\dots i]$ can be formed. Check all split points $j < i$: if $dp[j]$ is True and substring $s[j\dots i]$ is in dictionary, then $dp[i] = \text{True}$."
    },
    {
        "id": "lc_53_maximum_subarray",
        "module_num": 10,
        "title": "Maximum Subarray (LeetCode #53)",
        "difficulty": "Medium",
        "pattern": "Kadane's Dynamic Programming",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """Given an integer array `nums`, find the subarray with the largest sum, and return its sum.""",
        "starter_code": """class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        curr_sum = 0
        for x in nums:
            curr_sum = max(x, curr_sum + x)
            max_sum = max(max_sum, curr_sum)
        return max_sum
""",
        "visible_testcases": [
            {"input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "expected": 6},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [5, 4, -1, 7, 8]}, "expected": 23}
        ],
        "hidden_testcases": [
            {"input": {"nums": [-1]}, "expected": -1},
            {"input": {"nums": [-2, -1]}, "expected": -1}
        ],
        "explanation": "Kadane's algorithm: at each element, decide whether to start a new subarray or extend the existing one: $curr = \max(x, curr + x)$."
    },

    # -------------------------------------------------------------------------
    # MODULE 11: 2D Dynamic Programming, Knapsack & Grids
    # -------------------------------------------------------------------------
    {
        "id": "lc_62_unique_paths",
        "module_num": 11,
        "title": "Unique Paths (LeetCode #62)",
        "difficulty": "Medium",
        "pattern": "2D Grid Dynamic Programming",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(N)",
        "description": """There is a robot on an `m x n` grid. The robot is initially located at the top-left corner `(0, 0)` and tries to move to the bottom-right corner `(m - 1, n - 1)`. The robot can only move either down or right at any point in time.

Given two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.""",
        "starter_code": """class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n
        for _ in range(m - 1):
            new_row = [1] * n
            for j in range(n - 2, -1, -1):
                new_row[j] = new_row[j + 1] + row[j]
            row = new_row
        return row[0]
""",
        "visible_testcases": [
            {"input": {"m": 3, "n": 7}, "expected": 28},
            {"input": {"m": 3, "n": 2}, "expected": 3}
        ],
        "hidden_testcases": [
            {"input": {"m": 1, "n": 1}, "expected": 1},
            {"input": {"m": 7, "n": 3}, "expected": 28},
            {"input": {"m": 3, "n": 3}, "expected": 6},
            {"input": {"m": 1, "n": 5}, "expected": 1}
        ],
        "explanation": "$dp[r][c] = dp[r+1][c] + dp[r][c+1]$. Compress into a single 1D row of length N to optimize space to $O(N)$."
    },
    {
        "id": "lc_64_min_path_sum",
        "module_num": 11,
        "title": "Minimum Path Sum (LeetCode #64)",
        "difficulty": "Medium",
        "pattern": "2D Grid Cost Minimization",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(1) in-place",
        "description": """Given a `m x n` `grid` filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path. You can only move either down or right at any point in time.""",
        "starter_code": """class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        for r in range(m):
            for c in range(n):
                if r == 0 and c == 0:
                    continue
                elif r == 0:
                    grid[r][c] += grid[r][c - 1]
                elif c == 0:
                    grid[r][c] += grid[r - 1][c]
                else:
                    grid[r][c] += min(grid[r - 1][c], grid[r][c - 1])
        return grid[-1][-1]
""",
        "visible_testcases": [
            {"input": {"grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]]}, "expected": 7},
            {"input": {"grid": [[1, 2, 3], [4, 5, 6]]}, "expected": 12}
        ],
        "hidden_testcases": [
            {"input": {"grid": [[5]]}, "expected": 5},
            {"input": {"grid": [[1, 2], [1, 1]]}, "expected": 3},
            {"input": {"grid": [[1]]}, "expected": 1},
            {"input": {"grid": [[1, 2], [5, 6]]}, "expected": 9}
        ],
        "explanation": "At cell $(r, c)$, minimum path sum is $\text{grid}[r][c] + \min(dp[r-1][c], dp[r][c-1])$. We can accumulate directly into the matrix in-place."
    },
    {
        "id": "lc_1143_lcs",
        "module_num": 11,
        "title": "Longest Common Subsequence (LeetCode #1143)",
        "difficulty": "Medium",
        "pattern": "2D String Matching DP",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(M \times N)",
        "description": """Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.""",
        "starter_code": """class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
""",
        "visible_testcases": [
            {"input": {"text1": "abcde", "text2": "ace"}, "expected": 3},
            {"input": {"text1": "abc", "text2": "abc"}, "expected": 3},
            {"input": {"text1": "abc", "text2": "def"}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"text1": "bsbininm", "text2": "jmjkbkjkv"}, "expected": 1},
            {"input": {"text1": "a", "text2": "a"}, "expected": 1},
            {"input": {"text1": "ezupkr", "text2": "ubmrapg"}, "expected": 2}
        ],
        "explanation": "If characters match, $dp[i][j] = 1 + dp[i-1][j-1]$. If they don't, take $\max(dp[i-1][j], dp[i][j-1])$."
    },
    {
        "id": "lc_309_stock_cooldown",
        "module_num": 11,
        "title": "Best Time to Buy and Sell Stock with Cooldown (LeetCode #309)",
        "difficulty": "Medium",
        "pattern": "State Machine Dynamic Programming",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day. Find the maximum profit you can achieve.
After you sell your stock, you cannot buy stock on the next day (i.e., 1 day cooldown). Note: You may not engage in multiple transactions simultaneously.""",
        "starter_code": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        sold, held, reset = 0, -float('inf'), 0
        for p in prices:
            prev_sold = sold
            sold = held + p
            held = max(held, reset - p)
            reset = max(reset, prev_sold)
        return max(sold, reset)
""",
        "visible_testcases": [
            {"input": {"prices": [1, 2, 3, 0, 2]}, "expected": 3},
            {"input": {"prices": [1]}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"prices": [2, 1, 4]}, "expected": 3},
            {"input": {"prices": [6, 1, 3, 2, 4, 7]}, "expected": 6},
            {"input": {"prices": [1, 2]}, "expected": 1}
        ],
        "explanation": "Model three distinct states: `held` (own a share), `sold` (just sold today), and `reset` (ready to buy after cooldown). Transitions run in $O(N)$ with $O(1)$ space."
    },
    {
        "id": "lc_518_coin_change_2",
        "module_num": 11,
        "title": "Coin Change II (LeetCode #518)",
        "difficulty": "Medium",
        "pattern": "Unbounded Knapsack Combination Counting",
        "time_complexity": "O(A \times C)",
        "space_complexity": "O(A)",
        "description": """You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.
Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.
You may assume that you have an infinite number of each kind of coin.""",
        "starter_code": """class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for c in coins:
            for a in range(c, amount + 1):
                dp[a] += dp[a - c]
        return dp[amount]
""",
        "visible_testcases": [
            {"input": {"amount": 5, "coins": [1, 2, 5]}, "expected": 4},
            {"input": {"amount": 3, "coins": [2]}, "expected": 0},
            {"input": {"amount": 10, "coins": [10]}, "expected": 1}
        ],
        "hidden_testcases": [
            {"input": {"amount": 0, "coins": [7]}, "expected": 1},
            {"input": {"amount": 500, "coins": [3, 5, 7, 8, 9, 10, 11]}, "expected": 35502874},
            {"input": {"amount": 0, "coins": [1, 2, 5]}, "expected": 1}
        ],
        "explanation": "Outer loop iterates through each coin, inner loop increments amount. By placing the coin loop on the outside, we count unordered combinations rather than permutations."
    },
    {
        "id": "lc_72_edit_distance",
        "module_num": 11,
        "title": "Edit Distance (LeetCode #72)",
        "difficulty": "Hard",
        "pattern": "Levenshtein Matrix Dynamic Programming",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(M \times N)",
        "description": """Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.
You have the following three operations permitted on a word:
1. Insert a character
2. Delete a character
3. Replace a character""",
        "starter_code": """class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],    # delete
                        dp[i][j - 1],    # insert
                        dp[i - 1][j - 1] # replace
                    )
        return dp[m][n]
""",
        "visible_testcases": [
            {"input": {"word1": "horse", "word2": "ros"}, "expected": 3},
            {"input": {"word1": "intention", "word2": "execution"}, "expected": 5}
        ],
        "hidden_testcases": [
            {"input": {"word1": "", "word2": "a"}, "expected": 1},
            {"input": {"word1": "abc", "word2": "abc"}, "expected": 0},
            {"input": {"word1": "a", "word2": ""}, "expected": 1},
            {"input": {"word1": "", "word2": ""}, "expected": 0}
        ],
        "explanation": "Classic Levenshtein distance table where cell $(i, j)$ represents min operations to convert prefix $w1[0\dots i]$ to $w2[0\dots j]$."
    },
    {
        "id": "lc_416_partition_equal_subset_sum",
        "module_num": 11,
        "title": "Partition Equal Subset Sum (LeetCode #416)",
        "difficulty": "Medium",
        "pattern": "0/1 Knapsack Boolean Reachability",
        "time_complexity": "O(N \times \text{target})",
        "space_complexity": "O(\text{target})",
        "description": """Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `False` otherwise.""",
        "starter_code": """class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2
        dp = set([0])
        for x in nums:
            next_dp = set(dp)
            for s in dp:
                if s + x == target:
                    return True
                if s + x < target:
                    next_dp.add(s + x)
            dp = next_dp
        return target in dp
""",
        "visible_testcases": [
            {"input": {"nums": [1, 5, 11, 5]}, "expected": True},
            {"input": {"nums": [1, 2, 3, 5]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"nums": [1, 2, 5]}, "expected": False},
            {"input": {"nums": [2, 2]}, "expected": True},
            {"input": {"nums": [1, 1]}, "expected": True}
        ],
        "explanation": "If total sum is odd, partition is impossible. Otherwise target is $\text{sum} / 2$. This maps to 0/1 Knapsack: can a subset sum exactly to target?"
    },

    # -------------------------------------------------------------------------
    # MODULE 12: Greedy Algorithms & Interval Scheduling
    # -------------------------------------------------------------------------
    {
        "id": "lc_55_jump_game",
        "module_num": 12,
        "title": "Jump Game (LeetCode #55)",
        "difficulty": "Medium",
        "pattern": "Furthest Reachable Index Greedy",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
Return `True` if you can reach the last index, or `False` otherwise.""",
        "starter_code": """class Solution:
    def canJump(self, nums: list[int]) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def canJump(self, nums: list[int]) -> bool:
        max_reach = 0
        for i, jump in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i + jump)
        return True
""",
        "visible_testcases": [
            {"input": {"nums": [2, 3, 1, 1, 4]}, "expected": True},
            {"input": {"nums": [3, 2, 1, 0, 4]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"nums": [0]}, "expected": True},
            {"input": {"nums": [2, 0, 0]}, "expected": True},
            {"input": {"nums": [1, 0, 1, 0]}, "expected": False},
            {"input": {"nums": [2, 0]}, "expected": True}
        ],
        "explanation": "Track the maximum index reachable so far `max_reach`. If the current index `i` ever exceeds `max_reach`, we are stuck and cannot proceed."
    },
    {
        "id": "lc_45_jump_game_2",
        "module_num": 12,
        "title": "Jump Game II (LeetCode #45)",
        "difficulty": "Medium",
        "pattern": "BFS Window Greedy Steps",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """You are given a 0-indexed array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.
Each element `nums[i]` represents the maximum length of a forward jump from index `i`.
Return the minimum number of jumps to reach `nums[n - 1]`. You may assume you can always reach the last index.""",
        "starter_code": """class Solution:
    def jump(self, nums: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def jump(self, nums: list[int]) -> int:
        jumps = 0
        cur_end = 0
        cur_farthest = 0
        for i in range(len(nums) - 1):
            cur_farthest = max(cur_farthest, i + nums[i])
            if i == cur_end:
                jumps += 1
                cur_end = cur_farthest
        return jumps
""",
        "visible_testcases": [
            {"input": {"nums": [2, 3, 1, 1, 4]}, "expected": 2},
            {"input": {"nums": [2, 3, 0, 1, 4]}, "expected": 2}
        ],
        "hidden_testcases": [
            {"input": {"nums": [1]}, "expected": 0},
            {"input": {"nums": [7, 0, 9, 6, 9, 6, 1, 7, 9, 0, 1, 2, 9, 0, 3]}, "expected": 2},
            {"input": {"nums": [0]}, "expected": 0},
            {"input": {"nums": [1, 1, 1, 1]}, "expected": 3}
        ],
        "explanation": "Treat each jump as a BFS layer. When current pointer reaches `cur_end`, increment jump count and update `cur_end = cur_farthest` in $O(N)$."
    },
    {
        "id": "lc_134_gas_station",
        "module_num": 12,
        "title": "Gas Station (LeetCode #134)",
        "difficulty": "Medium",
        "pattern": "Deficit Accumulation and Reset",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "description": """There are `n` gas stations along a circular route, where the amount of gas at the `i-th` station is `gas[i]`.
You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i-th` station to its next `(i + 1)-th` station.
Return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return `-1`.""",
        "starter_code": """class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        if sum(gas) < sum(cost):
            return -1
        total_tank = 0
        curr_tank = 0
        start = 0
        for i in range(len(gas)):
            curr_tank += gas[i] - cost[i]
            if curr_tank < 0:
                start = i + 1
                curr_tank = 0
        return start
""",
        "visible_testcases": [
            {"input": {"gas": [1, 2, 3, 4, 5], "cost": [3, 4, 5, 1, 2]}, "expected": 3},
            {"input": {"gas": [2, 3, 4], "cost": [3, 4, 3]}, "expected": -1}
        ],
        "hidden_testcases": [
            {"input": {"gas": [5, 1, 2, 3, 4], "cost": [4, 4, 1, 5, 1]}, "expected": 4},
            {"input": {"gas": [2], "cost": [2]}, "expected": 0}
        ],
        "explanation": "If total gas >= total cost, a valid starting index is guaranteed to exist. If `curr_tank` drops below zero starting at `start`, no station between `start` and `i` could have been the valid start, so reset `start = i + 1`."
    },
    {
        "id": "lc_56_merge_intervals",
        "module_num": 12,
        "title": "Merge Intervals (LeetCode #56)",
        "difficulty": "Medium",
        "pattern": "Sort by Start Time + Linear Merge",
        "time_complexity": "O(N \log N)",
        "space_complexity": "O(N)",
        "description": """Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.""",
        "starter_code": """class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        for interval in intervals:
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                merged[-1][1] = max(merged[-1][1], interval[1])
        return merged
""",
        "visible_testcases": [
            {"input": {"intervals": [[1, 3], [2, 6], [8, 10], [15, 18]]}, "expected": [[1, 6], [8, 10], [15, 18]]},
            {"input": {"intervals": [[1, 4], [4, 5]]}, "expected": [[1, 5]]}
        ],
        "hidden_testcases": [
            {"input": {"intervals": [[1, 4], [0, 4]]}, "expected": [[0, 4]]},
            {"input": {"intervals": [[1, 4], [2, 3]]}, "expected": [[1, 4]]},
            {"input": {"intervals": [[1, 4]]}, "expected": [[1, 4]]}
        ],
        "explanation": "Sort intervals by start coordinate. If the current interval overlaps with the last interval in `merged` ($start \le end_{prev}$), extend $end_{prev} = \max(end_{prev}, end_{curr})$."
    },
    {
        "id": "lc_435_non_overlapping_intervals",
        "module_num": 12,
        "title": "Non-overlapping Intervals (LeetCode #435)",
        "difficulty": "Medium",
        "pattern": "Earliest Deadline First Greedy",
        "time_complexity": "O(N \log N)",
        "space_complexity": "O(1)",
        "description": """Given an array of intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.""",
        "starter_code": """class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        count = 0
        prev_end = -float('inf')
        for start, end in intervals:
            if start >= prev_end:
                prev_end = end
            else:
                count += 1
        return count
""",
        "visible_testcases": [
            {"input": {"intervals": [[1, 2], [2, 3], [3, 4], [1, 3]]}, "expected": 1},
            {"input": {"intervals": [[1, 2], [1, 2], [1, 2]]}, "expected": 2},
            {"input": {"intervals": [[1, 2], [2, 3]]}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"intervals": [[1, 100], [11, 22], [1, 11], [2, 12]]}, "expected": 2},
            {"input": {"intervals": [[1, 2]]}, "expected": 0}
        ],
        "explanation": "Interval Scheduling Theorem: sorting by earliest end time greedily maximizes the number of mutually compatible intervals. Any interval starting before `prev_end` is removed."
    },
    {
        "id": "lc_763_partition_labels",
        "module_num": 12,
        "title": "Partition Labels (LeetCode #763)",
        "difficulty": "Medium",
        "pattern": "Last Occurrence Greedy Partition",
        "time_complexity": "O(N)",
        "space_complexity": "O(1) (26 letters)",
        "description": """You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part.
Return a list of integers representing the size of these parts.""",
        "starter_code": """class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        pass
""",
        "reference_solution": """class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        last = {c: i for i, c in enumerate(s)}
        res = []
        anchor = 0
        end = 0
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                res.append(i - anchor + 1)
                anchor = i + 1
        return res
""",
        "visible_testcases": [
            {"input": {"s": "ababcbacadefegdehijhklij"}, "expected": [9, 7, 8]},
            {"input": {"s": "eccbbbbdec"}, "expected": [10]}
        ],
        "hidden_testcases": [
            {"input": {"s": "a"}, "expected": [1]},
            {"input": {"s": "caedbdedda"}, "expected": [1, 9]},
            {"input": {"s": "abcdef"}, "expected": [1, 1, 1, 1, 1, 1]}
        ],
        "explanation": "Precompute the last occurrence index of each character. Scan through `s` expanding the partition boundary `end = max(end, last[c])`. When `i == end`, finalize partition."
    }
]
