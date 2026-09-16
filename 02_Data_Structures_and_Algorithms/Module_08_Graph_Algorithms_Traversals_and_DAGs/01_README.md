# Module 08: Graph Traversals & DAGs (0 to 100 Mastery)

> **Adjacency Lists, Breadth-First Shortest Hop, Depth-First Backtracking & Kahn's Topological Sort**

Graphs represent networks, dependencies, and arbitrary relationships. In this module, you master **BFS level traversal**, **DFS component exploration**, **cycle detection via 3-color states**, and **Kahn's in-degree topological sort** for Directed Acyclic Graphs (DAGs).

---

## 1. Graph Representations: Matrix vs Adjacency List

| Feature | Adjacency Matrix ($V \\times V$) | Adjacency List |
| :--- | :--- | :--- |
| **Space** | $O(V^2)$ (Heavy for sparse graphs) | $O(V + E)$ (Optimal) |
| **Edge Lookup $(u, v)$** | $O(1)$ | $O(\\text{deg}(u))$ |
| **Neighbor Iteration** | $O(V)$ | $O(\\text{deg}(u))$ |

---

## 2. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

### Problem 1: Number of Islands ([LeetCode 200](https://leetcode.com/problems/number-of-islands/)) — Medium

#### Optimized: In-Place DFS Flood Fill
When encountering `'1'`, increment island count and recursively mark all connected `'1'`s to `'0'`.
```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Mark visited in-place
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
                
    return count
```
- **Time Complexity**: $O(R \\times C)$ — Each cell visited at most constant times.
- **Space Complexity**: $O(R \\times C)$ call stack worst-case.

---

### Problem 2: Clone Graph ([LeetCode 133](https://leetcode.com/problems/clone-graph/)) — Medium

#### Optimized: Hash Map Old-to-New Node Mapping DFS
Map `old_node -> new_node`. If visited, return mapped copy; otherwise create clone, add to map, and recursively clone neighbors.
- **Time Complexity**: $O(V + E)$, **Space Complexity**: $O(V)$.

---

### Problem 3: Max Area of Island ([LeetCode 695](https://leetcode.com/problems/max-area-of-island/)) — Medium

#### Optimized: Accumulator DFS
```python
def max_area_of_island(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    max_area = 0
    
    def dfs(r: int, c: int) -> int:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
    return max_area
```
- **Time Complexity**: $O(R \\times C)$, **Space Complexity**: $O(R \\times C)$.

---

### Problem 4: Rotting Oranges ([LeetCode 994](https://leetcode.com/problems/rotting-oranges/)) — Medium

#### Optimized: Multi-Source BFS
Enque all initial rotten oranges `(r, c)`. Advance time layer by layer in BFS, infecting fresh oranges.
```python
from collections import deque

def oranges_rotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
                
    if fresh == 0:
        return 0
        
    minutes = -1
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while q:
        minutes += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
                    
    return minutes if fresh == 0 else -1
```
- **Time Complexity**: $O(R \\times C)$, **Space Complexity**: $O(R \\times C)$.

---

### Problem 5: Course Schedule ([LeetCode 207](https://leetcode.com/problems/course-schedule/)) — Medium

#### Optimized: Kahn's Algorithm (In-Degree BFS)
Compute in-degree for all courses. Enqueue courses with `in_degree == 0`. Decrement in-degree of prerequisites as courses are taken. If total taken equals $N$, no cycle exists.
```python
from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    adj = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    for dest, src in prerequisites:
        adj[src].append(dest)
        in_degree[dest] += 1
        
    q = deque([i for i in range(num_courses) if in_degree[i] == 0])
    taken = 0
    
    while q:
        curr = q.popleft()
        taken += 1
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)
                
    return taken == num_courses
```
- **Time Complexity**: $O(V + E)$ — Optimal topological order verification.
- **Space Complexity**: $O(V + E)$.

---

## 3. Hands-On Project & Test Suite

Verify your graph traversals and topological sorting engine:
- Starter Template: [`starter/dag_and_traversal_engine.py`](starter/dag_and_traversal_engine.py)
- Production Solution: [`project_solution/dag_and_traversal_engine.py`](project_solution/dag_and_traversal_engine.py)
- Pytest Suite: [`project_solution/test_dag_and_traversal_engine.py`](project_solution/test_dag_and_traversal_engine.py)

## 🧪 Practice & Verification

Reading a module teaches recognition. Only the problems teach recall — and the
debug lab teaches the thing neither of them does, which is diagnosis.

### 1. Build the module project

```bash
cd starter
python -m pytest ../project_solution -q      # must FAIL before you start
```

Every shipped test must fail with `NotImplementedError` on an untouched
starter. If any passes, the grading loop is broken and is telling you your work
is correct when it has not been done — run `make integrity` from the course
root.

### 2. Work the problem bank — 8 problems

```bash
cd problems
python -m pytest tests -q                    # all of this module's problems
python -m pytest tests -q -k p03             # just problem 3
```

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Number Of Islands](problems/p01_num_islands.py) | DFS flood fill | Medium | `Time O(rows*cols), Space O(rows*cols)` |
| 02 | [Count Connected Components](problems/p02_count_components.py) | BFS/DFS over an adjacency list | Medium | `Time O(n + E), Space O(n + E)` |
| 03 | [Topological Sort](problems/p03_topological_order.py) | Kahn's algorithm | Medium | `Time O((n + E) log n), Space O(n + E)` |
| 04 | [Detect A Cycle In A Directed Graph](problems/p04_has_cycle_directed.py) | DFS with three colours | Medium | `Time O(n + E), Space O(n + E)` |
| 05 | [Course Schedule](problems/p05_can_finish_courses.py) | Cycle detection on prerequisites | Medium | `Time O(V + E), Space O(V + E)` |
| 06 | [Rotting Oranges](problems/p06_rotting_oranges.py) | Multi-source BFS | Medium | `Time O(rows*cols), Space O(rows*cols)` |
| 07 | [Shortest Path In A Binary Matrix](problems/p07_shortest_path_grid.py) | BFS with 8-directional moves | Medium | `Time O(n^2), Space O(n^2)` |
| 08 | [Word Ladder Length](problems/p08_word_ladder.py) | BFS over an implicit graph | Hard | `Time O(N * L * 26), Space O(N * L)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_graph_traversals.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. Choose BFS over DFS for unweighted shortest paths, and explain why DFS's first arrival is not optimal.
2. Detect a directed cycle with three colours, and produce a DAG that a two-state check rejects.
3. Use Kahn's algorithm and read its output length as cycle detection.
4. Seed a multi-source BFS and say what it turns O(V*E) into.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)
