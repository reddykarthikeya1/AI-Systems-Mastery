# 🐣 Interactive Foundations Playground: Graph Algorithms & Traversals

> *"A graph is a social network: people are vertices, friendships are edges."*

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
from collections import deque
```

---

## 1. Adjacency List Representation

An adjacency list maps each vertex to a list of its outgoing neighbors, using $O(V + E)$ space.

```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
assert len(graph['A']) == 2
assert 'D' in graph['B']
print(f"Graph vertices count: {len(graph)}, edges from 'A': {graph['A']}")
```

---

## 2. Breadth-First Search (BFS) for Shortest Path

BFS uses a FIFO queue to discover vertices level-by-level, guaranteeing the shortest path distance in unweighted graphs.

```python
def bfs_distance(start, target):
    visited = {start: 0}
    queue = deque([start])
    while queue:
        curr = queue.popleft()
        if curr == target:
            return visited[curr]
        for neighbor in graph.get(curr, []):
            if neighbor not in visited:
                visited[neighbor] = visited[curr] + 1
                queue.append(neighbor)
    return -1

assert bfs_distance('A', 'F') == 2, "A -> C -> F is 2 hops"
assert bfs_distance('A', 'A') == 0
assert bfs_distance('A', 'D') == 2
print(f"BFS shortest distance from A to F: {bfs_distance('A', 'F')} hops")
```

---

## 3. Topological Sort of a Directed Acyclic Graph (DAG)

Kahn's algorithm repeatedly removes vertices with in-degree 0, producing a linear ordering that respects all precedence constraints.

```python
dag = {'build': ['test'], 'compile': ['build'], 'test': ['deploy'], 'deploy': []}
in_degree = {u: 0 for u in dag}
for u in dag:
    for v in dag[u]:
        in_degree[v] += 1

q = deque([u for u in dag if in_degree[u] == 0])
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in dag[u]:
        in_degree[v] -= 1
        if in_degree[v] == 0:
            q.append(v)

assert order == ['compile', 'build', 'test', 'deploy']
assert len(order) == 4
print(f"Topological execution schedule: {' -> '.join(order)}")
```

---
