# Module 09: Shortest Paths & MST (0 to 100 Mastery)

> **Greedy Edge Relaxation, Priority Queue Dijkstra, Bellman-Ford Negative Cycles & Kruskal's MST**

Weighted graph algorithms solve latency routing in distributed systems and network layout design. In this module, you master **Dijkstra's Algorithm with Min-Heap**, **Bellman-Ford relaxation and negative cycle detection**, and **Kruskal's Minimum Spanning Tree with Disjoint Set Union**.

---

## 1. Algorithmic Tradeoffs for Shortest Paths

| Algorithm | Edge Weights | Time Complexity | Cycle Handling |
| :--- | :--- | :--- | :--- |
| **BFS** | Unweighted ($w=1$) | $O(V + E)$ | Handles general graphs |
| **Dijkstra** | Non-negative ($w \\ge 0$) | $O((V + E) \\log V)$ | Fails on negative edges |
| **Bellman-Ford** | Any ($w \\in \\mathbb{R}$) | $O(V \\cdot E)$ | Detects negative weight cycles |
| **Floyd-Warshall** | Any ($w \\in \\mathbb{R}$) | $O(V^3)$ | All-Pairs Shortest Path |

---

## 2. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

### Problem 1: Network Delay Time ([LeetCode 743](https://leetcode.com/problems/network-delay-time/)) — Medium

#### Optimized: Dijkstra's Algorithm with Min-Heap
```python
import heapq
from collections import defaultdict

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
        
    pq = [(0, k)]  # (dist, node)
    dist = {}
    
    while pq:
        d, u = heapq.heappop(pq)
        if u in dist:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(pq, (d + w, v))
                
    return max(dist.values()) if len(dist) == n else -1
```
- **Time Complexity**: $O(E \\log V)$, **Space Complexity**: $O(V + E)$.

---

### Problem 2: Min Cost to Connect All Points ([LeetCode 1584](https://leetcode.com/problems/min-cost-to-connect-all-points/)) — Medium

#### Optimized: Prim's Algorithm ($O(V^2 \\log V)$ Time)
Maintain min-heap of candidate edges connecting visited components to unvisited vertices. Add closest point greedily until all $V$ points are connected.
- **Time Complexity**: $O(V^2 \\log V)$, **Space Complexity**: $O(V^2)$.

---

### Problem 3: Cheapest Flights Within K Stops ([LeetCode 787](https://leetcode.com/problems/cheapest-flights-within-k-stops/)) — Medium

#### Optimized: Bellman-Ford Modified for $K + 1$ Steps
Relax edges at most $K + 1$ times using a snapshot of the previous distance array to prevent cascaded multi-hop relaxations within a single step.
```python
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    prices = [float("inf")] * n
    prices[src] = 0
    
    for _ in range(k + 1):
        temp = list(prices)
        for u, v, w in flights:
            if prices[u] != float("inf") and prices[u] + w < temp[v]:
                temp[v] = prices[u] + w
        prices = temp
        
    return int(prices[dst]) if prices[dst] != float("inf") else -1
```
- **Time Complexity**: $O(K \\times E)$, **Space Complexity**: $O(V)$.

---

### Problem 4: Swim in Rising Water ([LeetCode 778](https://leetcode.com/problems/swim-in-rising-water/)) — Hard

#### Optimized: Dijkstra Modified for Minimax Path
Use a min-heap storing `(max_elevation_so_far, r, c)`. Pop smallest elevation cell and explore 4 neighbors.
- **Time Complexity**: $O(N^2 \\log N)$, **Space Complexity**: $O(N^2)$.

---

### Problem 5: Word Ladder ([LeetCode 127](https://leetcode.com/problems/word-ladder/)) — Hard

#### Optimized: Bidirectional BFS
Simultaneously expand forward from `beginWord` and backward from `endWord`. Terminate the moment frontiers intersect.
- **Time Complexity**: $O(M^2 \\times N)$ where $M$ is word length and $N$ is dictionary size.
- **Space Complexity**: $O(M \\times N)$.

---

## 3. Hands-On Project & Test Suite

Verify your Shortest Path and MST engine:
- Starter Template: [`starter/shortest_path_mst_engine.py`](starter/shortest_path_mst_engine.py)
- Production Solution: [`project_solution/shortest_path_mst_engine.py`](project_solution/shortest_path_mst_engine.py)
- Pytest Suite: [`project_solution/test_shortest_path_mst_engine.py`](project_solution/test_shortest_path_mst_engine.py)

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
| 01 | [Dijkstra's Shortest Paths](problems/p01_dijkstra.py) | Dijkstra with a heap | Medium | `Time O(E log V), Space O(V + E)` |
| 02 | [Bellman-Ford With Negative Cycle Detection](problems/p02_bellman_ford.py) | Bellman-Ford | Hard | `Time O(V*E), Space O(V)` |
| 03 | [Network Delay Time](problems/p03_network_delay.py) | Dijkstra, single-source maximum | Medium | `Time O(E log V), Space O(V + E)` |
| 04 | [Cheapest Flight With At Most K Stops](problems/p04_cheapest_flights_k_stops.py) | Bellman-Ford by rounds | Hard | `Time O(k*E), Space O(V)` |
| 05 | [Minimum Spanning Tree (Kruskal)](problems/p05_kruskal_mst.py) | Sort edges + union-find | Medium | `Time O(E log E), Space O(V)` |
| 06 | [Minimum Spanning Tree (Prim)](problems/p06_prim_mst.py) | Prim with a heap | Medium | `Time O(E log V), Space O(V + E)` |
| 07 | [Redundant Connection](problems/p07_redundant_connection.py) | Union-find cycle detection | Medium | `Time O(n α(n)), Space O(n)` |
| 08 | [Minimum Cost To Connect All Points](problems/p08_min_cost_connect_points.py) | MST on a complete graph | Hard | `Time O(n^2 log n), Space O(n)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_routing_engine.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. State the decision rule from edge weights to shortest-path algorithm, all four cases.
2. Explain what Dijkstra assumes and give a graph where a negative edge silently breaks it.
3. Use Bellman-Ford's extra round to detect a negative cycle, and say why the answer is otherwise meaningless.
4. Implement both Kruskal and Prim, and say which suits a dense graph.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)
