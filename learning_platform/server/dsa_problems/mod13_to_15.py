# -*- coding: utf-8 -*-
"""LeetCode problems for Modules 13, 14, and 15."""

PROBLEMS_MOD13_15 = [
    # -------------------------------------------------------------------------
    # MODULE 13: Backtracking & Constraint Satisfaction
    # -------------------------------------------------------------------------
    {
        "id": "lc_78_subsets",
        "module_num": 13,
        "title": "Subsets (LeetCode #78)",
        "difficulty": "Medium",
        "pattern": "Power Set Generation / Backtracking",
        "time_complexity": "O(N \cdot 2^N)",
        "space_complexity": "O(N)",
        "is_unordered": True,
        "description": """Given an integer array `nums` of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.""",
        "starter_code": """class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        subset = []
        def dfs(i):
            if i >= len(nums):
                res.append(subset.copy())
                return
            # decision to include nums[i]
            subset.append(nums[i])
            dfs(i + 1)
            # decision NOT to include nums[i]
            subset.pop()
            dfs(i + 1)
        dfs(0)
        return res
""",
        "visible_testcases": [
            {"input": {"nums": [1, 2, 3]}, "expected": [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]},
            {"input": {"nums": [0]}, "expected": [[], [0]]}
        ],
        "hidden_testcases": [
            {"input": {"nums": [9, 10]}, "expected": [[], [9], [10], [9, 10]]},
            {"input": {"nums": []}, "expected": [[]]}
        ],
        "explanation": "Binary decision tree: for each element at index i, branch into two decisions: include nums[i] in the current subset, or omit it."
    },
    {
        "id": "lc_39_combination_sum",
        "module_num": 13,
        "title": "Combination Sum (LeetCode #39)",
        "difficulty": "Medium",
        "pattern": "Backtracking with Unbounded Choice",
        "time_complexity": "O(2^{T/M})",
        "space_complexity": "O(T/M)",
        "is_unordered": True,
        "description": """Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of candidates where the chosen numbers sum to `target`. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times.""",
        "starter_code": """class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []
        def dfs(i, cur, total):
            if total == target:
                res.append(cur.copy())
                return
            if i >= len(candidates) or total > target:
                return
            cur.append(candidates[i])
            dfs(i, cur, total + candidates[i])
            cur.pop()
            dfs(i + 1, cur, total)
        dfs(0, [], 0)
        return res
""",
        "visible_testcases": [
            {"input": {"candidates": [2, 3, 6, 7], "target": 7}, "expected": [[2, 2, 3], [7]]},
            {"input": {"candidates": [2, 3, 5], "target": 8}, "expected": [[2, 2, 2, 2], [2, 3, 3], [3, 5]]},
            {"input": {"candidates": [2], "target": 1}, "expected": []}
        ],
        "hidden_testcases": [
            {"input": {"candidates": [1], "target": 2}, "expected": [[1, 1]]},
            {"input": {"candidates": [7, 3, 2], "target": 18}, "expected": [[2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,3,3],[2,2,2,2,3,7],[2,2,2,3,3,3,3],[2,2,7,7],[2,3,3,3,7],[3,3,3,3,3,3]]}
        ],
        "explanation": "At index i, choose to either reuse candidate[i] by adding to current sum and recurring with same i, or skip candidate[i] permanently by advancing to i+1."
    },
    {
        "id": "lc_46_permutations",
        "module_num": 13,
        "title": "Permutations (LeetCode #46)",
        "difficulty": "Medium",
        "pattern": "Backtracking / Full Ordering Search",
        "time_complexity": "O(N \cdot N!)",
        "space_complexity": "O(N)",
        "is_unordered": True,
        "description": """Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.""",
        "starter_code": """class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        res = []
        if len(nums) == 1:
            return [nums.copy()]
        for i in range(len(nums)):
            n = nums.pop(0)
            perms = self.permute(nums)
            for p in perms:
                p.append(n)
            res.extend(perms)
            nums.append(n)
        return res
""",
        "visible_testcases": [
            {"input": {"nums": [1, 2, 3]}, "expected": [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]},
            {"input": {"nums": [0, 1]}, "expected": [[0, 1], [1, 0]]},
            {"input": {"nums": [1]}, "expected": [[1]]}
        ],
        "hidden_testcases": [
            {"input": {"nums": [5, 4]}, "expected": [[5, 4], [4, 5]]}
        ],
        "explanation": "Recursively isolate the first element, permute remaining elements, and append the isolated element to each generated permutation."
    },
    {
        "id": "lc_79_word_search",
        "module_num": 13,
        "title": "Word Search (LeetCode #79)",
        "difficulty": "Medium",
        "pattern": "2D Grid DFS Backtracking with In-Place Visited Mask",
        "time_complexity": "O(M \times N \times 3^L)",
        "space_complexity": "O(L)",
        "description": """Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.
The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.""",
        "starter_code": """class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        pass
""",
        "reference_solution": """class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
                return False
            temp = board[r][c]
            board[r][c] = '#'
            found = (dfs(r + 1, c, i + 1) or
                     dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or
                     dfs(r, c - 1, i + 1))
            board[r][c] = temp
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
""",
        "visible_testcases": [
            {
                "input": {
                    "board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
                    "word": "ABCCED"
                },
                "expected": True
            },
            {
                "input": {
                    "board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
                    "word": "SEE"
                },
                "expected": True
            },
            {
                "input": {
                    "board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
                    "word": "ABCB"
                },
                "expected": False
            }
        ],
        "hidden_testcases": [
            {"input": {"board": [["a"]], "word": "a"}, "expected": True},
            {"input": {"board": [["a", "b"], ["c", "d"]], "word": "abcd"}, "expected": False}
        ],
        "explanation": "DFS explore 4 directions. Temporarily mutate board cell to '#' to mark visited, and restore original character during backtracking unwind."
    },
    {
        "id": "lc_131_palindrome_partitioning",
        "module_num": 13,
        "title": "Palindrome Partitioning (LeetCode #131)",
        "difficulty": "Medium",
        "pattern": "Backtracking Partition with Palindrome Check",
        "time_complexity": "O(N \cdot 2^N)",
        "space_complexity": "O(N)",
        "is_unordered": True,
        "description": """Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of `s`.""",
        "starter_code": """class Solution:
    def partition(self, s: str) -> list[list[str]]:
        pass
""",
        "reference_solution": """class Solution:
    def partition(self, s: str) -> list[list[str]]:
        res = []
        part = []
        def is_pali(sub):
            return sub == sub[::-1]
        def dfs(i):
            if i >= len(s):
                res.append(part.copy())
                return
            for j in range(i, len(s)):
                sub = s[i:j + 1]
                if is_pali(sub):
                    part.append(sub)
                    dfs(j + 1)
                    part.pop()
        dfs(0)
        return res
""",
        "visible_testcases": [
            {"input": {"s": "aab"}, "expected": [["a", "a", "b"], ["aa", "b"]]},
            {"input": {"s": "a"}, "expected": [["a"]]}
        ],
        "hidden_testcases": [
            {"input": {"s": "ab"}, "expected": [["a", "b"]]},
            {"input": {"s": "racecar"}, "expected": [["r","a","c","e","c","a","r"],["r","a","cec","a","r"],["r","aceca","r"],["racecar"]]}
        ],
        "explanation": "Iterate potential right partition endpoints `j`. If substring `s[i:j+1]` is a palindrome, choose it and recurse on remainder `j+1`."
    },
    {
        "id": "lc_51_n_queens",
        "module_num": 13,
        "title": "N-Queens (LeetCode #51)",
        "difficulty": "Hard",
        "pattern": "Diagonal / Anti-Diagonal Constraint Backtracking",
        "time_complexity": "O(N!)",
        "space_complexity": "O(N)",
        "is_unordered": True,
        "description": """The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.
Given an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.""",
        "starter_code": """class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        pass
""",
        "reference_solution": """class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        cols = set()
        pos_diag = set()  # (r + c)
        neg_diag = set()  # (r - c)
        res = []
        board = [["."] * n for _ in range(n)]

        def backtrack(r):
            if r == n:
                res.append(["".join(row) for row in board])
                return
            for c in range(n):
                if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                    continue
                cols.add(c)
                pos_diag.add(r + c)
                neg_diag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                cols.remove(c)
                pos_diag.remove(r + c)
                neg_diag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res
""",
        "visible_testcases": [
            {"input": {"n": 4}, "expected": [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]},
            {"input": {"n": 1}, "expected": [["Q"]]}
        ],
        "hidden_testcases": [
            {"input": {"n": 2}, "expected": []},
            {"input": {"n": 3}, "expected": []}
        ],
        "explanation": "Queens attack along columns ($c$), positive diagonals ($r + c = \text{const}$), and negative diagonals ($r - c = \text{const}$). Track blocked sets and place queens row by row."
    },

    # -------------------------------------------------------------------------
    # MODULE 14: Advanced Structures: Trie, Union-Find, Segment Tree
    # -------------------------------------------------------------------------
    {
        "id": "lc_208_implement_trie",
        "module_num": 14,
        "title": "Implement Trie (Prefix Tree) (LeetCode #208)",
        "difficulty": "Medium",
        "pattern": "Prefix Tree / Multi-Way Branching",
        "time_complexity": "O(L) per operation",
        "space_complexity": "O(N \cdot L)",
        "is_design": True,
        "target_class": "Trie",
        "description": """A trie (pronounced as 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings.
Implement the `Trie` class:
- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts the string `word` into the trie.
- `boolean search(String word)` Returns `true` if the string `word` is in the trie, and `false` otherwise.
- `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string that has the prefix `prefix`.""",
        "starter_code": """class Trie:
    def __init__(self):
        pass

    def insert(self, word: str) -> None:
        pass

    def search(self, word: str) -> bool:
        pass

    def startsWith(self, prefix: str) -> bool:
        pass
""",
        "reference_solution": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
                    "args": [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
                },
                "expected": [None, None, True, False, True, None, True]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["Trie", "insert", "search"],
                    "args": [[], ["a"], ["a"]]
                },
                "expected": [None, None, True]
            }
        ],
        "explanation": "Each node maintains a children dictionary and an `is_end` boolean. Traversal follows string characters step by step in $O(L)$ where $L$ is string length."
    },
    {
        "id": "lc_211_design_add_search_words",
        "module_num": 14,
        "title": "Design Add and Search Words Data Structure (LeetCode #211)",
        "difficulty": "Medium",
        "pattern": "Trie with Wildcard DFS Search",
        "time_complexity": "O(L) insert, O(26^L) worst search",
        "space_complexity": "O(N \cdot L)",
        "is_design": True,
        "target_class": "WordDictionary",
        "description": """Design a data structure that supports adding new words and finding if a string matches any previously added string with '.' representing any single letter.""",
        "starter_code": """class WordDictionary:
    def __init__(self):
        pass

    def addWord(self, word: str) -> None:
        pass

    def search(self, word: str) -> bool:
        pass
""",
        "reference_solution": """class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr:
                curr[c] = {}
            curr = curr[c]
        curr['#'] = True

    def search(self, word: str) -> bool:
        def dfs(idx, node):
            curr = node
            for i in range(idx, len(word)):
                c = word[i]
                if c == '.':
                    for child in curr.values():
                        if isinstance(child, dict) and dfs(i + 1, child):
                            return True
                    return False
                else:
                    if c not in curr:
                        return False
                    curr = curr[c]
            return '#' in curr
        return dfs(0, self.root)
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"],
                    "args": [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]]
                },
                "expected": [None, None, None, None, False, True, True, True]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["WordDictionary", "addWord", "search"],
                    "args": [[], ["a"], ["."]]
                },
                "expected": [None, None, True]
            }
        ],
        "explanation": "Store words in a trie dictionary. For '.', branch DFS across all child nodes in the current layer."
    },
    {
        "id": "lc_547_number_of_provinces",
        "module_num": 14,
        "title": "Number of Provinces (LeetCode #547)",
        "difficulty": "Medium",
        "pattern": "Union-Find / Disjoint Set Union (DSU)",
        "time_complexity": "O(N^2 \cdot \alpha(N))",
        "space_complexity": "O(N)",
        "description": """There are `n` cities. Some of them are connected, while some are not. If city `a` is connected directly with city `b`, and city `b` is connected directly with city `c`, then city `a` is connected indirectly with city `c`.
A province is a group of directly or indirectly connected cities.
Given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `i-th` city and the `j-th` city are directly connected, return the total number of provinces.""",
        "starter_code": """class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))
        rank = [1] * n
        components = n

        def find(p):
            while p != parent[p]:
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        def union(p1, p2):
            nonlocal components
            r1, r2 = find(p1), find(p2)
            if r1 == r2:
                return
            if rank[r1] > rank[r2]:
                parent[r2] = r1
            elif rank[r2] > rank[r1]:
                parent[r1] = r2
            else:
                parent[r2] = r1
                rank[r1] += 1
            components -= 1

        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    union(i, j)
        return components
