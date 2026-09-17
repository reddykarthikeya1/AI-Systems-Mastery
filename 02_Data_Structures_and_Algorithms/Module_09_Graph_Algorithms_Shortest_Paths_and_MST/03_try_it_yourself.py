"""Beginner playground for Module 09 - Shortest Paths & Minimum Spanning Trees.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import heapq

# -------------------------------------------- 1. Dijkstra's Algorithm with Priority Queue
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

# -------------------------------------------- 2. Disjoint Set Union (DSU) for Cycle Detection
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

# -------------------------------------------- 3. Edge Relaxation Triangular Invariant
u_dist = 10
v_dist = 25
edge_weight = 7
if u_dist + edge_weight < v_dist:
    v_dist = u_dist + edge_weight

assert v_dist == 17
assert v_dist <= u_dist + edge_weight
print(f"Relaxed node v distance: {v_dist}")

print()
print("All checks passed.")
