# Module 17: Network Flow and Matching

> **Brand new to this topic?** Start with
> [`02_FOUNDATIONS_PLAYGROUND.md`](02_FOUNDATIONS_PLAYGROUND.md) - the same ideas
> in plain language with runnable code.

Max-flow is the algorithm most people skip and then meet in a Staff-level
screen, because an unusual number of problems are flow problems wearing a
disguise.

| The question | The flow formulation |
| :--- | :--- |
| Assign N workers to M jobs, most assignments | bipartite matching |
| Cheapest set of links to disconnect A from B | minimum cut |
| How many independent routes survive a failure? | edge-disjoint paths |
| Choose projects with shared prerequisites for max profit | project selection |
| Image segmentation, foreground vs background | minimum cut |

## Learning path

| Step | File | What you do |
| :---: | :--- | :--- |
| 1 | [`02_FOUNDATIONS_PLAYGROUND.md`](02_FOUNDATIONS_PLAYGROUND.md) | Plain-language version, runnable |
| 2 | This README | Residual graphs, the two algorithms, the theorem |
| 3 | [`03_try_it_yourself.py`](03_try_it_yourself.py) | Watch augmenting paths being found |
| 4 | [`starter/`](starter) | Implement the engine yourself |
| 5 | [`problems/`](problems) | Six problems, five of them reductions |
| 6 | [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md) | Diagnose three planted defects |
| 7 | [`04_PROJECT_GUIDE.md`](04_PROJECT_GUIDE.md) | Build the whole engine |

---
## 1. The one idea: the residual graph

Push `f` units along an edge of capacity `c` and two things happen:

- the edge has `c - f` capacity left going forward, and
- a **backward** edge appears with capacity `f`.

That backward edge is not a road. It is an accounting entry meaning *"up to `f`
units currently flowing this way could be sent somewhere else instead"*. It is
what lets the algorithm undo an earlier bad decision, and it is the entire
reason a greedy path-picker gets the wrong answer while this gets the right one.

Confusing the residual edge with a real edge silently turns your directed graph
into an undirected one and inflates the answer. That is planted defect 1.

### The graph that proves you need it

```
s -> a (1)     s -> b (1)
a -> b (1)
a -> t (1)     b -> t (1)
```

Take `s -> a -> b -> t` first and every edge on it is saturated. Without
backward edges you are stuck at 1. With them, flow can be pushed back along
`a -> b` and rerouted, reaching the true answer of 2.

## 2. Edmonds-Karp

Repeatedly find *the shortest* augmenting path (so: BFS) and push its bottleneck.
`O(V * E^2)`.

Choosing the shortest path is what bounds the running time. Ford-Fulkerson with
an arbitrary path choice can take time proportional to the *flow value* - and
with irrational capacities may not terminate at all.

## 3. Dinic

<!-- GENERATED_ALGORITHM_DIAGRAM: DINIC_MAX_FLOW START -->

```mermaid
graph LR
  %% Dinic's Algorithm: Level Graph BFS Phase & Admissible Edges
  %% Generated from verified algorithm execution
  classDef default fill:#18181b,stroke:#3f3f46,stroke-width:1px,color:#f4f4f5;
  classDef source fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;
  classDef sink fill:#831843,stroke:#f43f5e,stroke-width:2px,color:#ffffff;
  classDef admissible stroke:#38bdf8,stroke-width:2px,color:#38bdf8;
  subgraph Level_0 ["Level 0 (Dist = 0)"]
    S["S<br/>lvl=0"]:::source
  end
  subgraph Level_1 ["Level 1 (Dist = 1)"]
    A["A<br/>lvl=1"]:::default
    B["B<br/>lvl=1"]:::default
  end
  subgraph Level_2 ["Level 2 (Dist = 2)"]
    C["C<br/>lvl=2"]:::default
    D["D<br/>lvl=2"]:::default
  end
  subgraph Level_3 ["Level 3 (Dist = 3)"]
    T["T<br/>lvl=3"]:::sink
  end

  %% Admissible Edges: level[v] == level[u] + 1 with residual capacity > 0
  S ==>|cap=10 (admissible)| A
  S ==>|cap=10 (admissible)| B
  A ==>|cap=4 (admissible)| C
  A ==>|cap=8 (admissible)| D
  B ==>|cap=9 (admissible)| D
  C ==>|cap=10 (admissible)| T
  D ==>|cap=10 (admissible)| T
```