""",
        "visible_testcases": [
            {"input": {"isConnected": [[1, 1, 0], [1, 1, 0], [0, 0, 1]]}, "expected": 2},
            {"input": {"isConnected": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}, "expected": 3}
        ],
        "hidden_testcases": [
            {"input": {"isConnected": [[1]]}, "expected": 1},
            {"input": {"isConnected": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]}, "expected": 1}
        ],
        "explanation": "Initialize n disjoint components. For every connection `isConnected[i][j] == 1`, union the two components and decrement total component count."
    },
    {
        "id": "lc_684_redundant_connection",
        "module_num": 14,
        "title": "Redundant Connection (LeetCode #684)",
        "difficulty": "Medium",
        "pattern": "Union-Find Cycle Detection",
        "time_complexity": "O(N \cdot \alpha(N))",
        "space_complexity": "O(N)",
        "description": """In this problem, a tree is an undirected graph that is connected and has no cycles.
You are given a graph that started as a tree with `n` nodes labeled from 1 to `n`, with one additional edge added. The added edge has two different vertices chosen from 1 to `n`, and was not an edge that already existed.
Return an edge that can be removed so that the resulting graph is a tree of `n` nodes.""",
        "starter_code": """class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        pass
""",
        "reference_solution": """class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        n = len(edges)
        parent = list(range(n + 1))

        def find(p):
            while p != parent[p]:
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                return [u, v]
            parent[ru] = rv
        return []
