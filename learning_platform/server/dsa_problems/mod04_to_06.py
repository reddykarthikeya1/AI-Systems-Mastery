# -*- coding: utf-8 -*-
"""LeetCode problems for Modules 04, 05, and 06."""

PROBLEMS_MOD04_06 = [
    # -------------------------------------------------------------------------
    # MODULE 04: Stacks, Queues & Monotonic Structures
    # -------------------------------------------------------------------------
    {
        "id": "lc_20_valid_parentheses",
        "module_num": 4,
        "title": "Valid Parentheses (LeetCode #20)",
        "difficulty": "Easy",
        "pattern": "LIFO Stack Matching",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.""",
        "starter_code": """class Solution:
    def isValid(self, s: str) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        for char in s:
            if char in mapping:
                top = stack.pop() if stack else '#'
                if mapping[char] != top:
                    return False
            else:
                stack.append(char)
        return not stack
""",
        "visible_testcases": [
            {"input": {"s": "()"}, "expected": True},
            {"input": {"s": "()[]{}"}, "expected": True},
            {"input": {"s": "(]"}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"s": "([)]"}, "expected": False},
            {"input": {"s": "{[]}"}, "expected": True},
            {"input": {"s": "["}, "expected": False},
            {"input": {"s": "]"}, "expected": False}
        ],
        "explanation": "Push open brackets onto a LIFO stack. When a closing bracket is encountered, pop the top of the stack and check for type matching. At the end, verify stack is empty."
    },
    {
        "id": "lc_155_min_stack",
        "module_num": 4,
        "title": "Min Stack (LeetCode #155)",
        "difficulty": "Medium",
        "pattern": "Dual Stack / Paired Minimum",
        "time_complexity": "O(1) all ops",
        "space_complexity": "O(N)",
        "is_design": True,
        "target_class": "MinStack",
        "description": """Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element in constant time $O(1)$.

Implement the `MinStack` class:
- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element `val` onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.""",
        "starter_code": """class MinStack:
    def __init__(self):
        pass

    def push(self, val: int) -> None:
        pass

    def pop(self) -> None:
        pass

    def top(self) -> int:
        pass

    def getMin(self) -> int:
        pass
""",
        "reference_solution": """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            if self.min_stack and val == self.min_stack[-1]:
                self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1] if self.stack else None

    def getMin(self) -> int:
        return self.min_stack[-1] if self.min_stack else None
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
                    "args": [[], [-2], [0], [-3], [], [], [], []]
                },
                "expected": [None, None, None, None, -3, None, 0, -2]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["MinStack", "push", "push", "getMin", "getMin", "pop", "getMin"],
                    "args": [[], [2], [1], [], [], [], []]
                },
                "expected": [None, None, None, 1, 1, None, 2]
            }
        ],
        "explanation": "Maintain an auxiliary min_stack tracking current minimums. When pushing val <= min_stack[-1], push to min_stack. When popping equal value, pop from min_stack."
    },
    {
        "id": "lc_739_daily_temperatures",
        "module_num": 4,
        "title": "Daily Temperatures (LeetCode #739)",
        "difficulty": "Medium",
        "pattern": "Monotonic Decreasing Stack",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0` instead.""",
        "starter_code": """class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        pass
""",
        "reference_solution": """class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        ans = [0] * n
        stack = []  # indices of monotonic decreasing temps
        for i, t in enumerate(temperatures):
            while stack and t > temperatures[stack[-1]]:
                prev_idx = stack.pop()
                ans[prev_idx] = i - prev_idx
            stack.append(i)
        return ans
""",
        "visible_testcases": [
            {"input": {"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]}, "expected": [1, 1, 4, 2, 1, 1, 0, 0]},
            {"input": {"temperatures": [30, 40, 50, 60]}, "expected": [1, 1, 1, 0]},
            {"input": {"temperatures": [30, 60, 90]}, "expected": [1, 1, 0]}
        ],
        "hidden_testcases": [
            {"input": {"temperatures": [89, 62, 70, 58, 47, 47, 46, 76, 100, 70]}, "expected": [8, 1, 5, 4, 3, 2, 1, 1, 0, 0]},
            {"input": {"temperatures": [50, 50, 50]}, "expected": [0, 0, 0]}
        ],
        "explanation": "Use a monotonic stack storing indices of days. As soon as a warmer temperature appears, pop smaller previous temperatures and compute distance $i - \text{prev\_idx}$."
    },
    {
        "id": "lc_150_eval_rpn",
        "module_num": 4,
        "title": "Evaluate Reverse Polish Notation (LeetCode #150)",
        "difficulty": "Medium",
        "pattern": "Postfix Stack Evaluation",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """You are given an array of strings `tokens` that represents an arithmetic expression in Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.
Division between two integers always truncates toward zero.""",
        "starter_code": """class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for t in tokens:
            if t not in {"+", "-", "*", "/"}:
                stack.append(int(t))
            else:
                b = stack.pop()
                a = stack.pop()
                if t == "+":
                    stack.append(a + b)
                elif t == "-":
                    stack.append(a - b)
                elif t == "*":
                    stack.append(a * b)
                elif t == "/":
                    stack.append(int(a / b))
        return stack[0]
""",
        "visible_testcases": [
            {"input": {"tokens": ["2", "1", "+", "3", "*"]}, "expected": 9},
            {"input": {"tokens": ["4", "13", "5", "/", "+"]}, "expected": 6},
            {"input": {"tokens": ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]}, "expected": 22}
        ],
        "hidden_testcases": [
            {"input": {"tokens": ["3", "-4", "+"]}, "expected": -1},
            {"input": {"tokens": ["18"]}, "expected": 18}
        ],
        "explanation": "Iterate tokens. Push numbers onto stack. When an operator is met, pop operand b then operand a, perform operation $a \text{ op } b$, and push result back."
    },
    {
        "id": "lc_232_implement_queue_using_stacks",
        "module_num": 4,
        "title": "Implement Queue using Stacks (LeetCode #232)",
        "difficulty": "Easy",
        "pattern": "Dual Stack In/Out FIFO Simulation",
        "time_complexity": "Amortized O(1) all ops",
        "space_complexity": "O(N)",
        "is_design": True,
        "target_class": "MyQueue",
        "description": """Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `peek`, `pop`, and `empty`).""",
        "starter_code": """class MyQueue:
    def __init__(self):
        pass

    def push(self, x: int) -> None:
        pass

    def pop(self) -> int:
        pass

    def peek(self) -> int:
        pass

    def empty(self) -> bool:
        pass
""",
        "reference_solution": """class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _transfer(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["MyQueue", "push", "push", "peek", "pop", "empty"],
                    "args": [[], [1], [2], [], [], []]
                },
                "expected": [None, None, None, 1, 1, False]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["MyQueue", "push", "pop", "empty"],
                    "args": [[], [10], [], []]
                },
                "expected": [None, None, 10, True]
            }
        ],
        "explanation": "Use `in_stack` to accept pushes and `out_stack` for pop/peek. When `out_stack` is empty, dump elements from `in_stack` to invert order. Each item is moved at most twice, yielding amortized $O(1)$ per operation."
    },
    {
        "id": "lc_84_largest_rectangle_histogram",
        "module_num": 4,
        "title": "Largest Rectangle in Histogram (LeetCode #84)",
        "difficulty": "Hard",
        "pattern": "Monotonic Increasing Stack",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.""",
        "starter_code": """class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []  # pairs (index, height)
        max_area = 0
        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                idx, prev_h = stack.pop()
                max_area = max(max_area, prev_h * (i - idx))
                start = idx
            stack.append((start, h))
        n = len(heights)
        for idx, h in stack:
            max_area = max(max_area, h * (n - idx))
        return max_area
""",
        "visible_testcases": [
            {"input": {"heights": [2, 1, 5, 6, 2, 3]}, "expected": 10},
            {"input": {"heights": [2, 4]}, "expected": 4}
        ],
        "hidden_testcases": [
            {"input": {"heights": [1]}, "expected": 1},
            {"input": {"heights": [2, 1, 2]}, "expected": 3},
            {"input": {"heights": [5, 4, 3, 2, 1]}, "expected": 9}
        ],
        "explanation": "Maintain a monotonic increasing stack of (start_index, height). When a shorter bar is encountered, pop taller bars and calculate rectangle area with popped height extending from its start_index to current index."
    },

    # -------------------------------------------------------------------------
    # MODULE 05: Hash Tables & Collision Resolution
    # -------------------------------------------------------------------------
    {
        "id": "lc_217_contains_duplicate",
        "module_num": 5,
        "title": "Contains Duplicate (LeetCode #217)",
        "difficulty": "Easy",
        "pattern": "Hash Set Membership",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.""",
        "starter_code": """class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False
""",
        "visible_testcases": [
            {"input": {"nums": [1, 2, 3, 1]}, "expected": True},
            {"input": {"nums": [1, 2, 3, 4]}, "expected": False},
            {"input": {"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}, "expected": True}
        ],
        "hidden_testcases": [
            {"input": {"nums": [99]}, "expected": False},
            {"input": {"nums": [0, -1, -2, -1]}, "expected": True}
        ],
        "explanation": "Iterate through elements adding to a hash set. If an element is already in the set, a duplicate is found in $O(1)$ amortized time."
    },
    {
        "id": "lc_242_valid_anagram",
        "module_num": 5,
        "title": "Valid Anagram (LeetCode #242)",
        "difficulty": "Easy",
        "pattern": "Character Frequency Counting",
        "time_complexity": "O(N)",
        "space_complexity": "O(1) (bounded alphabet)",
        "description": """Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An Anagram is a word formed by rearranging the letters of a different word, typically using all the original letters exactly once.""",
        "starter_code": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        from collections import Counter
        return Counter(s) == Counter(t)
""",
        "visible_testcases": [
            {"input": {"s": "anagram", "t": "nagaram"}, "expected": True},
            {"input": {"s": "rat", "t": "car"}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"s": "a", "t": "ab"}, "expected": False},
            {"input": {"s": "ab", "t": "a"}, "expected": False},
            {"input": {"s": "aa", "t": "bb"}, "expected": False}
        ],
        "explanation": "Compare character frequency counts. If lengths differ, immediately return False. Otherwise tally frequencies and verify equality in $O(N)$ time."
    },
    {
        "id": "lc_49_group_anagrams",
        "module_num": 5,
        "title": "Group Anagrams (LeetCode #49)",
        "difficulty": "Medium",
        "pattern": "Canonical Tuple / Sorted Key Grouping",
        "time_complexity": "O(N \cdot K \log K)",
        "space_complexity": "O(N \cdot K)",
        "is_unordered": True,
        "description": """Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.""",
        "starter_code": """class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        pass
""",
        "reference_solution": """class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        from collections import defaultdict
        groups = defaultdict(list)
        for s in strs:
            key = "".join(sorted(s))
            groups[key].append(s)
        return list(groups.values())
""",
        "visible_testcases": [
            {"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]},
            {"input": {"strs": [""]}, "expected": [[""]]},
            {"input": {"strs": ["a"]}, "expected": [["a"]]}
        ],
        "hidden_testcases": [
            {"input": {"strs": ["a", "b", "a"]}, "expected": [["a", "a"], ["b"]]},
            {"input": {"strs": ["cab", "tin", "pew", "duh", "may", "ill", "buy", "bar", "max", "doc"]}, "expected": [["cab"], ["tin"], ["pew"], ["duh"], ["may"], ["ill"], ["buy"], ["bar"], ["max"], ["doc"]]}
        ],
        "explanation": "Map each word to its canonical form (the sorted characters). Words with the exact same canonical string belong to the same anagram group."
    },
    {
        "id": "lc_347_top_k_frequent",
        "module_num": 5,
        "title": "Top K Frequent Elements (LeetCode #347)",
        "difficulty": "Medium",
        "pattern": "Frequency Hash Map + Bucket Sort",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "is_unordered": True,
        "description": """Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.""",
        "starter_code": """class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        pass
""",
        "reference_solution": """class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        from collections import Counter
        count = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for val, freq in count.items():
            buckets[freq].append(val)
        res = []
        for freq in range(len(buckets) - 1, 0, -1):
            for val in buckets[freq]:
                res.append(val)
                if len(res) == k:
                    return res
        return res
""",
        "visible_testcases": [
            {"input": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, "expected": [1, 2]},
            {"input": {"nums": [1], "k": 1}, "expected": [1]}
        ],
        "hidden_testcases": [
            {"input": {"nums": [4, 1, -1, 2, -1, 2, 3], "k": 2}, "expected": [-1, 2]},
            {"input": {"nums": [5, 3, 1, 1, 1, 3, 73, 1], "k": 1}, "expected": [1]}
        ],
        "explanation": "Tally counts with a hash map, then use Bucket Sort where index represents frequency (0 to N). Traverse buckets from highest frequency downwards to collect k elements in $O(N)$ linear time."
    },
    {
        "id": "lc_128_longest_consecutive_sequence",
        "module_num": 5,
        "title": "Longest Consecutive Sequence (LeetCode #128)",
        "difficulty": "Medium",
        "pattern": "Hash Set Intelligent Expansion",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in $O(n)$ time.""",
        "starter_code": """class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        num_set = set(nums)
        longest = 0
        for num in num_set:
            if num - 1 not in num_set:
                curr = num
                curr_len = 1
                while curr + 1 in num_set:
                    curr += 1
                    curr_len += 1
                longest = max(longest, curr_len)
        return longest
""",
        "visible_testcases": [
            {"input": {"nums": [100, 4, 200, 1, 3, 2]}, "expected": 4},
            {"input": {"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}, "expected": 9}
        ],
        "hidden_testcases": [
            {"input": {"nums": []}, "expected": 0},
            {"input": {"nums": [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]}, "expected": 7}
        ],
        "explanation": "Store numbers in a hash set. Only begin counting sequence length from numbers that are the start of a streak (i.e., `num - 1` is not in set). Each number is visited at most twice, guaranteeing $O(N)$ time."
    },
    {
        "id": "lc_560_subarray_sum_equals_k",
        "module_num": 5,
        "title": "Subarray Sum Equals K (LeetCode #560)",
        "difficulty": "Medium",
        "pattern": "Prefix Sum Hash Map",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

A subarray is a contiguous non-empty sequence of elements within an array.""",
        "starter_code": """class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        from collections import defaultdict
        prefix_count = defaultdict(int)
        prefix_count[0] = 1
        curr_sum = 0
        count = 0
        for x in nums:
            curr_sum += x
            count += prefix_count[curr_sum - k]
            prefix_count[curr_sum] += 1
        return count
""",
        "visible_testcases": [
            {"input": {"nums": [1, 1, 1], "k": 2}, "expected": 2},
            {"input": {"nums": [1, 2, 3], "k": 3}, "expected": 2}
        ],
        "hidden_testcases": [
            {"input": {"nums": [1, -1, 0], "k": 0}, "expected": 3},
            {"input": {"nums": [1], "k": 0}, "expected": 0},
            {"input": {"nums": [-1, -1, 1], "k": 0}, "expected": 1}
        ],
        "explanation": "Subarray sum $(i \dots j) = \text{prefix}[j] - \text{prefix}[i-1] = k$. Thus $\text{prefix}[i-1] = \text{prefix}[j] - k$. As we accumulate running prefix sum, add occurrences of `prefix_sum - k` to count in $O(N)$."
    },

    # -------------------------------------------------------------------------
    # MODULE 06: Trees, Binary Search Trees & Self-Balancing
    # -------------------------------------------------------------------------
    {
        "id": "lc_104_max_depth_binary_tree",
        "module_num": 6,
        "title": "Maximum Depth of Binary Tree (LeetCode #104)",
        "difficulty": "Easy",
        "pattern": "Post-Order Recursive DFS",
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "description": """Given the `root` of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.""",
        "starter_code": """# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
""",
        "visible_testcases": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "expected": 3},
            {"input": {"root": [1, None, 2]}, "expected": 2}
        ],
        "hidden_testcases": [
            {"input": {"root": []}, "expected": 0},
            {"input": {"root": [0]}, "expected": 1},
            {"input": {"root": [1, 2, 3, 4, None, None, 5]}, "expected": 3}
        ],
        "explanation": "Base case: depth of empty subtree is 0. Inductive step: depth of current node is $1 + \max(\text{depth}(left), \text{depth}(right))$."
    },
    {
        "id": "lc_226_invert_binary_tree",
        "module_num": 6,
        "title": "Invert Binary Tree (LeetCode #226)",
        "difficulty": "Easy",
        "pattern": "Recursive Tree Transformation",
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "description": """Given the `root` of a binary tree, invert the tree (mirroring all left and right subtrees), and return its root.""",
        "starter_code": """class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        pass
""",
        "reference_solution": """class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
""",
        "visible_testcases": [
            {"input": {"root": [4, 2, 7, 1, 3, 6, 9]}, "expected": [4, 7, 2, 9, 6, 3, 1]},
            {"input": {"root": [2, 1, 3]}, "expected": [2, 3, 1]},
            {"input": {"root": []}, "expected": []}
        ],
        "hidden_testcases": [
            {"input": {"root": [1]}, "expected": [1]},
            {"input": {"root": [1, 2]}, "expected": [1, None, 2]}
        ],
        "explanation": "Recursively invert the left and right subtrees and swap the children pointers on the root."
    },
    {
        "id": "lc_543_diameter_binary_tree",
        "module_num": 6,
        "title": "Diameter of Binary Tree (LeetCode #543)",
        "difficulty": "Easy",
        "pattern": "Bottom-Up Subtree Heights",
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "description": """Given the `root` of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.""",
        "starter_code": """class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0
        def height(node):
            nonlocal diameter
            if not node:
                return 0
            lh = height(node.left)
            rh = height(node.right)
            diameter = max(diameter, lh + rh)
            return 1 + max(lh, rh)
        height(root)
        return diameter
""",
        "visible_testcases": [
            {"input": {"root": [1, 2, 3, 4, 5]}, "expected": 3},
            {"input": {"root": [1, 2]}, "expected": 1}
        ],
        "hidden_testcases": [
            {"input": {"root": [1]}, "expected": 0},
            {"input": {"root": [2, 3, None, 1]}, "expected": 2}
        ],
        "explanation": "At any node, the longest path passing through that node is $\text{height}(\text{left}) + \text{height}(\text{right})$. Track the global maximum while returning node height bottom-up."
    },
    {
        "id": "lc_98_validate_bst",
        "module_num": 6,
        "title": "Validate Binary Search Tree (LeetCode #98)",
        "difficulty": "Medium",
        "pattern": "Range Invariant Bounding",
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "description": """Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys strictly less than the node's key.
- The right subtree of a node contains only nodes with keys strictly greater than the node's key.
- Both the left and right subtrees must also be binary search trees.""",
        "starter_code": """class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node, low=-float('inf'), high=float('inf')):
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        return validate(root)
""",
        "visible_testcases": [
            {"input": {"root": [2, 1, 3]}, "expected": True},
            {"input": {"root": [5, 1, 4, None, None, 3, 6]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"root": [2, 2, 2]}, "expected": False},
            {"input": {"root": [2147483647]}, "expected": True},
            {"input": {"root": [5, 4, 6, None, None, 3, 7]}, "expected": False}
        ],
        "explanation": "Pass lower and upper bounds $(low, high)$ into recursive calls. Going left updates the upper bound to current node value; going right updates the lower bound."
    },
    {
        "id": "lc_235_lca_bst",
        "module_num": 6,
        "title": "Lowest Common Ancestor of a BST (LeetCode #235)",
        "difficulty": "Medium",
        "pattern": "BST Value Branching",
        "time_complexity": "O(H)",
        "space_complexity": "O(1)",
        "description": """Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given values `p` and `q`.

The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants.""",
        "starter_code": """class Solution:
    def lowestCommonAncestor(self, root: Optional[TreeNode], p: int, q: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def lowestCommonAncestor(self, root: Optional[TreeNode], p: int, q: int) -> int:
        curr = root
        while curr:
            if p < curr.val and q < curr.val:
                curr = curr.left
            elif p > curr.val and q > curr.val:
                curr = curr.right
            else:
                return curr.val
        return -1
""",
        "visible_testcases": [
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 8}, "expected": 6},
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 4}, "expected": 2}
        ],
        "hidden_testcases": [
            {"input": {"root": [2, 1], "p": 2, "q": 1}, "expected": 2},
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 3, "q": 5}, "expected": 4}
        ],
        "explanation": "Take advantage of BST property: if both p and q are smaller than curr.val, LCA must be in left subtree. If both larger, right subtree. The first node where p and q split (or one equals curr.val) is the LCA."
    },
    {
        "id": "lc_124_binary_tree_max_path_sum",
        "module_num": 6,
        "title": "Binary Tree Maximum Path Sum (LeetCode #124)",
        "difficulty": "Hard",
        "pattern": "Bottom-Up Path Gain Propagation",
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "description": """A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can only appear in the sequence at most once.

Given the `root` of a binary tree, return the maximum path sum of any non-empty path.""",
        "starter_code": """class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        max_sum = -float('inf')
        def max_gain(node):
            nonlocal max_sum
            if not node:
                return 0
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)
            curr_path = node.val + left_gain + right_gain
            max_sum = max(max_sum, curr_path)
            return node.val + max(left_gain, right_gain)
        max_gain(root)
        return max_sum
""",
        "visible_testcases": [
            {"input": {"root": [1, 2, 3]}, "expected": 6},
            {"input": {"root": [-10, 9, 20, None, None, 15, 7]}, "expected": 42}
        ],
        "hidden_testcases": [
            {"input": {"root": [-3]}, "expected": -3},
            {"input": {"root": [2, -1]}, "expected": 2},
            {"input": {"root": [-2, -1]}, "expected": -1}
        ],
        "explanation": "Compute the maximum branch gain contributed by subtrees bottom-up (clamped to 0 if negative). At each node, the combined arch sum is `node.val + left_gain + right_gain`."
    }
]