<!-- GENERATED_ALGORITHM_DIAGRAM: DINIC_MAX_FLOW END -->

One BFS labels every node with its distance from the source - the **level
graph**. A DFS then pushes flow, but only along edges going strictly one level
deeper, until the level graph is saturated. Repeat.

`O(V^2 * E)` in general, and `O(E * sqrt(V))` on unit capacities - which is why
it is the right choice for bipartite matching. The `progress` pointer, which
never retries an edge within a phase, is what makes the blocking flow linear
rather than quadratic.

## 4. Max-flow min-cut

**The maximum flow equals the capacity of the minimum cut.** Not approximately,
not usually - exactly, always.

The constructive proof is short. Run the flow, then explore the *residual* graph
from the source. Everything reachable is the source side; everything else is the
sink side; the original edges crossing that boundary are a minimum cut.

Two things follow that are worth internalising:

1. You get a free correctness check. The capacities of the cut you return must
   sum to the flow you computed. If they do not, your code is wrong - it is a
   theorem, so there is no input for which it fails.
2. Exploring with the *original* capacities instead of the residual ones finds
   everything reachable and therefore returns an empty cut. That is planted
   defect 2, and the free check above catches it immediately.

A graph may have several minimum cuts of equal capacity. Residual exploration
from the source yields the *source-minimal* one.

## 5. Reductions are where the marks are

Only one of the six problems in this module is about implementing the algorithm.
The rest are about building the right graph. Notice what each capacity forbids:

| Capacity | The rule it encodes |
| :--- | :--- |
| `source -> worker = 1` | one job per worker |
| `job -> sink = 1` | one worker per job |
| every edge `= 1` | no edge reused (edge-disjoint paths) |
| `v_in -> v_out = 1` | no node reused (vertex-disjoint paths) |
| `source -> worker = k` | up to `k` shifts per worker |

Flow has no notion of node capacity. To get one, **split the node**: replace `v`
with `v_in -> v_out` and put the capacity on that internal edge. Every original
edge into `v` arrives at `v_in`; every edge out leaves `v_out`.

Setting `source -> worker` to 2 by mistake still produces the maximum *number* of
assignments, so the headline figure looks right while one worker quietly does
everyone's job. That is planted defect 3, and it is the reason to test the shape
of an answer and not only its size.

---

## 6. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

This section walks through the **6 canonical LeetCode challenges** curated for this module.
Each problem is analyzed from brute force intuition to the optimal invariant-driven solution, along with the critical edge cases to guard against in production.

### Problem 1: Is Graph Bipartite? ([LeetCode #785](https://leetcode.com/problems/is-graph-bipartite/)) — Medium

> **Pattern**: `2-Coloring BFS / Odd Cycle Detection` | **Target Time**: $O(V + E)$ | **Target Space**: $O(V)

#### Problem Specification
There is an undirected graph with `n` nodes, where each node is numbered between `0` and `n - 1`. You are given a 2D array `graph`, where `graph[u]` is an array of nodes that node `u` is adjacent to.
Return `true` if and only if it is bipartite.
A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge connects a node in set A and a node in set B.

#### Algorithmic Invariants & Optimal Derivation
A graph is bipartite if and only if it contains no odd-length cycles. Attempt 2-coloring with BFS: alternate colors between neighbors. If any edge connects two vertices of the same color, return False.