""",
        "visible_testcases": [
            {"input": {"edges": [[1, 2], [1, 3], [2, 3]]}, "expected": [2, 3]},
            {"input": {"edges": [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]}, "expected": [1, 4]}
        ],
        "hidden_testcases": [
            {"input": {"edges": [[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]}, "expected": [1, 3]}
        ],
        "explanation": "For each edge $(u, v)$, find their roots. If `find(u) == find(v)`, adding $(u, v)$ completes a cycle, meaning this is the redundant edge."
    },
    {
        "id": "lc_212_word_search_2",
        "module_num": 14,
        "title": "Word Search II (LeetCode #212)",
        "difficulty": "Hard",
        "pattern": "Trie + Grid Backtracking Pruning",
        "time_complexity": "O(M \times N \times 4^L)",
        "space_complexity": "O(\sum L)",
        "is_unordered": True,
        "description": """Given an `m x n` `board` of characters and a list of strings `words`, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring.""",
        "starter_code": """class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        pass
""",
        "reference_solution": """class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # Build Trie
        trie = {}
        for w in words:
            curr = trie
            for c in w:
                if c not in curr:
                    curr[c] = {}
                curr = curr[c]
            curr['#'] = w

        rows, cols = len(board), len(board[0])
        res = []

        def dfs(r, c, parent_node):
            ch = board[r][c]
            curr_node = parent_node[ch]

            if '#' in curr_node:
                res.append(curr_node['#'])
                del curr_node['#']  # avoid duplicates

            board[r][c] = '$'
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in curr_node:
                    dfs(nr, nc, curr_node)
            board[r][c] = ch

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in trie:
                    dfs(r, c, trie)
        return res
