# 🐣 Interactive Foundations Playground: Shortest Paths & Minimum Spanning Trees

> *"Dijkstra is a GPS navigation unit that explores roads in strictly increasing travel time order."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import heapq
```

---

## 1. Dijkstra's Algorithm with Priority Queue

Dijkstra's algorithm greedily expands the closest unvisited node using a min-heap, yielding single-source shortest paths in $O((V + E) \log V)$ time.

```python
adj = {
    'A': [('B', 4), ('C', 2)],
    'C': [('B', 1), ('D', 5)],
    'B': [('D', 1)],
    'D': []
}

def dijkstra(start):
    distances = {u: float('inf') for u in adj}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > distances[u]:
            continue
        for v, weight in adj[u]:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                heapq.heappush(pq, (distances[v], v))
    return distances

dist = dijkstra('A')
assert dist['A'] == 0
assert dist['B'] == 3, "A -> C (2) -> B (1) = 3"
assert dist['D'] == 4, "A -> C -> B -> D = 4"
print(f"Shortest distances from A: {dist}")
```

---

## 2. Disjoint Set Union (DSU) for Cycle Detection

Kruskal's algorithm sorts edges by weight and selects edges connecting distinct components using Union-Find to form a Minimum Spanning Tree without cycles.

```python
parent = {x: x for x in ['A', 'B', 'C', 'D']}

def find(i):
    if parent[i] == i:
        return i
    parent[i] = find(parent[i])
    return parent[i]

def union(i, j):
    root_i = find(i)
    root_j = find(j)
    if root_i != root_j:
        parent[root_i] = root_j
        return True
    return False

assert union('A', 'B') is True
assert union('B', 'C') is True
assert union('A', 'C') is False, "A and C already in the same component"
print("DSU correctly identified redundant edge forming cycle.")
```

---

## 3. Edge Relaxation Triangular Invariant

For any edge $(u, v)$ with weight $w$, relaxation ensures the triangle inequality: $\text{dist}[v] \le \text{dist}[u] + w$.

```python
u_dist = 10
v_dist = 25
edge_weight = 7
if u_dist + edge_weight < v_dist:
    v_dist = u_dist + edge_weight

assert v_dist == 17
assert v_dist <= u_dist + edge_weight
print(f"Relaxed node v distance: {v_dist}")
```

---
