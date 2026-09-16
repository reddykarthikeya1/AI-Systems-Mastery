# -*- coding: utf-8 -*-
"""LeetCode problems for Modules 07, 08, and 09."""

PROBLEMS_MOD07_09 = [
    # -------------------------------------------------------------------------
    # MODULE 07: Heaps, Priority Queues & TopK Patterns
    # -------------------------------------------------------------------------
    {
        "id": "lc_703_kth_largest_stream",
        "module_num": 7,
        "title": "Kth Largest Element in a Stream (LeetCode #703)",
        "difficulty": "Easy",
        "pattern": "Size-K Min-Heap",
        "time_complexity": "O(\log K) per add",
        "space_complexity": "O(K)",
        "is_design": True,
        "target_class": "KthLargest",
        "description": """Design a class to find the `k-th` largest element in a stream. Note that it is the `k-th` largest element in the sorted order, not the `k-th` distinct element.

Implement `KthLargest` class:
- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)` Appends the integer `val` to the stream and returns the element representing the `k-th` largest element in the stream.""",
        "starter_code": """class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        pass

    def add(self, val: int) -> int:
        pass
""",
        "reference_solution": """import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["KthLargest", "add", "add", "add", "add", "add"],
                    "args": [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
                },
                "expected": [None, 4, 5, 5, 8, 8]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["KthLargest", "add", "add"],
                    "args": [[1, []], [-3], [-2]]
                },
                "expected": [None, -3, -2]
            }
        ],
        "explanation": "Maintain a min-heap of size k. The root of the min-heap is always the k-th largest element seen so far. Each add takes $O(\log K)$."
    },
    {
        "id": "lc_1046_last_stone_weight",
        "module_num": 7,
        "title": "Last Stone Weight (LeetCode #1046)",
        "difficulty": "Easy",
        "pattern": "Max-Heap Simulation",
        "time_complexity": "O(N \log N)",
        "space_complexity": "O(N)",
        "description": """You are given an array of integers `stones` where `stones[i]` is the weight of the `i-th` stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones with weights `x` and `y` with `x <= y`. The result of this smash is:
- If `x == y`, both stones are destroyed.
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

At the end of the game, there is at most one stone left. Return the weight of the last remaining stone. If there are no stones left, return `0`.""",
        "starter_code": """class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        pass
""",
        "reference_solution": """import heapq

class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        max_heap = [-s for s in stones]
        heapq.heapify(max_heap)
        while len(max_heap) > 1:
            first = -heapq.heappop(max_heap)
            second = -heapq.heappop(max_heap)
            if first != second:
                heapq.heappush(max_heap, -(first - second))
        return -max_heap[0] if max_heap else 0
""",
        "visible_testcases": [
            {"input": {"stones": [2, 7, 4, 1, 8, 1]}, "expected": 1},
            {"input": {"stones": [1]}, "expected": 1}
        ],
        "hidden_testcases": [
            {"input": {"stones": [2, 2]}, "expected": 0},
            {"input": {"stones": [9, 3, 2, 10]}, "expected": 0}
        ],
        "explanation": "Simulate max-heap by negating values in Python's heapq. Repeatedly pop the two largest stones and push the difference back if non-zero."
    },
    {
        "id": "lc_973_k_closest_points",
        "module_num": 7,
        "title": "K Closest Points to Origin (LeetCode #973)",
        "difficulty": "Medium",
        "pattern": "Max-Heap of Size K / Euclidean Distance",
        "time_complexity": "O(N \log K)",
        "space_complexity": "O(K)",
        "is_unordered": True,
        "description": """Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

The distance between two points on the X-Y plane is Euclidean distance: $\sqrt{x^2 + y^2}$. You may return the answer in any order.""",
        "starter_code": """class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        pass
""",
        "reference_solution": """import heapq

class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        max_heap = []
        for x, y in points:
            dist = -(x * x + y * y)
            if len(max_heap) < k:
                heapq.heappush(max_heap, (dist, [x, y]))
            else:
                heapq.heappushpop(max_heap, (dist, [x, y]))
        return [pt for _, pt in max_heap]
""",
        "visible_testcases": [
            {"input": {"points": [[1, 3], [-2, 2]], "k": 1}, "expected": [[-2, 2]]},
            {"input": {"points": [[3, 3], [5, -1], [-2, 4]], "k": 2}, "expected": [[3, 3], [-2, 4]]}
        ],
        "hidden_testcases": [
            {"input": {"points": [[0, 1], [1, 0]], "k": 2}, "expected": [[0, 1], [1, 0]]},
            {"input": {"points": [[1, 1]], "k": 1}, "expected": [[1, 1]]}
        ],
        "explanation": "Maintain a max-heap of size K using negative squared distances. Points farther away than the current K closest are automatically evicted."
    },
    {
        "id": "lc_621_task_scheduler",
        "module_num": 7,
        "title": "Task Scheduler (LeetCode #621)",
        "difficulty": "Medium",
        "pattern": "Greedy Max-Heap with Cooldown Queue",
        "time_complexity": "O(N)",
        "space_complexity": "O(1) (26 tasks)",
        "description": """Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer `n` that represents the cooldown period between two same tasks (the same task must be separated by at least `n` units of time).

Return the least number of units of times that the CPU will take to finish all the given tasks.""",
        "starter_code": """class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        pass
""",
        "reference_solution": """from collections import Counter

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        max_freq = max(counts.values())
        max_count = sum(1 for c, v in counts.items() if v == max_freq)
        empty_slots = (max_freq - 1) * (n - (max_count - 1))
        available_tasks = len(tasks) - max_freq * max_count
        idles = max(0, empty_slots - available_tasks)
        return len(tasks) + idles
""",
        "visible_testcases": [
            {"input": {"tasks": ["A", "A", "A", "B", "B", "B"], "n": 2}, "expected": 8},
            {"input": {"tasks": ["A", "A", "A", "B", "B", "B"], "n": 0}, "expected": 6},
            {"input": {"tasks": ["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], "n": 2}, "expected": 16}
        ],
        "hidden_testcases": [
            {"input": {"tasks": ["A"], "n": 2}, "expected": 1},
            {"input": {"tasks": ["A", "B", "C"], "n": 2}, "expected": 3}
        ],
        "explanation": "The bottleneck is dictated by the task(s) with the maximum frequency $M$. There are $M - 1$ frame blocks of size $n+1$, plus the final row of size $K$ (where $K$ is the number of tasks sharing max frequency)."
    },
    {
        "id": "lc_295_find_median_data_stream",
        "module_num": 7,
        "title": "Find Median from Data Stream (LeetCode #295)",
        "difficulty": "Hard",
        "pattern": "Dual Balancing Heaps (Min/Max)",
        "time_complexity": "O(\log N) add, O(1) find",
        "space_complexity": "O(N)",
        "is_design": True,
        "target_class": "MedianFinder",
        "description": """The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

Implement the `MedianFinder` class:
- `MedianFinder()` initializes the MedianFinder object.
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far.""",
        "starter_code": """class MedianFinder:
    def __init__(self):
        pass

    def addNum(self, num: int) -> None:
        pass

    def findMedian(self) -> float:
        pass
""",
        "reference_solution": """import heapq

class MedianFinder:
    def __init__(self):
        # small: max_heap (invert numbers)
        # large: min_heap
        self.small = []
        self.large = []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # ensure every in small <= every in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        # balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
""",
        "visible_testcases": [
            {
                "input": {
                    "commands": ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
                    "args": [[], [1], [2], [], [3], []]
                },
                "expected": [None, None, None, 1.5, None, 2.0]
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "commands": ["MedianFinder", "addNum", "findMedian"],
                    "args": [[], [-1], []]
                },
                "expected": [None, None, -1.0]
            }
        ],
        "explanation": "Maintain two heaps: a max-heap `small` for the lower half of numbers, and a min-heap `large` for the upper half. Keep heaps balanced such that `len(small) == len(large)` or `len(small) == len(large) + 1`."
    },
    {
        "id": "lc_215_kth_largest_element",
        "module_num": 7,
        "title": "Kth Largest Element in an Array (LeetCode #215)",
        "difficulty": "Medium",
        "pattern": "Min-Heap of Size K / Quickselect",
        "time_complexity": "O(N \log K)",
        "space_complexity": "O(K)",
        "description": """Given an integer array `nums` and an integer `k`, return the `k-th` largest element in the array.

Note that it is the `k-th` largest element in the sorted order, not the `k-th` distinct element. Can you solve it without sorting?""",
        "starter_code": """class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        pass
""",
        "reference_solution": """import heapq

class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        heap = []
        for x in nums:
            heapq.heappush(heap, x)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]
""",
        "visible_testcases": [
            {"input": {"nums": [3, 2, 1, 5, 6, 4], "k": 2}, "expected": 5},
            {"input": {"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6], "k": 4}, "expected": 4}
        ],
        "hidden_testcases": [
            {"input": {"nums": [1], "k": 1}, "expected": 1},
            {"input": {"nums": [-1, 2, 0], "k": 2}, "expected": 0}
        ],
        "explanation": "Feed elements into a min-heap of maximum size K. When size exceeds K, pop the smallest. After scanning all elements, the root of the heap holds the Kth largest."
    },

    # -------------------------------------------------------------------------
    # MODULE 08: Graph Algorithms: Traversals and DAGs
    # -------------------------------------------------------------------------
    {
        "id": "lc_200_number_of_islands",
        "module_num": 8,
        "title": "Number of Islands (LeetCode #200)",
        "difficulty": "Medium",
        "pattern": "Connected Components / BFS / DFS Flood Fill",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(M \times N)",
        "description": """Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.""",
        "starter_code": """class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        count = 0
        def dfs(r, c):
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
                return
            grid[r][c] = '0'  # mark visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(m):
            for c in range(n):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count
""",
        "visible_testcases": [
            {
                "input": {
                    "grid": [
                        ["1","1","1","1","0"],
                        ["1","1","0","1","0"],
                        ["1","1","0","0","0"],
                        ["0","0","0","0","0"]
                    ]
                },
                "expected": 1
            },
            {
                "input": {
                    "grid": [
                        ["1","1","0","0","0"],
                        ["1","1","0","0","0"],
                        ["0","0","1","0","0"],
                        ["0","0","0","1","1"]
                    ]
                },
                "expected": 3
            }
        ],
        "hidden_testcases": [
            {"input": {"grid": [["1"]]}, "expected": 1},
            {"input": {"grid": [["0"]]}, "expected": 0},
            {"input": {"grid": [["1","0"],["0","1"]]}, "expected": 2}
        ],
        "explanation": "Iterate through each cell. When an unvisited land cell '1' is found, increment island count and execute DFS/BFS to sink all 4-directionally connected land cells to '0'."
    },
    {
        "id": "lc_695_max_area_island",
        "module_num": 8,
        "title": "Max Area of Island (LeetCode #695)",
        "difficulty": "Medium",
        "pattern": "Recursive Flood Fill Area Accumulation",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(M \times N)",
        "description": """You are given an `m x n` binary matrix `grid`. An island is a group of `1`'s (representing land) connected 4-directionally. You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value `1` in the island. Return the maximum area of an island in `grid`. If there is no island, return `0`.""",
        "starter_code": """class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def dfs(r, c):
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != 1:
                return 0
            grid[r][c] = 0
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

        max_area = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    max_area = max(max_area, dfs(r, c))
        return max_area
""",
        "visible_testcases": [
            {
                "input": {
                    "grid": [
                        [0,0,1,0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,0,0,0,1,1,1,0,0,0],
                        [0,1,1,0,1,0,0,0,0,0,0,0,0],
                        [0,1,0,0,1,1,0,0,1,0,1,0,0],
                        [0,1,0,0,1,1,0,0,1,1,1,0,0],
                        [0,0,0,0,0,0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,0,0,1,1,1,0,0,0],
                        [0,0,0,0,0,0,0,1,1,0,0,0,0]
                    ]
                },
                "expected": 6
            },
            {"input": {"grid": [[0, 0, 0, 0, 0]]}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"grid": [[1, 1], [1, 1]]}, "expected": 4},
            {"input": {"grid": [[1]]}, "expected": 1}
        ],
        "explanation": "DFS returns 1 + sum of areas of neighbors, while sinking visited cells to 0 to prevent re-traversal."
    },
    {
        "id": "lc_133_clone_graph",
        "module_num": 8,
        "title": "Clone Graph (LeetCode #133)",
        "difficulty": "Medium",
        "pattern": "DFS / BFS with Hash Map Memoization",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": """Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.

Represented as adjacency list where `adjList[i]` is a list of neighbors of the `i-th` node (1-indexed).""",
        "starter_code": """class Solution:
    def cloneGraph(self, adjList: list[list[int]]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def cloneGraph(self, adjList: list[list[int]]) -> list[list[int]]:
        if not adjList:
            return []
        # Return cloned adjacency list
        return [list(neighbors) for neighbors in adjList]
""",
        "visible_testcases": [
            {"input": {"adjList": [[2, 4], [1, 3], [2, 4], [1, 3]]}, "expected": [[2, 4], [1, 3], [2, 4], [1, 3]]},
            {"input": {"adjList": [[]]}, "expected": [[]]},
            {"input": {"adjList": []}, "expected": []}
        ],
        "hidden_testcases": [
            {"input": {"adjList": [[2], [1]]}, "expected": [[2], [1]]}
        ],
        "explanation": "Use a hash map mapping original nodes to cloned nodes. Traverse recursively (DFS); if a neighbor is already in the map, attach the existing clone, preventing infinite cycles in cyclic graphs."
    },
    {
        "id": "lc_417_pacific_atlantic",
        "module_num": 8,
        "title": "Pacific Atlantic Water Flow (LeetCode #417)",
        "difficulty": "Medium",
        "pattern": "Reverse Multi-Source BFS/DFS from Boundaries",
        "time_complexity": "O(M \times N)",
        "space_complexity": "O(M \times N)",
        "is_unordered": True,
        "description": """There is an `m x n` rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.

Water can flow from a cell to an adjacent cell if the adjacent cell's height is less than or equal to the current cell's height. Return a 2D list of grid coordinates where rain water can flow to both oceans.""",
        "starter_code": """class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        pass
""",
        "reference_solution": """class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        if not heights:
            return []
        m, n = len(heights), len(heights[0])
        pac = set()
        atl = set()

        def dfs(r, c, visit, prev_height):
            if ((r, c) in visit or r < 0 or c < 0 or r >= m or c >= n or heights[r][c] < prev_height):
                return
            visit.add((r, c))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(r + dr, c + dc, visit, heights[r][c])

        for c in range(n):
            dfs(0, c, pac, heights[0][c])
            dfs(m - 1, c, atl, heights[m - 1][c])
        for r in range(m):
            dfs(r, 0, pac, heights[r][0])
            dfs(r, n - 1, atl, heights[r][n - 1])

        return [[r, c] for r, c in (pac & atl)]
""",
        "visible_testcases": [
            {
                "input": {
                    "heights": [
                        [1,2,2,3,5],
                        [3,2,3,4,4],
                        [2,4,5,3,1],
                        [6,7,1,4,5],
                        [5,1,1,2,4]
                    ]
                },
                "expected": [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
            },
            {"input": {"heights": [[1]]}, "expected": [[0, 0]]}
        ],
        "hidden_testcases": [
            {"input": {"heights": [[2, 1], [1, 2]]}, "expected": [[0, 0], [0, 1], [1, 0], [1, 1]]}
        ],
        "explanation": "Reverse problem: Start from Pacific edges and Atlantic edges, flowing 'uphill' (next height >= current height). The intersection of cells reachable from both oceans yields the answer."
    },
    {
        "id": "lc_207_course_schedule",
        "module_num": 8,
        "title": "Course Schedule (LeetCode #207)",
        "difficulty": "Medium",
        "pattern": "Kahn's Topological Sort / In-Degree BFS",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "description": """There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you must take course `bi` first if you want to take course `ai`.

Return `true` if you can finish all courses. Otherwise, return `false`.""",
        "starter_code": """class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        pass
""",
        "reference_solution": """from collections import deque, defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        adj = defaultdict(list)
        in_degree = [0] * numCourses
        for course, prereq in prerequisites:
            adj[prereq].append(course)
            in_degree[course] += 1

        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        visited = 0
        while queue:
            node = queue.popleft()
            visited += 1
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return visited == numCourses
""",
        "visible_testcases": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected": True},
            {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected": False}
        ],
        "hidden_testcases": [
            {"input": {"numCourses": 1, "prerequisites": []}, "expected": True},
            {"input": {"numCourses": 3, "prerequisites": [[0, 1], [0, 2], [1, 2]]}, "expected": True},
            {"input": {"numCourses": 4, "prerequisites": [[2, 0], [1, 0], [3, 1], [3, 2], [1, 3]]}, "expected": False}
        ],
        "explanation": "Kahn's algorithm: Count in-degrees. Enqueue all nodes with in_degree == 0. While processing, decrement neighbor in-degrees. If total visited nodes equals numCourses, graph is a DAG (no cycle)."
    },
    {
        "id": "lc_127_word_ladder",
        "module_num": 8,
        "title": "Word Ladder (LeetCode #127)",
        "difficulty": "Hard",
        "pattern": "BFS Shortest Transformation Sequence",
        "time_complexity": "O(M^2 \times N)",
        "space_complexity": "O(M^2 \times N)",
        "description": """A transformation sequence from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:
- Every adjacent pair of words differs by a single letter.
- Every `si` for $1 \le i \le k$ is in `wordList`. Note that `beginWord` does not need to be in `wordList`.
- $sk == \text{endWord}$.

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence, or `0` if no such sequence exists.""",
        "starter_code": """class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        pass
""",
        "reference_solution": """from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            word, steps = queue.popleft()
            if word == endWord:
                return steps
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]
                    if next_word in words and next_word not in visited:
                        visited.add(next_word)
                        queue.append((next_word, steps + 1))
        return 0
""",
        "visible_testcases": [
            {
                "input": {
                    "beginWord": "hit",
                    "endWord": "cog",
                    "wordList": ["hot", "dot", "dog", "lot", "log", "cog"]
                },
                "expected": 5
            },
            {
                "input": {
                    "beginWord": "hit",
                    "endWord": "cog",
                    "wordList": ["hot", "dot", "dog", "lot", "log"]
                },
                "expected": 0
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "beginWord": "a",
                    "endWord": "c",
                    "wordList": ["a", "b", "c"]
                },
                "expected": 2
            }
        ],
        "explanation": "BFS guarantees finding the shortest path first in an unweighted graph where edges represent a 1-character difference."
    },

    # -------------------------------------------------------------------------
    # MODULE 09: Graph Algorithms: Shortest Paths and MST
    # -------------------------------------------------------------------------
    {
        "id": "lc_743_network_delay_time",
        "module_num": 9,
        "title": "Network Delay Time (LeetCode #743)",
        "difficulty": "Medium",
        "pattern": "Dijkstra's Single-Source Shortest Path",
        "time_complexity": "O(E \log V)",
        "space_complexity": "O(V + E)",
        "description": """You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the source node, `vi` is the target node, and `wi` is the time it takes for a signal to travel from source to target.

We will send a signal from a given node `k`. Return the minimum time it takes for all the `n` nodes to receive the signal. If it is impossible for all the `n` nodes to receive the signal, return `-1`.""",
        "starter_code": """class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        pass
""",
        "reference_solution": """import heapq
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        pq = [(0, k)]
        dist = {}
        while pq:
            d, node = heapq.heappop(pq)
            if node in dist:
                continue
            dist[node] = d
            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(pq, (d + weight, neighbor))
        return max(dist.values()) if len(dist) == n else -1
""",
        "visible_testcases": [
            {"input": {"times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]], "n": 4, "k": 2}, "expected": 2},
            {"input": {"times": [[1, 2, 1]], "n": 2, "k": 1}, "expected": 1},
            {"input": {"times": [[1, 2, 1]], "n": 2, "k": 2}, "expected": -1}
        ],
        "hidden_testcases": [
            {"input": {"times": [[1, 2, 1], [2, 3, 2], [1, 3, 4]], "n": 3, "k": 1}, "expected": 3},
            {"input": {"times": [[1, 2, 1], [2, 1, 3]], "n": 2, "k": 2}, "expected": 3}
        ],
        "explanation": "Classic Dijkstra's algorithm with a min-priority queue. The answer is $\max(\text{dist}[v])$ across all nodes once all have been settled."
    },
    {
        "id": "lc_787_cheapest_flights_k_stops",
        "module_num": 9,
        "title": "Cheapest Flights Within K Stops (LeetCode #787)",
        "difficulty": "Medium",
        "pattern": "Bellman-Ford / BFS Step-Bounded Relaxation",
        "time_complexity": "O(K \times E)",
        "space_complexity": "O(V)",
        "description": """There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [fromi, toi, pricei]` indicates that there is a flight from city `fromi` to city `toi` with cost `pricei`.

You are also given three integers `src`, `dst`, and `k`, return the cheapest price from `src` to `dst` with at most `k` stops. If there is no such route, return `-1`.""",
        "starter_code": """class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        prices = [float('inf')] * n
        prices[src] = 0
        for _ in range(k + 1):
            tmp_prices = prices.copy()
            for u, v, w in flights:
                if prices[u] == float('inf'):
                    continue
                if prices[u] + w < tmp_prices[v]:
                    tmp_prices[v] = prices[u] + w
            prices = tmp_prices
        return prices[dst] if prices[dst] != float('inf') else -1
""",
        "visible_testcases": [
            {
                "input": {
                    "n": 4,
                    "flights": [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],
                    "src": 0, "dst": 3, "k": 1
                },
                "expected": 700
            },
            {
                "input": {
                    "n": 3,
                    "flights": [[0,1,100],[1,2,100],[0,2,500]],
                    "src": 0, "dst": 2, "k": 1
                },
                "expected": 200
            }
        ],
        "hidden_testcases": [
            {
                "input": {
                    "n": 3,
                    "flights": [[0,1,100],[1,2,100],[0,2,500]],
                    "src": 0, "dst": 2, "k": 0
                },
                "expected": 500
            }
        ],
        "explanation": "Bellman-Ford relaxation executed exactly $K + 1$ rounds. Using a cloned copy `tmp_prices` prevents using flights from the same iteration (which would count as multiple stops)."
    },
    {
        "id": "lc_1584_min_cost_connect_points",
        "module_num": 9,
        "title": "Min Cost to Connect All Points (LeetCode #1584)",
        "difficulty": "Medium",
        "pattern": "Prim's Algorithm / Minimum Spanning Tree (MST)",
        "time_complexity": "O(N^2)",
        "space_complexity": "O(N)",
        "description": """You are given an array `points` representing integer coordinates of some points on a 2D-plane, where `points[i] = [xi, yi]`.

The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the Manhattan distance between them: $|xi - xj| + |yi - yj|$.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.""",
        "starter_code": """class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """import heapq

class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)
        visited = set()
        min_heap = [(0, 0)]  # (cost, point_idx)
        total_cost = 0
        while len(visited) < n:
            cost, u = heapq.heappop(min_heap)
            if u in visited:
                continue
            visited.add(u)
            total_cost += cost
            x1, y1 = points[u]
            for v in range(n):
                if v not in visited:
                    x2, y2 = points[v]
                    dist = abs(x1 - x2) + abs(y1 - y2)
                    heapq.heappush(min_heap, (dist, v))
        return total_cost
""",
        "visible_testcases": [
            {"input": {"points": [[0,0],[2,2],[3,10],[5,2],[7,0]]}, "expected": 20},
            {"input": {"points": [[3,12],[-2,5],[-4,1]]}, "expected": 18}
        ],
        "hidden_testcases": [
            {"input": {"points": [[0, 0]]}, "expected": 0},
            {"input": {"points": [[0, 0], [1, 1], [1, 0], [-1, 1]]}, "expected": 4}
        ],
        "explanation": "Prim's algorithm builds an MST by greedily adding the lowest-cost edge connecting an unvisited vertex to the growing connected tree component."
    },
    {
        "id": "lc_1631_path_min_effort",
        "module_num": 9,
        "title": "Path With Minimum Effort (LeetCode #1631)",
        "difficulty": "Medium",
        "pattern": "Minimax Path / Modified Dijkstra",
        "time_complexity": "O(M \times N \log(M \times N))",
        "space_complexity": "O(M \times N)",
        "description": """You are a hiker preparing for an upcoming hike. You are given `heights`, a 2D array of size `rows x columns`, where `heights[row][col]` represents the height of cell `(row, col)`.
A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.
Return the minimum effort required to travel from the top-left cell `(0, 0)` to the bottom-right cell `(rows - 1, columns - 1)`.""",
        "starter_code": """class Solution:
    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """import heapq

class Solution:
    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        pq = [(0, 0, 0)]  # (effort, r, c)
        dist = [[float('inf')] * cols for _ in range(rows)]
        dist[0][0] = 0
        while pq:
            effort, r, c = heapq.heappop(pq)
            if r == rows - 1 and c == cols - 1:
                return effort
            if effort > dist[r][c]:
                continue
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_effort = max(effort, abs(heights[r][c] - heights[nr][nc]))
                    if new_effort < dist[nr][nc]:
                        dist[nr][nc] = new_effort
                        heapq.heappush(pq, (new_effort, nr, nc))
        return 0
""",
        "visible_testcases": [
            {"input": {"heights": [[1,2,2],[3,8,2],[5,3,5]]}, "expected": 2},
            {"input": {"heights": [[1,2,3],[3,8,4],[5,3,5]]}, "expected": 1},
            {"input": {"heights": [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]}, "expected": 0}
        ],
        "hidden_testcases": [
            {"input": {"heights": [[3]]}, "expected": 0},
            {"input": {"heights": [[1, 10, 6, 7, 9, 10, 4, 9, 9, 8, 4]]}, "expected": 9}
        ],
        "explanation": "Modify Dijkstra's distance update rule from addition to minimax: $\text{new\_effort} = \max(\text{effort}, |h_{curr} - h_{next}|)$."
    },
    {
        "id": "lc_778_swim_in_rising_water",
        "module_num": 9,
        "title": "Swim in Rising Water (LeetCode #778)",
        "difficulty": "Hard",
        "pattern": "Minimax Dijkstra on Grid",
        "time_complexity": "O(N^2 \log N)",
        "space_complexity": "O(N^2)",
        "description": """You are given an `n x n` integer matrix `grid` where each value `grid[i][j]` represents the elevation at that point `(i, j)`.

The rain starts to fall at time `t = 0`. At time `t`, the depth of the water everywhere is `t`. You can swim from a square to any 4-directionally adjacent square if and only if the elevation of both squares is at most `t`.

Return the least time until you can reach the bottom right square `(n - 1, n - 1)` if you start at the top left square `(0, 0)`.""",
        "starter_code": """class Solution:
    def swimInWater(self, grid: list[list[int]]) -> int:
        pass
""",
        "reference_solution": """import heapq

class Solution:
    def swimInWater(self, grid: list[list[int]]) -> int:
        n = len(grid)
        visited = set([(0, 0)])
        pq = [(grid[0][0], 0, 0)]
        while pq:
            t, r, c = heapq.heappop(pq)
            if r == n - 1 and c == n - 1:
                return t
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))
        return 0
""",
        "visible_testcases": [
            {"input": {"grid": [[0, 2], [1, 3]]}, "expected": 3},
            {
                "input": {
                    "grid": [
                        [0,1,2,3,4],
                        [24,23,22,21,5],
                        [12,13,14,15,16],
                        [11,17,18,19,20],
                        [10,9,8,7,6]
                    ]
                },
                "expected": 16
            }
        ],
        "hidden_testcases": [
            {"input": {"grid": [[3]]}, "expected": 3},
            {"input": {"grid": [[10, 12], [4, 5]]}, "expected": 10}
        ],
        "explanation": "Dijkstra using max elevation on path: `max(current_t, grid[nr][nc])`. The first time the destination is popped from the priority queue, its time is guaranteed to be minimal."
    },
    {
        "id": "lc_1334_city_smallest_neighbors",
        "module_num": 9,
        "title": "Find City With Smallest Neighbors at Threshold (LeetCode #1334)",
        "difficulty": "Medium",
        "pattern": "Floyd-Warshall All-Pairs Shortest Path",
        "time_complexity": "O(N^3)",
        "space_complexity": "O(N^2)",
        "description": """There are `n` cities numbered from `0` to `n-1`. Given the array `edges` where `edges[i] = [fromi, toi, weighti]` represents a bidirectional and weighted edge between cities `fromi` and `toi`, and given the integer `distanceThreshold`.

Return the city with the smallest number of cities that are reachable through some path and whose distance is at most `distanceThreshold`. If there are multiple such cities, return the city with the greatest number.""",
        "starter_code": """class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        pass
""",
        "reference_solution": """class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = w
            dist[v][u] = w

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        min_reachable = float('inf')
        best_city = -1
        for i in range(n):
            reachable = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if reachable <= min_reachable:
                min_reachable = reachable
                best_city = i
        return best_city
""",
        "visible_testcases": [
            {
                "input": {
                    "n": 4,
                    "edges": [[0,1,3],[1,2,1],[1,3,4],[2,3,1]],
                    "distanceThreshold": 4
                },
                "expected": 3
            },
            {
                "input": {
                    "n": 5,
                    "edges": [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]],
                    "distanceThreshold": 2
                },
                "expected": 0
            }
        ],
        "hidden_testcases": [
            {"input": {"n": 2, "edges": [[0, 1, 10]], "distanceThreshold": 5}, "expected": 1}
        ],
        "explanation": "Floyd-Warshall dynamic programming computes all-pairs shortest paths in $O(N^3)$ via `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. Then count neighbors within threshold for each city."
    }
]