""",
        "visible_testcases": [
            {
                "input": {
                    "board": [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
                    "words": ["oath","pea","eat","rain"]
                },
                "expected": ["eat", "oath"]
            },
            {
                "input": {
                    "board": [["a","b"],["c","d"]],
                    "words": ["abcb"]
                },
                "expected": []
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "board": [["a"]],
                    "words": ["a"]
                },
                "expected": ["a"]
            }
        ],
        "explanation": "Store all target words in a Trie. Traverse the grid with DFS, advancing along corresponding Trie branches and immediately pruning branches when characters deviate."
    },
    {
        "id": "lc_307_range_sum_query_mutable",
        "module_num": 14,
        "title": "Range Sum Query - Mutable (LeetCode #307)",
        "difficulty": "Medium",
        "pattern": "Binary Indexed Tree (BIT) / Segment Tree",
        "time_complexity": "O(\log N) update and query",
        "space_complexity": "O(N)",
        "is_design": True,
        "target_class": "NumArray",
        "description": """Given an integer array `nums`, handle two types of queries:
1. Update the value of an element in `nums`.
2. Calculate the sum of the elements of `nums` between indices `left` and `right` inclusive.
Both operations must run in $O(\log n)$ time.""",
        "starter_code": """class NumArray:
    def __init__(self, nums: list[int]):
        pass

    def update(self, index: int, val: int) -> None:
        pass

    def sumRange(self, left: int, right: int) -> int:
        pass
