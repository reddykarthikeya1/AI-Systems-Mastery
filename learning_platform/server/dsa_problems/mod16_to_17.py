# -*- coding: utf-8 -*-
"""LeetCode problems for Modules 16 and 17."""

PROBLEMS_MOD16_17 = [
    # -------------------------------------------------------------------------
    # MODULE 16: String Algorithms & Pattern Matching
    # -------------------------------------------------------------------------
    {
        "id": "lc_28_find_first_occurrence",
        "module_num": 16,
        "title": "Find the Index of the First Occurrence in a String (LeetCode #28)",
        "difficulty": "Easy",
        "pattern": "Knuth-Morris-Pratt (KMP) / LPS Array",
        "time_complexity": "O(N + M)",
        "space_complexity": "O(M)",
        "description": """Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.""",
        "starter_code": """class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle:
            return 0
        # Build KMP LPS array
        lps = [0] * len(needle)
        prev_lps, i = 0, 1
        while i < len(needle):
            if needle[i] == needle[prev_lps]:
                lps[i] = prev_lps + 1
                prev_lps += 1
                i += 1
            elif prev_lps == 0:
                lps[i] = 0
                i += 1
            else:
                prev_lps = lps[prev_lps - 1]

        # KMP Matching
        h_idx, n_idx = 0, 0
        while h_idx < len(haystack):
            if haystack[h_idx] == needle[n_idx]:
                h_idx += 1
                n_idx += 1
            else:
                if n_idx == 0:
                    h_idx += 1
                else:
                    n_idx = lps[n_idx - 1]
            if n_idx == len(needle):
                return h_idx - len(needle)
        return -1
""",
        "visible_testcases": [
            {"input": {"haystack": "sadbutsad", "needle": "sad"}, "expected": 0},
            {"input": {"haystack": "leetcode", "needle": "leeto"}, "expected": -1}
        ],
        "hidden_testcases": [
            {"input": {"haystack": "a", "needle": "a"}, "expected": 0},
            {"input": {"haystack": "mississippi", "needle": "issip"}, "expected": 4},
            {"input": {"haystack": "hello", "needle": "ll"}, "expected": 2}
        ],
        "explanation": "KMP algorithm builds the Longest Prefix Suffix (LPS) array in $O(M)$ time and skips redundant character comparisons in haystack, matching in $O(N + M)$ total time."
    },
    {
        "id": "lc_187_repeated_dna_sequences",
        "module_num": 16,
        "title": "Repeated DNA Sequences (LeetCode #187)",
        "difficulty": "Medium",
        "pattern": "Rabin-Karp / Rolling Hash Substring",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "is_unordered": True,
        "description": """The DNA sequence is composed of a series of nucleotides abbreviated as `'A'`, `'C'`, `'G'`, and `'T'`.
Given a string `s` that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. You may return the answer in any order.""",
        "starter_code": """class Solution:
    def findRepeatedDnaSequences(self, s: str) -> list[str]:
        pass
""",
        "reference_solution": """class Solution:
    def findRepeatedDnaSequences(self, s: str) -> list[str]:
        seen = set()
        repeated = set()
        for i in range(len(s) - 9):
            sub = s[i:i + 10]
            if sub in seen:
                repeated.add(sub)
            else:
                seen.add(sub)
        return list(repeated)
""",
        "visible_testcases": [
            {"input": {"s": "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"}, "expected": ["AAAAACCCCC", "CCCCCAAAAA"]},
            {"input": {"s": "AAAAAAAAAAAAA"}, "expected": ["AAAAAAAAAA"]}
        ],
        "hidden_testcases": [
            {"input": {"s": "A"}, "expected": []},
            {"input": {"s": "AAAAAAAAAAA"}, "expected": ["AAAAAAAAAA"]}
        ],
        "explanation": "Extract length-10 substrings with sliding window. Add to `seen` set, and if already seen, record in `repeated` set."
    },
    {
        "id": "lc_1392_longest_happy_prefix",
        "module_num": 16,
        "title": "Longest Happy Prefix (LeetCode #1392)",
        "difficulty": "Hard",
        "pattern": "KMP Prefix Function (Pi-Array)",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "description": """A string is called a happy prefix if is a non-empty prefix which is also a suffix (excluding itself).
Given a string `s`, return the longest happy prefix of `s`. Return an empty string `""` if no such prefix exists.""",
        "starter_code": """class Solution:
    def longestPrefix(self, s: str) -> str:
        pass
""",
        "reference_solution": """class Solution:
    def longestPrefix(self, s: str) -> str:
        n = len(s)
        lps = [0] * n
        length = 0
        i = 1
        while i < n:
            if s[i] == s[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length > 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return s[:lps[-1]]
""",
        "visible_testcases": [
            {"input": {"s": "level"}, "expected": "l"},
            {"input": {"s": "ababab"}, "expected": "abab"}
        ],
        "hidden_testcases": [
            {"input": {"s": "a"}, "expected": ""},
            {"input": {"s": "bba"}, "expected": ""},
            {"input": {"s": "leetcode"}, "expected": ""}
        ],
        "explanation": "The length of the longest proper prefix that is also a suffix for string s is given directly by the final entry of the KMP LPS array `lps[-1]`."
    },
    {
        "id": "lc_115_distinct_subsequences",
        "module_num": 16,
        "title": "Distinct Subsequences (LeetCode #115)",
        "difficulty": "Hard",
        "pattern": "2D String Matching Dynamic Programming",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(M \times N)",
        "description": """Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.""",
        "starter_code": """class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = 1
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[i - 1] == t[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
                else:
                    dp[i][j] = dp[i - 1][j]
        return dp[m][n]
""",
        "visible_testcases": [
            {"input": {"s": "rabbbit", "t": "rabbit"}, "expected": 3},
            {"input": {"s": "babgbag", "t": "bag"}, "expected": 5}
        ],
        "hidden_testcases": [
            {"input": {"s": "a", "t": "b"}, "expected": 0},
            {"input": {"s": "a", "t": "a"}, "expected": 1}
        ],
        "explanation": "If `s[i-1] == t[j-1]`, we can either match the character ($dp[i-1][j-1]$) or skip it ($dp[i-1][j]$). If they don't match, we must skip ($dp[i-1][j]$)."
    },
    {
        "id": "lc_336_palindrome_pairs",
        "module_num": 16,
        "title": "Palindrome Pairs (LeetCode #336)",
        "difficulty": "Hard",
        "pattern": "Prefix/Suffix Partitioning with Hash Map",
        "time_complexity": "O(N \times K^2)",
        "space_complexity": "O(N \times K)",
        "is_unordered": True,
        "description": """Given a list of unique words, return all pairs of distinct indices `(i, j)` in the given list, so that the concatenation of the two words `words[i] + words[j]` is a palindrome.""",
        "starter_code": """class Solution:
    def palindromePairs(self, words: list[str]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def palindromePairs(self, words: list[str]) -> list[list[int]]:
        word_map = {w: i for i, w in enumerate(words)}
        res = []

        for i, word in enumerate(words):
            n = len(word)
            for j in range(n + 1):
                # Prefix split
                pref = word[:j]
                suff = word[j:]
                # If prefix is palindrome, reverse of suffix followed by word is palindrome
                if pref == pref[::-1]:
                    rev_suff = suff[::-1]
                    if rev_suff in word_map and word_map[rev_suff] != i:
                        res.append([word_map[rev_suff], i])
                # If suffix is palindrome, word followed by reverse of prefix is palindrome
                if j != n and suff == suff[::-1]:
                    rev_pref = pref[::-1]
                    if rev_pref in word_map and word_map[rev_pref] != i:
                        res.append([i, word_map[rev_pref]])
        return res
""",
        "visible_testcases": [
            {"input": {"words": ["abcd", "dcba", "lls", "s", "sssll"]}, "expected": [[0, 1], [1, 0], [3, 2], [2, 4]]},
            {"input": {"words": ["bat", "tab", "cat"]}, "expected": [[0, 1], [1, 0]]},
            {"input": {"words": ["a", ""]}, "expected": [[0, 1], [1, 0]]}
        ],
        "hidden_testcases": [
            {"input": {"words": ["a", "abc", "aba", ""] }, "expected": [[0, 3], [3, 0], [2, 3], [3, 2]]}
        ],
        "explanation": "Split word into prefix and suffix. If prefix is palindromic, look up reversed suffix in hash map. If suffix is palindromic, look up reversed prefix in hash map."
    },
    {
        "id": "lc_5_longest_palindromic_substring",
        "module_num": 16,
        "title": "Longest Palindromic Substring (LeetCode #5)",
        "difficulty": "Medium",
        "pattern": "Expand Around Center / Two Pointers",
        "time_complexity": "O(N^2)",
        "space_complexity": "O(1)",
        "description": """Given a string `s`, return the longest palindromic substring in `s`.""",
        "starter_code": """class Solution:
    def longestPalindrome(self, s: str) -> str:
        pass
""",
        "reference_solution": """class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ""
        res_len = 0

        for i in range(len(s)):
            # Odd length center
            l, r = i, i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > res_len:
                    res = s[l:r + 1]
                    res_len = r - l + 1
                l -= 1
                r += 1

            # Even length center
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > res_len:
                    res = s[l:r + 1]
                    res_len = r - l + 1
                l -= 1
                r += 1

        return res
""",
        "visible_testcases": [
            {"input": {"s": "babad"}, "expected": "bab"},
            {"input": {"s": "cbbd"}, "expected": "bb"}
        ],
        "hidden_testcases": [
            {"input": {"s": "a"}, "expected": "a"},
            {"input": {"s": "ac"}, "expected": "a"},
            {"input": {"s": "racecar"}, "expected": "racecar"}
        ],
        "explanation": "Every palindrome has a center: either a single character (odd length) or between two characters (even length). Expand outward from all $2N - 1$ centers."
    },

    # -------------------------------------------------------------------------
    # MODULE 17: Network Flow and Matching
    # -------------------------------------------------------------------------
    {
        "id": "lc_785_is_graph_bipartite",
        "module_num": 17,
        "title": "Is Graph Bipartite? (LeetCode #785)",
        "difficulty": "Medium",
        "pattern": "2-Coloring BFS / Odd Cycle Detection",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": """There is an undirected graph with `n` nodes, where each node is numbered between `0` and `n - 1`. You are given a 2D array `graph`, where `graph[u]` is an array of nodes that node `u` is adjacent to.
Return `True` if and only if it is bipartite.
A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge connects a node in set A and a node in set B.""",
        "starter_code": """class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        pass
""",
        "reference_solution": """from collections import deque

class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        color = {}
        for i in range(len(graph)):
            if i not in color:
                color[i] = 0
                q = deque([i])
                while q:
                    node = q.popleft()
                    for neighbor in graph[node]:
                        if neighbor not in color:
                            color[neighbor] = 1 - color[node]
                            q.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False
        return True
""",
        "visible_testcases": [
            {"input": {"graph": [[1,2,3],[0,2],[0,1,3],[0,2]]}, "expected": False},
            {"input": {"graph": [[1,3],[0,2],[1,3],[0,2]]}, "expected": True}
        ],
        "hidden_testcases": [
            {"input": {"graph": [[]]}, "expected": True},
            {"input": {"graph": [[1],[0,3],[3],[1,2]]}, "expected": True},
            {"input": {"graph": [[1,2],[0,2],[0,1]]}, "expected": False}
        ],
        "explanation": "A graph is bipartite if and only if it contains no odd-length cycles. Attempt 2-coloring with BFS: alternate colors between neighbors. If any edge connects two vertices of the same color, return False."
    },
    {
        "id": "lc_886_possible_bipartition",
        "module_num": 17,
        "title": "Possible Bipartition (LeetCode #886)",
        "difficulty": "Medium",
        "pattern": "Graph 2-Coloring Formulation",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "description": """We want to split a group of `n` people (labeled from 1 to `n`) into two groups of any size. Each person may dislike some other people.
Given the integer `n` and the array `dislikes` where `dislikes[i] = [ai, bi]`, return `True` if it is possible to split everyone into two groups in this way.""",
        "starter_code": """class Solution:
    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:
        pass
""",
        "reference_solution": """from collections import defaultdict, deque

class Solution:
    def possibleBipartition(self, n: int, dislikes: list[list[int]]) -> bool:
        adj = defaultdict(list)
        for u, v in dislikes:
            adj[u].append(v)
            adj[v].append(u)

        color = {}
        for i in range(1, n + 1):
            if i not in color:
                color[i] = 0
                q = deque([i])
                while q:
                    curr = q.popleft()
                    for nei in adj[curr]:
                        if nei not in color:
                            color[nei] = 1 - color[curr]
                            q.append(nei)
                        elif color[nei] == color[curr]:
                            return False
        return True
""",
        "visible_testcases": [
            {"input": {"n": 4, "dislikes": [[1, 2], [1, 3], [2, 4]]}, "expected": True},
            {"input": {"n": 3, "dislikes": [[1, 2], [1, 3], [2, 3]]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"n": 5, "dislikes": [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]}, "expected": False},
            {"input": {"n": 1, "dislikes": []}, "expected": True}
        ],
        "explanation": "Construct an undirected graph where dislikes are edges. The problem reduces directly to verifying whether the graph is 2-colorable (bipartite)."
    },
    {
        "id": "lc_1129_shortest_path_alternating_colors",
        "module_num": 17,
        "title": "Shortest Path with Alternating Colors (LeetCode #1129)",
        "difficulty": "Medium",
        "pattern": "Multi-Layer Flow BFS",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "description": """You are given an integer `n`, the number of nodes in a directed graph where the nodes are labeled from `0` to `n - 1`. Each edge is red or blue in this graph.
Return an array `answer` of length `n`, where each `answer[x]` is the length of the shortest path from node 0 to node x such that the edge colors alternate, or `-1` if no such path exists.""",
        "starter_code": """class Solution:
    def shortestAlternatingPaths(self, n: int, redEdges: list[list[int]], blueEdges: list[list[int]]) -> list[int]:
        pass
""",
        "reference_solution": """from collections import defaultdict, deque

class Solution:
    def shortestAlternatingPaths(self, n: int, redEdges: list[list[int]], blueEdges: list[list[int]]) -> list[int]:
        red = defaultdict(list)
        blue = defaultdict(list)
        for u, v in redEdges:
            red[u].append(v)
        for u, v in blueEdges:
            blue[u].append(v)

        # state: (node, last_color): 0 for red, 1 for blue
        ans = [-1] * n
        q = deque([(0, 0, None)])  # (node, dist, last_color)
        visited = set([(0, None)])

        while q:
            node, dist, last_col = q.popleft()
            if ans[node] == -1:
                ans[node] = dist

            if last_col != "RED":
                for nei in red[node]:
                    if (nei, "RED") not in visited:
                        visited.add((nei, "RED"))
                        q.append((nei, dist + 1, "RED"))

            if last_col != "BLUE":
                for nei in blue[node]:
                    if (nei, "BLUE") not in visited:
                        visited.add((nei, "BLUE"))
                        q.append((nei, dist + 1, "BLUE"))

        return ans
""",
        "visible_testcases": [
            {"input": {"n": 3, "redEdges": [[0, 1], [1, 2]], "blueEdges": []}, "expected": [0, 1, -1]},
            {"input": {"n": 3, "redEdges": [[0, 1]], "blueEdges": [[2, 1]]}, "expected": [0, 1, -1]}
        ],
        "hidden_testcases": [
            {"input": {"n": 1, "redEdges": [], "blueEdges": []}, "expected": [0]},
            {"input": {"n": 3, "redEdges": [[0, 1], [0, 2]], "blueEdges": [[1, 0]]}, "expected": [0, 1, 1]}
        ],
        "explanation": "Model the state graph as $(node, last\_color)$. Running BFS on this layered product graph guarantees finding the shortest alternating path to each node."
    },
    {
        "id": "lc_1489_critical_edges_mst",
        "module_num": 17,
        "title": "Find Critical and Pseudo-Critical Edges in MST (LeetCode #1489)",
        "difficulty": "Hard",
        "pattern": "MST Min-Cut Sensitivity Analysis / Kruskal's",
        "time_complexity": "O(E^2 \cdot \alpha(V))",
        "space_complexity": "O(V + E)",
        "description": """Given a weighted undirected connected graph with `n` vertices numbered from 0 to `n - 1`, and an array `edges` where `edges[i] = [fromi, toi, weighti]`.
An MST edge whose deletion increases the MST weight is called a critical edge. A pseudo-critical edge is that which can appear in some MSTs but not all.
Find all the critical and pseudo-critical edges in the given graph.""",
        "starter_code": """class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n

    def find(self, p):
        while p != self.parent[p]:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        return p

    def union(self, u, v):
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            return False
        self.parent[ru] = rv
        self.count -= 1
        return True

class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        edges_with_idx = [[u, v, w, i] for i, (u, v, w) in enumerate(edges)]
        edges_with_idx.sort(key=lambda x: x[2])

        def mst_weight(exclude_idx=-1, force_edge=None):
            uf = UnionFind(n)
            w_total = 0
            if force_edge is not None:
                uf.union(force_edge[0], force_edge[1])
                w_total += force_edge[2]
            for u, v, w, idx in edges_with_idx:
                if idx == exclude_idx:
                    continue
                if uf.union(u, v):
                    w_total += w
            return w_total if uf.count == 1 else float('inf')

        base_mst = mst_weight()
        critical = []
        pseudo = []

        for u, v, w, idx in edges_with_idx:
            # Check critical
            if mst_weight(exclude_idx=idx) > base_mst:
                critical.append(idx)
            # Check pseudo-critical
            elif mst_weight(force_edge=[u, v, w]) == base_mst:
                pseudo.append(idx)

        return [critical, pseudo]
""",
        "visible_testcases": [
            {
                "input": {
                    "n": 5,
                    "edges": [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
                },
                "expected": [[0, 1], [2, 3, 4, 5]]
            },
            {
                "input": {
                    "n": 4,
                    "edges": [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]
                },
                "expected": [[], [0, 1, 2, 3]]
            }
        ],
        "hidden_testcases": [
            {"input": {"n": 2, "edges": [[0, 1, 1]]}, "expected": [[0], []]}
        ],
        "explanation": "Compute base MST cost via Kruskal's. An edge is critical if excluding it strictly increases MST weight (or disconnects the graph). An edge is pseudo-critical if forcibly including it still produces an MST of base cost."
    },
    {
        "id": "lc_1349_max_students_taking_exam",
        "module_num": 17,
        "title": "Maximum Students Taking Exam (LeetCode #1349)",
        "difficulty": "Hard",
        "pattern": "Maximum Independent Set / Bitmask DP",
        "time_complexity": "O(M \times 2^{2N})",
        "space_complexity": "O(M \times 2^N)",
        "description": """Given a `m x n` matrix `seats` that represent seats for students, where `seats[i][j] == '.'` is available and `'#'` is broken.
Students can see the answers of those sitting directly to their left, right, upper-left, and upper-right. Return the maximum number of students that can take the exam together without any student cheating.""",
        "starter_code": """class Solution:
    def maxStudents(self, seats: list[list[str]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxStudents(self, seats: list[list[str]]) -> int:
        m, n = len(seats), len(seats[0])
        valid_masks = []
        for r in range(m):
            mask = 0
            for c in range(n):
                if seats[r][c] == '.':
                    mask |= (1 << c)
            valid_masks.append(mask)

        memo = {}
        def dp(r, prev_mask):
            if r == m:
                return 0
            state = (r, prev_mask)
            if state in memo:
                return memo[state]
            max_s = 0
            # Iterate all subsets of valid seats in current row
            row_mask = valid_masks[r]
            sub = row_mask
            while True:
                # Check no adjacent students in row
                if (sub & (sub >> 1)) == 0:
                    # Check diagonal conflicts with previous row
                    if (sub & (prev_mask >> 1)) == 0 and (sub & (prev_mask << 1)) == 0:
                        count = bin(sub).count('1')
                        max_s = max(max_s, count + dp(r + 1, sub))
                if sub == 0:
                    break
                sub = (sub - 1) & row_mask
            memo[state] = max_s
            return max_s

        return dp(0, 0)
""",
        "visible_testcases": [
            {
                "input": {
                    "seats": [
                        ["#",".","#","#",".","#"],
                        [".","#","#","#","#","."],
                        ["#",".","#","#",".","#"]
                    ]
                },
                "expected": 4
            },
            {
                "input": {
                    "seats": [
                        [".","#"],
                        ["#","#"],
                        ["#","."],
                        ["#","#"],
                        [".","#"]
                    ]
                },
                "expected": 3
            }
        ],
        "hidden_testcases": [
            {"input": {"seats": [["#"]]}, "expected": 0},
            {"input": {"seats": [["."]]}, "expected": 1}
        ],
        "explanation": "Since students cannot see adjacent or diagonal neighbors, this is equivalent to Maximum Independent Set on a Bipartite / Row-layered graph. Solved via Bitmask Dynamic Programming."
    },
    {
        "id": "lc_1066_campus_bikes_2",
        "module_num": 17,
        "title": "Campus Bikes II (LeetCode #1066)",
        "difficulty": "Medium",
        "pattern": "Bipartite Min-Cost Matching / Bitmask DP",
        "time_complexity": "O(W \times 2^B)",
        "space_complexity": "O(2^B)",
        "description": """On a campus represented by a 2D grid, there are `n` workers and `m` bikes, with `n <= m`.
Assign each worker to a unique bike such that the sum of the Manhattan distances between each worker and their assigned bike is minimized. Return the minimum possible sum of Manhattan distances.""",
        "starter_code": """class Solution:
    def assignBikes(self, workers: list[list[int]], bikes: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def assignBikes(self, workers: list[list[int]], bikes: list[list[int]]) -> int:
        n, m = len(workers), len(bikes)
        memo = {}

        def dp(w_idx, bike_mask):
            if w_idx == n:
                return 0
            state = (w_idx, bike_mask)
            if state in memo:
                return memo[state]
            min_dist = float('inf')
            wx, wy = workers[w_idx]
            for b in range(m):
                if not (bike_mask & (1 << b)):
                    d = abs(wx - bikes[b][0]) + abs(wy - bikes[b][1])
                    min_dist = min(min_dist, d + dp(w_idx + 1, bike_mask | (1 << b)))
            memo[state] = min_dist
            return min_dist

        return dp(0, 0)
""",
        "visible_testcases": [
            {
                "input": {
                    "workers": [[0,0],[2,1]],
                    "bikes": [[1,2],[3,3]]
                },
                "expected": 6
            },
            {
                "input": {
                    "workers": [[0,0],[1,1],[2,0]],
                    "bikes": [[1,0],[2,2],[2,1]]
                },
                "expected": 4
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "workers": [[0,0]],
                    "bikes": [[1000,1000]]
                },
                "expected": 2000
            }
        ],
        "explanation": "Weighted bipartite matching can be solved via Min-Cost Max-Flow (Hungarian Algorithm) or Bitmask Dynamic Programming where bitmask tracks assigned bikes."
    }
]
