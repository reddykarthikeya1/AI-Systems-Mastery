"""Beginner playground for Module 08 - Graph Algorithms & Traversals.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import deque

# -------------------------------------------- 1. Adjacency List Representation
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

# -------------------------------------------- 2. Breadth-First Search (BFS) for Shortest Path
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

# -------------------------------------------- 3. Topological Sort of a Directed Acyclic Graph (DAG)
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

print()
print("All checks passed.")
