from .models import Problem

def get_problems_46_60() -> list[Problem]:
    problems = []

    # ----------------------------------------------------
    # Problem 46: Subsets
    # ----------------------------------------------------
    def trace_p46():
        nums = [1, 2, 3]
        out = [
            f"Input: {nums}",
            "Power Set construction tree (Include / Exclude):",
            "  Start: []",
            "  Include 1: [1]",
            "    Include 2: [1, 2] -> Include 3: [1, 2, 3], Exclude 3: [1, 2]",
            "    Exclude 2: [1] -> Include 3: [1, 3], Exclude 3: [1]",
            "  Exclude 1: []",
            "    Include 2: [2] -> Include 3: [2, 3], Exclude 3: [2]",
            "    Exclude 2: [] -> Include 3: [3], Exclude 3: []",
            "Total subsets (2^3 = 8): [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=46,
        slug="p46_subsets",
        title="Subsets",
        category="Backtracking",
        difficulty="Medium",
        statement="Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.",
        brute_force="Iterate through integers $0$ to $2^N - 1$, taking the $j^{\\text{th}}$ element if the $j^{\\text{th}}$ bit is set. Time: $O(N \\cdot 2^N)$, Space: $O(N \\cdot 2^N)$.",
        key_insight="At each step in Backtracking DFS, either include `nums[i]` or exclude `nums[i]`, generating all $2^N$ subsets systematically.",
        func_name="subsets",
        stub_code="""def subsets(nums: list[int]) -> list[list[int]]:
    \"\"\"Generates power set of nums in O(N * 2^N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def subsets(nums: list[int]) -> list[list[int]]:
    \"\"\"Generates power set of nums in O(N * 2^N) time.\"\"\"
    res: list[list[int]] = []
    subset: list[int] = []
    
    def dfs(i: int):
        if i >= len(nums):
            res.append(list(subset))
            return
            
        # Decision 1: Include nums[i]
        subset.append(nums[i])
        dfs(i + 1)
        
        # Decision 2: Do NOT include nums[i]
        subset.pop()
        dfs(i + 1)
        
    dfs(0)
    return res
""",
        tests_code="""assert sorted([sorted(s) for s in subsets([1, 2, 3])]) == sorted([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
assert subsets([0]) == [[0], []] or subsets([0]) == [[], [0]]
assert subsets([]) == [[]]
""",
        time_complexity="$O(N \\cdot 2^N)$ to generate $2^N$ subsets of average length $N/2$.",
        space_complexity="$O(N)$ recursion depth.",
        follow_up="What if the input contains duplicates (Subsets II)? Sort the array first and skip duplicate branches when excluding the current element.",
        run_trace=trace_p46
    ))

    # ----------------------------------------------------
    # Problem 47: Number of Islands
    # ----------------------------------------------------
    def trace_p47():
        grid = [
            ["1","1","0","0","0"],
            ["1","1","0","0","0"],
            ["0","0","1","0","0"],
            ["0","0","0","1","1"]
        ]
        out = [
            f"Input grid (4x5):",
            "  Row 0: 1 1 0 0 0",
            "  Row 1: 1 1 0 0 0",
            "  Row 2: 0 0 1 0 0",
            "  Row 3: 0 0 0 1 1",
            "Traversal execution:",
            "  Encounter '1' at (0, 0) -> Island 1 found! Sink connected '1's via DFS: (0,0), (0,1), (1,0), (1,1)",
            "  Encounter '1' at (2, 2) -> Island 2 found! Sink (2, 2)",
            "  Encounter '1' at (3, 3) -> Island 3 found! Sink (3, 3), (3, 4)",
            "Total islands: 3"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=47,
        slug="p47_number_of_islands",
        title="Number of Islands",
        category="Graphs",
        difficulty="Medium",
        statement="Given an $m \\times n$ 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
        brute_force="Find all land cells and compute connected components via an $O((M \\cdot N)^2)$ all-pairs reachability scan.",
        key_insight="Iterate through grid. Whenever a `'1'` is found, increment island count and flood-fill sink all connected land cells to `'0'` using BFS or DFS.",
        func_name="num_islands",
        stub_code="""def num_islands(grid: list[list[str]]) -> int:
    \"\"\"Counts islands by sinking connected land in O(M * N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def num_islands(grid: list[list[str]]) -> int:
    \"\"\"Counts islands by sinking connected land in O(M * N) time.\"\"\"
    if not grid:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Sink land
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)
                
    return islands
""",
        tests_code="""g1 = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
assert num_islands(g1) == 1

g2 = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
assert num_islands(g2) == 3
assert num_islands([]) == 0
""",
        time_complexity="$O(M \\cdot N)$ visiting every cell a constant number of times.",
        space_complexity="$O(M \\cdot N)$ worst-case call stack space for a grid filled with land.",
        follow_up="What if mutating the input grid is forbidden? Maintain a `visited` boolean set/matrix or use Disjoint Set Union (Union-Find).",
        run_trace=trace_p47
    ))

    # ----------------------------------------------------
    # Problem 48: Clone Graph
    # ----------------------------------------------------
    def trace_p48():
        out = [
            "Graph: 1 -- 2, 2 -- 3, 3 -- 4, 4 -- 1 (Cycle of 4 nodes)",
            "DFS clone process:",
            "  1. Visit node 1 -> Create clone Node(1), store in visited map",
            "  2. Visit neighbor 2 -> Create clone Node(2), link clone(1).neighbors.append(clone(2))",
            "  3. Visit neighbor 3 -> Create clone Node(3)",
            "  4. Visit neighbor 4 -> Create clone Node(4)",
            "  5. Node 4 points back to 1 -> clone(1) already in visited map! Link without recurse.",
            "Result: Deep copy created with identical topology and separate memory references."
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=48,
        slug="p48_clone_graph",
        title="Clone Graph",
        category="Graphs",
        difficulty="Medium",
        statement="Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors.",
        brute_force="Traversing without tracking visited nodes causes an infinite loop due to graph cycles.",
        key_insight="Maintain a hash map `visited: dict[Node, Node]` mapping original node references to their cloned copies. For each neighbor, either recurse or return the existing clone from the map.",
        func_name="clone_graph",
        stub_code="""class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional[GraphNode]) -> Optional[GraphNode]:
    \"\"\"Clones an undirected graph using DFS in O(V + E) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional[GraphNode]) -> Optional[GraphNode]:
    \"\"\"Clones an undirected graph using DFS in O(V + E) time.\"\"\"
    if not node:
        return None
        
    cloned: dict[GraphNode, GraphNode] = {}
    
    def dfs(curr: GraphNode) -> GraphNode:
        if curr in cloned:
            return cloned[curr]
            
        copy = GraphNode(curr.val)
        cloned[curr] = copy
        for nei in curr.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
        
    return dfs(node)
""",
        tests_code="""n1 = GraphNode(1)
n2 = GraphNode(2)
n1.neighbors.append(n2)
n2.neighbors.append(n1)

c1 = clone_graph(n1)
assert c1 is not n1
assert c1.val == 1
assert len(c1.neighbors) == 1
assert c1.neighbors[0].val == 2
assert c1.neighbors[0].neighbors[0] is c1
assert clone_graph(None) is None
""",
        time_complexity="$O(V + E)$ visiting every vertex and edge once.",
        space_complexity="$O(V)$ hash map memory to store vertex clones.",
        follow_up="How to implement this with BFS instead of DFS? Use a queue: pop node, iterate neighbors, clone unvisited neighbors, push to queue, and wire up neighbor pointers.",
        run_trace=trace_p48
    ))

    # ----------------------------------------------------
    # Problem 49: Pacific Atlantic Water Flow
    # ----------------------------------------------------
    def trace_p49():
        out = [
            "Grid (5x5 elevation map):",
            "  Pacific borders: Top and Left edges",
            "  Atlantic borders: Bottom and Right edges",
            "Reverse inward flow search:",
            "  1. Multi-source BFS/DFS from Pacific boundary uphill (height >= prev): marks pacific_reachable set",
            "  2. Multi-source BFS/DFS from Atlantic boundary uphill: marks atlantic_reachable set",
            "  3. Intersection pacific_reachable & atlantic_reachable yields cells that flow to both oceans.",
            "Example coordinates: [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=49,
        slug="p49_pacific_atlantic_water_flow",
        title="Pacific Atlantic Water Flow",
        category="Graphs",
        difficulty="Medium",
        statement="There is an $m \\times n$ rectangular island that borders both the Pacific Ocean (top and left edges) and Atlantic Ocean (bottom and right edges). Water flows from a cell to an adjacent cell with an equal or lower height. Return a list of grid coordinates where water can flow to both oceans.",
        brute_force="Run BFS/DFS from every cell $(r, c)$ to check if both oceans are reachable. Time: $O((M \\cdot N)^2)$.",
        key_insight="Reverse the problem: start from the ocean borders and simulate water flowing **uphill** ($h[\\text{next}] \\ge h[\\text{curr}]$). Cells in the intersection of both reachability sets flow to both oceans.",
        func_name="pacific_atlantic",
        stub_code="""def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    \"\"\"Finds cells that can reach both oceans via reverse uphill BFS/DFS.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    \"\"\"Finds cells that can reach both oceans via reverse uphill BFS/DFS.\"\"\"
    if not heights:
        return []
        
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()
    
    def dfs(r: int, c: int, visit: set):
        visit.add((r, c))
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visit:
                if heights[nr][nc] >= heights[r][c]:  # Reverse flow: uphill
                    dfs(nr, nc, visit)
                    
    for c in range(cols):
        dfs(0, c, pac)
        dfs(rows - 1, c, atl)
    for r in range(rows):
        dfs(r, 0, pac)
        dfs(r, cols - 1, atl)
        
    return [list(coord) for coord in (pac & atl)]
""",
        tests_code="""h = [
  [1,2,2,3,5],
  [3,2,3,4,4],
  [2,4,5,3,1],
  [6,7,1,4,5],
  [5,1,1,2,4]
]
res = pacific_atlantic(h)
assert sorted(res) == sorted([[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]])
assert pacific_atlantic([[1]]) == [[0, 0]]
""",
        time_complexity="$O(M \\cdot N)$ as each cell is visited at most twice.",
        space_complexity="$O(M \\cdot N)$ memory for reachability sets.",
        follow_up="What if water can flow diagonally as well? Add 4 diagonal vectors to the exploration directions without changing the algorithmic structure.",
        run_trace=trace_p49
    ))

    # ----------------------------------------------------
    # Problem 50: Course Schedule (Cycle Detection / Topological Sort)
    # ----------------------------------------------------
    def trace_p50():
        numCourses = 4
        prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]
        out = [
            f"Input: numCourses = {numCourses}, prereqs = {prereqs}",
            "Graph construction:",
            "  In-degrees: {0: 0, 1: 1, 2: 1, 3: 2}",
            "  Adjacency: 0 -> [1, 2], 1 -> [3], 2 -> [3]",
            "Kahn's BFS queue simulation:",
            "  Step 1: In-degree 0 courses -> Queue: [0]",
            "  Step 2: Pop 0 (courses_taken = 1). Decrement neighbors 1 and 2 -> In-degrees: {1: 0, 2: 0} -> Queue: [1, 2]",
            "  Step 3: Pop 1 (courses_taken = 2). Decrement 3 -> In-degree: {3: 1}",
            "  Step 4: Pop 2 (courses_taken = 3). Decrement 3 -> In-degree: {3: 0} -> Queue: [3]",
            "  Step 5: Pop 3 (courses_taken = 4). Queue empty.",
            "Courses taken (4) == numCourses (4) -> True (DAG has no cycle)"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=50,
        slug="p50_course_schedule",
        title="Course Schedule",
        category="Graphs",
        difficulty="Medium",
        statement="There are a total of `numCourses` courses you have to take, labeled from $0$ to $\\text{numCourses} - 1$. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take course $b$ first if you want to take course $a$. Return `True` if you can finish all courses.",
        brute_force="Exhaustively check all permutations of course sequences: $O(N!)$.",
        key_insight="This is directed graph cycle detection. Use **Kahn's Algorithm (BFS with In-Degrees)**: start with in-degree 0 nodes; decrement neighbor in-degrees on pop. If the number of processed nodes equals `numCourses`, no cycle exists.",
        func_name="can_finish",
        stub_code="""def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    \"\"\"Determines if all courses can be finished using topological sort.\"\"\"
    raise NotImplementedError
""",
        solution_code="""from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    \"\"\"Determines if all courses can be finished using topological sort.\"\"\"
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    in_degrees = [0] * num_courses
    
    for crs, pre in prerequisites:
        adj[pre].append(crs)
        in_degrees[crs] += 1
        
    queue = deque([i for i in range(num_courses) if in_degrees[i] == 0])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        for nei in adj[node]:
            in_degrees[nei] -= 1
            if in_degrees[nei] == 0:
                queue.append(nei)
                
    return count == num_courses
""",
        tests_code="""assert can_finish(2, [[1, 0]]) is True
assert can_finish(2, [[1, 0], [0, 1]]) is False # Cycle deadlock
assert can_finish(1, []) is True
assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
""",
        time_complexity="$O(V + E)$ where $V = \\text{numCourses}$ and $E = \\text{len}(\\text{prerequisites})$.",
        space_complexity="$O(V + E)$ adjacency list and in-degree table.",
        follow_up="How to return the valid course sequence order (Course Schedule II)? Append each popped node to an `order` list; return `order` if `len(order) == numCourses` else `[]`.",
        run_trace=trace_p50
    ))

    # ----------------------------------------------------
    # Problem 51: Number of Connected Components in an Undirected Graph
    # ----------------------------------------------------
    def trace_p51():
        n = 5
        edges = [[0, 1], [1, 2], [3, 4]]
        out = [
            f"Input: n = {n}, edges = {edges}",
            "Initial state: 5 isolated components [0], [1], [2], [3], [4]",
            "Disjoint Set Union (DSU) operations:",
            "  Union(0, 1): root(0) != root(1) -> Merge! Components remaining: 4",
            "  Union(1, 2): root(0) != root(2) -> Merge! Components remaining: 3",
            "  Union(3, 4): root(3) != root(4) -> Merge! Components remaining: 2",
            "Final connected component count: 2 (Components: {0, 1, 2} and {3, 4})"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=51,
        slug="p51_number_of_connected_components",
        title="Number of Connected Components in an Undirected Graph",
        category="Graphs",
        difficulty="Medium",
        statement="You have a graph of $n$ nodes. You are given an integer $n$ and an array `edges` where `edges[i] = [a, b]` indicates that there is an edge between $a$ and $b$ in the graph. Return the number of connected components in the graph.",
        brute_force="Adjacency list with DFS from every unvisited node. Time: $O(V + E)$, Space: $O(V + E)$.",
        key_insight="Use **Disjoint Set Union (DSU)** with path compression and union-by-rank. Start with $n$ components; each successful union of two disjoint roots decrements the component count by 1 in nearly $O(1)$ amortized time ($O(\\alpha(N))$).",
        func_name="count_components",
        stub_code="""def count_components(n: int, edges: list[list[int]]) -> int:
    \"\"\"Counts connected components using Disjoint Set Union (Union-Find).\"\"\"
    raise NotImplementedError
""",
        solution_code="""def count_components(n: int, edges: list[list[int]]) -> int:
    \"\"\"Counts connected components using Disjoint Set Union (Union-Find).\"\"\"
    parent = list(range(n))
    rank = [1] * n
    
    def find(p: int) -> int:
        while p != parent[p]:
            parent[p] = parent[parent[p]]  # Path compression
            p = parent[p]
        return p
        
    def union(p1: int, p2: int) -> int:
        r1, r2 = find(p1), find(p2)
        if r1 == r2:
            return 0
        if rank[r1] < rank[r2]:
            parent[r1] = r2
            rank[r2] += rank[r1]
        else:
            parent[r2] = r1
            rank[r1] += rank[r2]
        return 1
        
    components = n
    for n1, n2 in edges:
        components -= union(n1, n2)
        
    return components
""",
        tests_code="""assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
assert count_components(4, []) == 4
""",
        time_complexity="$O(V + E \\cdot \\alpha(V))$ nearly linear time where $\\alpha$ is inverse Ackermann function.",
        space_complexity="$O(V)$ parent and rank arrays.",
        follow_up="When is DSU preferable over BFS/DFS? DSU excels in dynamic connectivity where edges arrive continuously over time (online graph connectivity).",
        run_trace=trace_p51
    ))

    # ----------------------------------------------------
    # Problem 52: Graph Valid Tree
    # ----------------------------------------------------
    def trace_p52():
        n = 5
        edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
        out = [
            f"Input: n = {n}, edges = {edges}",
            "Tree properties check:",
            "  1. Edge count condition: len(edges) == n - 1 (4 == 5 - 1 -> True)",
            "  2. Union-Find cycle check:",
            "     Union(0, 1): roots 0, 1 -> OK",
            "     Union(0, 2): roots 0, 2 -> OK",
            "     Union(0, 3): roots 0, 3 -> OK",
            "     Union(1, 4): roots 0, 4 -> OK",
            "No cycles detected and all nodes connected: True (Valid Tree)"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=52,
        slug="p52_graph_valid_tree",
        title="Graph Valid Tree",
        category="Graphs",
        difficulty="Medium",
        statement="Given $n$ nodes labeled from $0$ to $n - 1$ and a list of undirected edges, write a function to check whether these edges make up a valid tree.",
        brute_force="DFS to check if graph is connected and has no cycles. Time: $O(V + E)$.",
        key_insight="A graph of $n$ nodes is a valid tree if and only if: 1) It has exactly $n - 1$ edges, and 2) It is fully connected (no cycles). With Union-Find, if `find(u) == find(v)` on any edge, a cycle exists.",
        func_name="valid_tree",
        stub_code="""def valid_tree(n: int, edges: list[list[int]]) -> bool:
    \"\"\"Checks if graph is a valid tree using Disjoint Set Union.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def valid_tree(n: int, edges: list[list[int]]) -> bool:
    \"\"\"Checks if graph is a valid tree using Disjoint Set Union.\"\"\"
    if len(edges) != n - 1:
        return False
        
    parent = list(range(n))
    
    def find(p: int) -> int:
        while p != parent[p]:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p
        
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return False  # Cycle detected
        parent[root_u] = root_v
        
    return True
""",
        tests_code="""assert valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
assert valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False # Cycle between 1, 2, 3
assert valid_tree(4, [[0, 1], [2, 3]]) is False # Disconnected
assert valid_tree(1, []) is True
""",
        time_complexity="$O(V \\cdot \\alpha(V))$ amortized time.",
        space_complexity="$O(V)$ parent array memory.",
        follow_up="Why is `len(edges) == n - 1` an essential initial check? It immediately filters out under-connected graphs ($E < n - 1$) and graphs that must contain cycles ($E > n - 1$).",
        run_trace=trace_p52
    ))

    # ----------------------------------------------------
    # Problem 53: Network Delay Time (Dijkstra's Algorithm)
    # ----------------------------------------------------
    def trace_p53():
        times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
        n = 4
        k = 2
        out = [
            f"Input: times = {times}, n = {n}, k = {k}",
            "Dijkstra's Priority Queue execution:",
            "  Init: heap = [(0, 2)], dist = {2: 0}",
            "  Pop (0, node 2): visit neighbors 1 (wt 1) and 3 (wt 1)",
            "    Push (1, 1) -> dist[1] = 1",
            "    Push (1, 3) -> dist[3] = 1",
            "  Pop (1, node 1): no outgoing edges",
            "  Pop (1, node 3): visit neighbor 4 (wt 1) -> Push (2, 4) -> dist[4] = 2",
            "  Pop (2, node 4): no outgoing edges",
            "Final distances: {2: 0, 1: 1, 3: 1, 4: 2} -> Max time to reach all nodes: 2"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=53,
        slug="p53_network_delay_time",
        title="Network Delay Time",
        category="Graphs",
        difficulty="Medium",
        statement="You are given a network of $n$ nodes, labeled from $1$ to $n$. You are also given `times`, a list of travel times as directed edges `times[i] = (u, v, w)`. We will send a signal from node $k$. Return the minimum time it takes for all $n$ nodes to receive the signal. If it is impossible, return `-1`.",
        brute_force="Bellman-Ford algorithm with $V$ iterations: $O(V \\cdot E)$.",
        key_insight="Use **Dijkstra's Shortest Path Algorithm** with a Min-Heap: track shortest confirmed distance to each node. Pop lowest-latency frontier node, relax outgoing edges, and return the maximum distance among all nodes.",
        func_name="network_delay_time",
        stub_code="""def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    \"\"\"Finds time for signal to reach all nodes using Dijkstra's algorithm.\"\"\"
    raise NotImplementedError
""",
        solution_code="""import heapq
from collections import defaultdict

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    \"\"\"Finds time for signal to reach all nodes using Dijkstra's algorithm.\"\"\"
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
        
    min_heap = [(0, k)]
    dist: dict[int, int] = {}
    
    while min_heap:
        d, u = heapq.heappop(min_heap)
        if u in dist:
            continue
        dist[u] = d
        
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(min_heap, (d + w, v))
                
    return max(dist.values()) if len(dist) == n else -1
""",
        tests_code="""assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
assert network_delay_time([[1, 2, 1]], 2, 1) == 1
assert network_delay_time([[1, 2, 1]], 2, 2) == -1 # Unreachable node
""",
        time_complexity="$O(E \\log V)$ using binary min-heap.",
        space_complexity="$O(V + E)$ graph and heap storage.",
        follow_up="What if edge weights could be negative? Dijkstra fails with negative weights; you must use Bellman-Ford or SPFA in $O(V \\cdot E)$ time.",
        run_trace=trace_p53
    ))

    # ----------------------------------------------------
    # Problem 54: Alien Dictionary (Topological Sort)
    # ----------------------------------------------------
    def trace_p54():
        words = ["wrt", "wrf", "er", "ett", "rftt"]
        out = [
            f"Input dictionary: {words}",
            "Extracting ordering from adjacent word prefixes:",
            "  'wrt' vs 'wrf': 't' comes before 'f' -> Edge t -> f",
            "  'wrf' vs 'er': 'w' comes before 'e' -> Edge w -> e",
            "  'er' vs 'ett': 'r' comes before 't' -> Edge r -> t",
            "  'ett' vs 'rftt': 'e' comes before 'r' -> Edge e -> r",
            "Topological order of DAG: 'w' -> 'e' -> 'r' -> 't' -> 'f'",
            "Result: 'wertf'"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=54,
        slug="p54_alien_dictionary",
        title="Alien Dictionary",
        category="Graphs",
        difficulty="Hard",
        statement="There is a new alien language that uses the English alphabet. Given a list of words from the alien language dictionary sorted lexicographically by the rules of this new language, derive the order of letters in this language. If the order is invalid, return `\"\"`.",
        brute_force="Compare all pairs of words and check all permutations: factorial complexity.",
        key_insight="Compare adjacent pairs of words `words[i]` and `words[i+1]`. The first differing character gives a directed edge $c_1 \\to c_2$. Build graph and run Topological Sort (Kahn's or post-order DFS). If a cycle occurs (or prefix rule is violated like `\"abc\"` before `\"ab\"`), return `\"\"`.",
        func_name="alien_order",
        stub_code="""def alien_order(words: list[str]) -> str:
    \"\"\"Derives alien alphabet order using topological sort.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def alien_order(words: list[str]) -> str:
    \"\"\"Derives alien alphabet order using topological sort.\"\"\"
    adj = {c: set() for w in words for c in w}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""  # Invalid prefix condition
            
        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j])
                break
                
    visited: dict[str, bool] = {}  # False = in current DFS path, True = fully processed
    res = []
    
    def dfs(c: str) -> bool:
        if c in visited:
            return visited[c]
            
        visited[c] = False  # Mark in current recursion stack
        for nei in adj[c]:
            if not dfs(nei):
                return False
        visited[c] = True
        res.append(c)
        return True
        
    for c in list(adj.keys()):
        if c not in visited:
            if not dfs(c):
                return ""
                
    res.reverse()
    return "".join(res)
""",
        tests_code="""assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
assert alien_order(["z", "x"]) == "zx"
assert alien_order(["z", "x", "z"]) == "" # Cycle detected
assert alien_order(["abc", "ab"]) == "" # Prefix violation
""",
        time_complexity="$O(C)$ where $C$ is total length of all words combined.",
        space_complexity="$O(U + E)$ where $U$ is unique characters (at most 26).",
        follow_up="What if multiple valid alien alphabets exist? Any valid topological sort satisfies the problem criteria.",
        run_trace=trace_p54
    ))

    # ----------------------------------------------------
    # Problem 55: Climbing Stairs
    # ----------------------------------------------------
    def trace_p55():
        n = 5
        out = [
            f"Input: n = {n} steps",
            "Dynamic Programming state transition: dp[i] = dp[i-1] + dp[i-2]",
            "Base cases: dp[1] = 1, dp[2] = 2",
            "  i = 3: dp[3] = 1 + 2 = 3 ways",
            "  i = 4: dp[4] = 2 + 3 = 5 ways",
            "  i = 5: dp[5] = 3 + 5 = 8 ways",
            "Total ways to climb 5 stairs: 8"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=55,
        slug="p55_climbing_stairs",
        title="Climbing Stairs",
        category="Dynamic Programming",
        difficulty="Easy",
        statement="You are climbing a staircase. It takes $n$ steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        brute_force="Recursively compute `climb(n-1) + climb(n-2)` without memoization. Time: $O(2^N)$, Space: $O(N)$.",
        key_insight="To reach step $n$, you must have come from step $n-1$ (taking 1 step) or step $n-2$ (taking 2 steps). Hence $W(n) = W(n-1) + W(n-2)$ (Fibonacci sequence) computed in $O(1)$ space.",
        func_name="climb_stairs",
        stub_code="""def climb_stairs(n: int) -> int:
    \"\"\"Calculates number of ways to climb n stairs in O(N) time, O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def climb_stairs(n: int) -> int:
    \"\"\"Calculates number of ways to climb n stairs in O(N) time, O(1) space.\"\"\"
    if n <= 2:
        return n
        
    one, two = 1, 2
    for _ in range(3, n + 1):
        one, two = two, one + two
        
    return two
""",
        tests_code="""assert climb_stairs(2) == 2
assert climb_stairs(3) == 3
assert climb_stairs(5) == 8
assert climb_stairs(1) == 1
""",
        time_complexity="$O(N)$ linear time.",
        space_complexity="$O(1)$ constant auxiliary memory.",
        follow_up="Can this be solved in $O(\\log N)$ time? Yes, using Matrix Exponentiation on $\\begin{pmatrix}1 & 1 \\\\ 1 & 0\\end{pmatrix}^n$ or Binet's Fibonacci formula.",
        run_trace=trace_p55
    ))

    # ----------------------------------------------------
    # Problem 56: House Robber
    # ----------------------------------------------------
    def trace_p56():
        nums = [2, 7, 9, 3, 1]
        out = [
            f"Input houses: {nums}",
            f"{'House':<7} | {'Val':<5} | {'rob1 (prev-prev)':<18} | {'rob2 (prev)':<15} | {'New Max = max(rob1+val, rob2)':<30}",
            "-" * 80
        ]
        r1, r2 = 0, 0
        for i, val in enumerate(nums):
            new_r = max(r1 + val, r2)
            out.append(f"H{i}     | {val:<5} | {r1:<18} | {r2:<15} | max({r1}+{val}, {r2}) = {new_r}")
            r1, r2 = r2, new_r
        out.append(f"Max loot: {r2}")
        return "\n".join(out)

    problems.append(Problem(
        id=56,
        slug="p56_house_robber",
        title="House Robber",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected and will automatically contact the police if two adjacent houses were broken into on the same night. Determine the maximum amount of money you can rob tonight without alerting the police.",
        brute_force="Generate all non-adjacent subsets and take the maximum sum. Time: $O(2^N)$, Space: $O(N)$.",
        key_insight="At house $i$, choose either: 1) Rob house $i$ plus max loot from house $i-2$, or 2) Skip house $i$ and keep max loot from house $i-1$. Rolling state `rob1, rob2` achieves $O(1)$ space.",
        func_name="rob",
        stub_code="""def rob(nums: list[int]) -> int:
    \"\"\"Finds max non-adjacent house loot in O(N) time, O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def rob(nums: list[int]) -> int:
    \"\"\"Finds max non-adjacent house loot in O(N) time, O(1) space.\"\"\"
    rob1, rob2 = 0, 0
    for num in nums:
        rob1, rob2 = rob2, max(rob1 + num, rob2)
    return rob2
""",
        tests_code="""assert rob([1, 2, 3, 1]) == 4
assert rob([2, 7, 9, 3, 1]) == 12
assert rob([5]) == 5
assert rob([]) == 0
""",
        time_complexity="$O(N)$ linear single pass.",
        space_complexity="$O(1)$ rolling variables.",
        follow_up="What if houses are arranged in a tree structure (House Robber III)? Return a tuple `(rob_root, skip_root)` using post-order tree DP.",
        run_trace=trace_p56
    ))

    # ----------------------------------------------------
    # Problem 57: House Robber II
    # ----------------------------------------------------
    def trace_p57():
        nums = [2, 3, 2]
        out = [
            f"Input circular street: {nums}",
            "Because first house (2) and last house (2) are adjacent:",
            "  Case A: Rob from houses [0..N-2] = [2, 3] -> Max loot = 3",
            "  Case B: Rob from houses [1..N-1] = [3, 2] -> Max loot = 3",
            "Max of both scenarios: max(3, 3) = 3"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=57,
        slug="p57_house_robber_ii",
        title="House Robber II",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="You are a professional robber planning to rob houses along a street, but all houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Determine the maximum amount of money you can rob tonight without alerting the police.",
        brute_force="Exhaustively test all valid combinations: $O(2^N)$.",
        key_insight="Since the first and last houses are adjacent, you can never rob both. Break the circle into two linear sub-problems: `rob(nums[:-1])` (exclude last house) and `rob(nums[1:])` (exclude first house), taking $\\max(\\text{Case A}, \\text{Case B})$.",
        func_name="rob_circular",
        stub_code="""def rob_circular(nums: list[int]) -> int:
    \"\"\"Solves circular house robber problem in O(N) time, O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def rob_circular(nums: list[int]) -> int:
    \"\"\"Solves circular house robber problem in O(N) time, O(1) space.\"\"\"
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
        
    def rob_linear(houses: list[int]) -> int:
        r1, r2 = 0, 0
        for h in houses:
            r1, r2 = r2, max(r1 + h, r2)
        return r2
        
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
""",
        tests_code="""assert rob_circular([2, 3, 2]) == 3
assert rob_circular([1, 2, 3, 1]) == 4
assert rob_circular([1, 2, 3]) == 3
assert rob_circular([1]) == 1
""",
        time_complexity="$O(N)$ two linear passes.",
        space_complexity="$O(1)$ constant auxiliary memory.",
        follow_up="What if houses are arranged in a 2D grid where adjacent houses share an edge? This becomes the Maximum Independent Set on bipartite grid graphs, solvable via Max Flow / Min Cut.",
        run_trace=trace_p57
    ))

    # ----------------------------------------------------
    # Problem 58: Coin Change (Unbounded Knapsack)
    # ----------------------------------------------------
    def trace_p58():
        coins = [1, 2, 5]
        amount = 11
        dp = [0] + [float("inf")] * amount
        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])
        out = [
            f"Input: coins = {coins}, amount = {amount}",
            "Unbounded Knapsack DP table (min coins for amount a):",
            f"{'Amount':<8} | {'Min Coins dp[a]':<18} | {'Optimal transition':<25}",
            "-" * 55
        ]
        for a in range(1, amount + 1):
            out.append(f"{a:<8} | {dp[a]:<18} | dp[{a}] = 1 + dp[{a - min(c for c in coins if a-c >= 0)}]")
        out.append(f"Minimum coins for amount {amount}: {dp[amount]}")
        return "\n".join(out)

    problems.append(Problem(
        id=58,
        slug="p58_coin_change",
        title="Coin Change",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.",
        brute_force="Exhaustively explore all combinations with recursive branching: $O(S^A)$ where $S$ is coin count and $A$ is amount.",
        key_insight="Bottom-up Unbounded Knapsack: `dp[a]` stores minimum coins for amount $a$. Transition: `dp[a] = min(dp[a], 1 + dp[a - c])` for each coin $c \\le a$.",
        func_name="coin_change",
        stub_code="""def coin_change(coins: list[int], amount: int) -> int:
    \"\"\"Finds minimum coins needed for amount using DP in O(amount * len(coins)).\"\"\"
    raise NotImplementedError
""",
        solution_code="""def coin_change(coins: list[int], amount: int) -> int:
    \"\"\"Finds minimum coins needed for amount using DP in O(amount * len(coins)).\"\"\"
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != float("inf") else -1
""",
        tests_code="""assert coin_change([1, 2, 5], 11) == 3
assert coin_change([2], 3) == -1
assert coin_change([1], 0) == 0
assert coin_change([2, 5, 10, 1], 27) == 4 # 10 + 10 + 5 + 2
""",
        time_complexity="$O(A \\cdot C)$ where $A$ is target amount and $C$ is number of coin denominations.",
        space_complexity="$O(A)$ array of size `amount + 1`.",
        follow_up="How to count the number of UNIQUE combinations that sum to amount (Coin Change II)? Iterate coins on outer loop and amounts on inner loop: `dp[a] += dp[a - c]`.",
        run_trace=trace_p58
    ))

    # ----------------------------------------------------
    # Problem 59: Longest Increasing Subsequence
    # ----------------------------------------------------
    def trace_p59():
        nums = [10, 9, 2, 5, 3, 7, 101, 18]
        tails = []
        out = [
            f"Input: {nums}",
            "Patience Sorting / Binary Search (tails array represents smallest tail of all increasing subsequences of length i+1):",
            f"{'num':<5} | {'Binary Search Ins Pos':<22} | {'tails state':<25}",
            "-" * 55
        ]
        import bisect
        for x in nums:
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
            else:
                tails[idx] = x
            out.append(f"{x:<5} | Insert/replace at {idx:<6} | {str(tails):<25}")
        out.append(f"Length of LIS: {len(tails)}")
        return "\n".join(out)

    problems.append(Problem(
        id=59,
        slug="p59_longest_increasing_subsequence",
        title="Longest Increasing Subsequence",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="Given an integer array `nums`, return the length of the longest strictly increasing subsequence.",
        brute_force="Classic $O(N^2)$ DP where `dp[i] = 1 + max(dp[j])` for all $j < i$ with `nums[j] < nums[i]`.",
        key_insight="Patience Sorting with Binary Search: maintain array `tails` where `tails[i]` is the smallest tail element of all increasing subsequences of length $i+1$. For each `num`, binary search its insertion position in $O(\\log N)$, yielding $O(N \\log N)$ total time.",
        func_name="length_of_lis",
        stub_code="""def length_of_lis(nums: list[int]) -> int:
    \"\"\"Finds length of longest increasing subsequence in O(N log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""import bisect

def length_of_lis(nums: list[int]) -> int:
    \"\"\"Finds length of longest increasing subsequence in O(N log N) time.\"\"\"
    tails: list[int] = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)
""",
        tests_code="""assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
assert length_of_lis([7, 7, 7, 7, 7]) == 1
assert length_of_lis([]) == 0
""",
        time_complexity="$O(N \\log N)$ time using binary search bisection.",
        space_complexity="$O(N)$ space for tails array.",
        follow_up="How to reconstruct the actual subsequence instead of just its length? Maintain predecessor pointers array `parent` mapping each element to its previous subsequence item.",
        run_trace=trace_p59
    ))

    # ----------------------------------------------------
    # Problem 60: Word Break
    # ----------------------------------------------------
    def trace_p60():
        s = "leetcode"
        wordDict = ["leet", "code"]
        dp = [True] + [False] * len(s)
        out = [
            f"Input: s = '{s}', wordDict = {wordDict}",
            "1D DP Prefix matching: dp[i] is True if s[:i] can be segmented",
            f"{'i':<3} | {'Prefix s[:i]':<15} | {'dp[i]':<8} | {'Matched Word':<15}",
            "-" * 45
        ]
        for i in range(1, len(s) + 1):
            for w in wordDict:
                if i >= len(w) and dp[i - len(w)] and s[i - len(w) : i] == w:
                    dp[i] = True
                    out.append(f"{i:<3} | '{s[:i]}'        | True     | Matched '{w}'")
                    break
        out.append(f"Can segment string: {dp[len(s)]}")
        return "\n".join(out)

    problems.append(Problem(
        id=60,
        slug="p60_word_break",
        title="Word Break",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of one or more dictionary words.",
        brute_force="Recursively check every prefix and test remainder: $O(2^N)$ time.",
        key_insight="1D Dynamic Programming: `dp[i]` indicates whether prefix `s[:i]` can be segmented. For every index $i$ and word $w$ in dictionary, if `dp[i - len(w)]` is `True` and `s[i - len(w) : i] == w`, then `dp[i] = True`.",
        func_name="word_break",
        stub_code="""def word_break(s: str, word_dict: list[str]) -> bool:
    \"\"\"Checks if string s can be segmented into words from word_dict.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def word_break(s: str, word_dict: list[str]) -> bool:
    \"\"\"Checks if string s can be segmented into words from word_dict.\"\"\"
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for w in word_dict:
            if i >= len(w) and dp[i - len(w)]:
                if s[i - len(w) : i] == w:
                    dp[i] = True
                    break
                    
    return dp[len(s)]
""",
        tests_code="""assert word_break("leetcode", ["leet", "code"]) is True
assert word_break("applepenapple", ["apple", "pen"]) is True
assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
assert word_break("", ["a"]) is True
""",
        time_complexity="$O(N \\cdot M \\cdot K)$ where $N = \\text{len}(s)$, $M$ is dictionary word count, and $K$ is max word length.",
        space_complexity="$O(N)$ for the boolean DP array.",
        follow_up="How to return all possible segmented sentences (Word Break II)? Use DFS with memoization returning list of formed sentences.",
        run_trace=trace_p60
    ))

    return problems