```python
from collections import deque

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
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 2: Possible Bipartition ([LeetCode #886](https://leetcode.com/problems/possible-bipartition/)) — Medium

> **Pattern**: `Graph 2-Coloring Formulation` | **Target Time**: $O(V + E)$ | **Target Space**: $O(V + E)

#### Problem Specification
We want to split a group of `n` people (labeled from 1 to `n`) into two groups of any size. Each person may dislike some other people.
Given the integer `n` and the array `dislikes` where `dislikes[i] = [ai, bi]`, return `true` if it is possible to split everyone into two groups in this way.

#### Algorithmic Invariants & Optimal Derivation
Construct an undirected graph where dislikes are edges. The problem reduces directly to verifying whether the graph is 2-colorable (bipartite).

```python
from collections import defaultdict, deque

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
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 3: Shortest Path with Alternating Colors ([LeetCode #1129](https://leetcode.com/problems/shortest-path-with-alternating-colors/)) — Medium

> **Pattern**: `Multi-Layer Flow BFS` | **Target Time**: $O(V + E)$ | **Target Space**: $O(V + E)

#### Problem Specification
You are given an integer `n`, the number of nodes in a directed graph where the nodes are labeled from `0` to `n - 1`. Each edge is red or blue in this graph.
Return an array `answer` of length `n`, where each `answer[x]` is the length of the shortest path from node 0 to node x such that the edge colors alternate, or `-1` if no such path exists.

#### Algorithmic Invariants & Optimal Derivation
Model the state graph as $(node, last\_color)$. Running BFS on this layered product graph guarantees finding the shortest alternating path to each node.

```python
from collections import defaultdict, deque

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
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 4: Find Critical and Pseudo-Critical Edges in MST ([LeetCode #1489](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-mst/)) — Hard

> **Pattern**: `MST Min-Cut Sensitivity Analysis / Kruskal's` | **Target Time**: $O(E^2 \cdot lpha(V))$ | **Target Space**: $O(V + E)

#### Problem Specification
Given a weighted undirected connected graph with `n` vertices numbered from 0 to `n - 1`, and an array `edges` where `edges[i] = [fromi, toi, weighti]`.
An MST edge whose deletion increases the MST weight is called a critical edge. A pseudo-critical edge is that which can appear in some MSTs but not all.
Find all the critical and pseudo-critical edges in the given graph.

#### Algorithmic Invariants & Optimal Derivation
Compute base MST cost via Kruskal's. An edge is critical if excluding it strictly increases MST weight (or disconnects the graph). An edge is pseudo-critical if forcibly including it still produces an MST of base cost.

```python
class UnionFind:
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
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 5: Maximum Students Taking Exam ([LeetCode #1349](https://leetcode.com/problems/maximum-students-taking-exam/)) — Hard

> **Pattern**: `Maximum Independent Set / Bitmask DP` | **Target Time**: $O(M 	imes 2^{2N})$ | **Target Space**: $O(M 	imes 2^N)

#### Problem Specification
Given a `m x n` matrix `seats` that represent seats for students, where `seats[i][j] == '.'` is available and `'#'` is broken.
Students can see the answers of those sitting directly to their left, right, upper-left, and upper-right. Return the maximum number of students that can take the exam together without any student cheating.

#### Algorithmic Invariants & Optimal Derivation
Since students cannot see adjacent or diagonal neighbors, this is equivalent to Maximum Independent Set on a Bipartite / Row-layered graph. Solved via Bitmask Dynamic Programming.

```python
class Solution:
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
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 6: Campus Bikes II ([LeetCode #1066](https://leetcode.com/problems/campus-bikes-ii/)) — Medium

> **Pattern**: `Bipartite Min-Cost Matching / Bitmask DP` | **Target Time**: $O(W 	imes 2^B)$ | **Target Space**: $O(2^B)

#### Problem Specification
On a campus represented by a 2D grid, there are `n` workers and `m` bikes, with `n <= m`.
Assign each worker to a unique bike such that the sum of the Manhattan distances between each worker and their assigned bike is minimized. Return the minimum possible sum of Manhattan distances.

#### Algorithmic Invariants & Optimal Derivation
Weighted bipartite matching can be solved via Min-Cost Max-Flow (Hungarian Algorithm) or Bitmask Dynamic Programming where bitmask tracks assigned bikes.

```python
class Solution:
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
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---
## You have mastered this when you can

- [ ] Explain what a residual edge means, and why it is not a road.
- [ ] Draw the four-node graph where a greedy choice needs to be undone.
- [ ] Say why Edmonds-Karp insists on the *shortest* augmenting path.
- [ ] Explain what a level graph is and what the `progress` pointer prevents.
- [ ] State max-flow min-cut and use it as a self-check on your own code.
- [ ] Construct the minimum cut from a saturated flow, and say which capacities
      the reachability search must use.
- [ ] Model "assign workers to jobs" as a flow network from scratch.
- [ ] Explain node splitting and when you need it.
- [ ] Give a case where greedy matching returns fewer pairs than the maximum.