""",
        "reference_solution": """class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.nums = nums[:]
        self.bit = [0] * (self.n + 1)
        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, idx, delta):
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & (-idx)

    def _prefix_sum(self, idx):
        total = 0
        while idx > 0:
            total += self.bit[idx]
            idx -= idx & (-idx)
        return total

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sum(right + 1) - self._prefix_sum(left)
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["NumArray", "sumRange", "update", "sumRange"],
                    "args": [[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
                },
                "expected": [None, 9, None, 8]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["NumArray", "sumRange"],
                    "args": [[[7]], [0, 0]]
                },
                "expected": [None, 7]
            }
        ],
        "explanation": "A Fenwick tree (Binary Indexed Tree) supports point updates and prefix sum queries in $O(\log N)$ using bit manipulation `idx & (-idx)`."
    },

    # -------------------------------------------------------------------------
    # MODULE 15: Systems-Level Structures: LRU, LFU, Circular Queue, SkipLists
    # -------------------------------------------------------------------------
    {
        "id": "lc_146_lru_cache",
        "module_num": 15,
        "title": "LRU Cache (LeetCode #146)",
        "difficulty": "Medium",
        "pattern": "Hash Map + Doubly Linked List",
        "time_complexity": "O(1) all ops",
        "space_complexity": "O(C)",
        "is_design": True,
        "target_class": "LRUCache",
        "description": """Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
Implement the `LRUCache` class:
- `LRUCache(int capacity)` Initialize the LRU cache with positive size `capacity`.
- `int get(int key)` Return the value of the `key` if the key exists, otherwise return `-1`.
- `void put(int key, int value)` Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity, evict the least recently used key.
Both functions must run in $O(1)$ average time complexity.""",
        "starter_code": """class LRUCache:
    def __init__(self, capacity: int):
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass
""",
        "reference_solution": """class DNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # key -> node
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _insert(self, node):
        prev, nxt = self.tail.prev, self.tail
        prev.next = node
        nxt.prev = node
        node.prev = prev
        node.next = nxt

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._insert(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = DNode(key, value)
        self.cache[key] = node
        self._insert(node)
        if len(self.cache) > self.cap:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
                    "args": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
                },
                "expected": [None, None, None, 1, None, -1, None, -1, 3, 4]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["LRUCache", "put", "get"],
                    "args": [[1], [2, 1], [2]]
                },
                "expected": [None, None, 1]
            }
        ],
        "explanation": "Combine a Hash Map (for $O(1)$ lookups) with a Doubly Linked List (for $O(1)$ node splicing and reordering upon read/write)."
    },
    {
        "id": "lc_460_lfu_cache",
        "module_num": 15,
        "title": "LFU Cache (LeetCode #460)",
        "difficulty": "Hard",
        "pattern": "Frequency Hash Map of Doubly Linked Lists",
        "time_complexity": "O(1) all ops",
        "space_complexity": "O(C)",
        "is_design": True,
        "target_class": "LFUCache",
        "description": """Design and implement a data structure for a Least Frequently Used (LFU) cache.
When the cache reaches its capacity, it should invalidate and remove the least frequently used key before inserting a new item. For this problem, when there is a tie (i.e., two or more keys with the same frequency), the least recently used key would be invalidated.""",
        "starter_code": """class LFUCache:
    def __init__(self, capacity: int):
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass
""",
        "reference_solution": """from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.key_val = {}
        self.key_freq = {}
        self.freq_keys = defaultdict(OrderedDict)

    def _update_freq(self, key):
        freq = self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_freq[key] = freq + 1
        self.freq_keys[freq + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_val:
            return -1
        self._update_freq(key)
        return self.key_val[key]

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return
        if key in self.key_val:
            self.key_val[key] = value
            self._update_freq(key)
            return
        if len(self.key_val) >= self.cap:
            evict_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
            del self.key_val[evict_key]
            del self.key_freq[evict_key]
        self.key_val[key] = value
        self.key_freq[key] = 1
        self.freq_keys[1][key] = None
        self.min_freq = 1
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"],
                    "args": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
                },
                "expected": [None, None, None, 1, None, -1, 3, None, -1, 3, 4]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["LFUCache", "put", "get"],
                    "args": [[0], [0, 0], [0]]
                },
                "expected": [None, None, -1]
            }
        ],
        "explanation": "Maintain `freq_keys` mapping each frequency count to an `OrderedDict` (LRU chain). Track `min_freq` to evict the lowest frequency and LRU element in $O(1)$."
    },
    {
        "id": "lc_622_design_circular_queue",
        "module_num": 15,
        "title": "Design Circular Queue (LeetCode #622)",
        "difficulty": "Medium",
        "pattern": "Ring Buffer with Modulo Indexing",
        "time_complexity": "O(1) all ops",
        "space_complexity": "O(K)",
        "is_design": True,
        "target_class": "MyCircularQueue",
        "description": """Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO principle, and the last position is connected back to the first position to make a circle.
Implement the `MyCircularQueue` class:
- `MyCircularQueue(k)` Initializes the object with the size of the queue to be `k`.
- `boolean enQueue(int value)` Inserts an element into the circular queue. Return true if the operation is successful.
- `boolean deQueue()` Deletes an element from the circular queue. Return true if the operation is successful.
- `int Front()` Gets the front item from the queue. If the queue is empty, return -1.
- `int Rear()` Gets the last item from the queue. If the queue is empty, return -1.
- `boolean isEmpty()` Checks whether the circular queue is empty or not.
- `boolean isFull()` Checks whether the circular queue is full or not.""",
        "starter_code": """class MyCircularQueue:
    def __init__(self, k: int):
        pass

    def enQueue(self, value: int) -> bool:
        pass

    def deQueue(self) -> bool:
        pass

    def Front(self) -> int:
        pass

    def Rear(self) -> int:
        pass

    def isEmpty(self) -> bool:
        pass

    def isFull(self) -> bool:
        pass
""",
        "reference_solution": """class MyCircularQueue:
    def __init__(self, k: int):
        self.k = k
        self.queue = [0] * k
        self.head = 0
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        tail = (self.head + self.count) % self.k
        self.queue[tail] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.k
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.head]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        tail = (self.head + self.count - 1) % self.k
        return self.queue[tail]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.k
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"],
                    "args": [[3], [1], [2], [3], [4], [], [], [], [4], []]
                },
                "expected": [None, True, True, True, False, 3, True, True, True, 4]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["MyCircularQueue", "Front", "Rear"],
                    "args": [[1], [], []]
                },
                "expected": [None, -1, -1]
            }
        ],
        "explanation": "Store values in a fixed-size buffer of length K. Calculate logical tail as `(head + count) % K`. All operations are strictly $O(1)$."
    },
    {
        "id": "lc_355_design_twitter",
        "module_num": 15,
        "title": "Design Twitter (LeetCode #355)",
        "difficulty": "Medium",
        "pattern": "K-Way Merge Heap + Hash Sets",
        "time_complexity": "O(K \log F) news feed",
        "space_complexity": "O(U + T)",
        "is_design": True,
        "target_class": "Twitter",
        "description": """Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and see the 10 most recent tweets in the user's news feed.
Implement the `Twitter` class:
- `Twitter()` Initializes your twitter object.
- `void postTweet(int userId, int tweetId)` Composes a new tweet with ID `tweetId` by the user `userId`.
- `List<Integer> getNewsFeed(int userId)` Retrieves the 10 most recent tweet IDs in the user's news feed.
- `void follow(int followerId, int followeeId)` The user `followerId` started following the user `followeeId`.
- `void unfollow(int followerId, int followeeId)` The user `followerId` started unfollowing the user `followeeId`.""",
        "starter_code": """class Twitter:
    def __init__(self):
        pass

    def postTweet(self, userId: int, tweetId: int) -> None:
        pass

    def getNewsFeed(self, userId: int) -> list[int]:
        pass

    def follow(self, followerId: int, followeeId: int) -> None:
        pass

    def unfollow(self, followerId: int, followeeId: int) -> None:
        pass
""",
        "reference_solution": """import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.timestamp = 0
        self.tweets = defaultdict(list)    # userId -> [(timestamp, tweetId)]
        self.following = defaultdict(set) # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.timestamp += 1
        self.tweets[userId].append((self.timestamp, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        min_heap = []
        followees = set(self.following[userId])
        followees.add(userId)

        for followee in followees:
            if followee in self.tweets and self.tweets[followee]:
                idx = len(self.tweets[followee]) - 1
                t, tw_id = self.tweets[followee][idx]
                min_heap.append((-t, tw_id, followee, idx - 1))

        heapq.heapify(min_heap)
        res = []
        while min_heap and len(res) < 10:
            neg_t, tw_id, followee, next_idx = heapq.heappop(min_heap)
            res.append(tw_id)
            if next_idx >= 0:
                t, next_tw_id = self.tweets[followee][next_idx]
                heapq.heappush(min_heap, (-t, next_tw_id, followee, next_idx - 1))
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"],
                    "args": [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
                },
                "expected": [None, None, [5], None, None, [6, 5], None, [5]]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["Twitter", "getNewsFeed"],
                    "args": [[], [1]]
                },
                "expected": [None, []]
            }
        ],
        "explanation": "Model feed aggregation as a K-way merge of sorted lists: use a max-heap keyed by timestamp across all followed users to pull the 10 newest tweets in $O(10 \log K)$."
    },
    {
        "id": "lc_706_design_hashmap",
        "module_num": 15,
        "title": "Design HashMap (LeetCode #706)",
        "difficulty": "Easy",
        "pattern": "Separate Chaining Hash Table",
        "time_complexity": "O(1) average all ops",
        "space_complexity": "O(K + N)",
        "is_design": True,
        "target_class": "MyHashMap",
        "description": """Design a HashMap without using any built-in hash table libraries.
Implement the `MyHashMap` class:
- `MyHashMap()` initializes the object with an empty map.
- `void put(int key, int value)` inserts a (key, value) pair into the HashMap. If the key already exists in the map, update the corresponding value.
- `int get(int key)` returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key.
- `void remove(key)` removes the key and its corresponding value if the map contains the mapping for the key.""",
        "starter_code": """class MyHashMap:
    def __init__(self):
        pass

    def put(self, key: int, value: int) -> None:
        pass

    def get(self, key: int) -> int:
        pass

    def remove(self, key: int) -> None:
        pass
""",
        "reference_solution": """class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: int) -> int:
        idx = self._hash(key)
        bucket = self.table[idx]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"],
                    "args": [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
                },
                "expected": [None, None, None, 1, -1, None, 1, None, -1]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["MyHashMap", "get"],
                    "args": [[], [5]]
                },
                "expected": [None, -1]
            }
        ],
        "explanation": "Use a fixed array of buckets (e.g. 1000) and modulo hashing $h = \text{key} \% 1000$. Resolve collisions via separate chaining using lists."
    },
    {
        "id": "lc_380_insert_delete_getrandom",
        "module_num": 15,
        "title": "Insert Delete GetRandom O(1) (LeetCode #380)",
        "difficulty": "Medium",
        "pattern": "Hash Map + Dynamic Array Swap",
        "time_complexity": "O(1) all ops",
        "space_complexity": "O(N)",
        "is_design": True,
        "target_class": "RandomizedSet",
        "description": """Implement the `RandomizedSet` class:
- `RandomizedSet()` Initializes the RandomizedSet object.
- `bool insert(int val)` Inserts an item `val` into the set if not present. Returns `true` if item was not present, `false` otherwise.
- `bool remove(int val)` Removes an item `val` from the set if present. Returns `true` if item was present, `false` otherwise.
- `int getRandom()` Returns a random element from the current set of elements (guaranteed that each element has same probability).
Each function must work in $O(1)$ average time complexity.""",
        "starter_code": """class RandomizedSet:
    def __init__(self):
        pass

    def insert(self, val: int) -> bool:
        pass

    def remove(self, val: int) -> bool:
        pass

    def getRandom(self) -> int:
        pass
""",
        "reference_solution": """import random

class RandomizedSet:
    def __init__(self):
        self.indices = {}
        self.elements = []

    def insert(self, val: int) -> bool:
        if val in self.indices:
            return False
        self.indices[val] = len(self.elements)
        self.elements.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.indices:
            return False
        idx = self.indices[val]
        last = self.elements[-1]
        self.elements[idx] = last
        self.indices[last] = idx
        self.elements.pop()
        del self.indices[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.elements)
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["RandomizedSet", "insert", "remove", "insert", "remove", "insert"],
                    "args": [[], [1], [2], [2], [1], [2]]
                },
                "expected": [None, True, False, True, True, False]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["RandomizedSet", "remove"],
                    "args": [[], [0]]
                },
                "expected": [None, False]
            }
        ],
        "explanation": "To remove in $O(1)$ from an array: swap the target element with the last element in the array, update the hash map index, and call `pop()` on the last position."
    }
]
