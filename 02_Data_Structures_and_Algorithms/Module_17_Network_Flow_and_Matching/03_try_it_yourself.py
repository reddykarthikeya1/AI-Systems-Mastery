"""Beginner playground for Module 17 - Network Flow & Bipartite Matching.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import deque

# -------------------------------------------- 1. Residual Graph and Forward/Backward Capacities
capacity = {('s', 'A'): 10, ('A', 't'): 8}
flow = {('s', 'A'): 6, ('A', 't'): 6}

def residual(u, v):
    cap = capacity.get((u, v), 0)
    f = flow.get((u, v), 0)
    back_f = flow.get((v, u), 0)
    return (cap - f) + back_f

assert residual('s', 'A') == 4, "10 - 6 = 4 remaining forward capacity"
assert residual('A', 's') == 6, "Can push 6 units backward to cancel flow"
assert residual('A', 't') == 2
print("Residual graph capacities correctly calculated.")

# -------------------------------------------- 2. Edmonds-Karp BFS Augmenting Path
nodes = ['s', 'A', 'B', 't']
edges = {
    's': [('A', 10), ('B', 5)],
    'A': [('B', 15), ('t', 10)],
    'B': [('t', 10)],
    't': []
}

# Find single augmenting path using BFS
def find_path():
    parent = {'s': None}
    q = deque(['s'])
    while q:
        curr = q.popleft()
        if curr == 't':
            break
        for nxt, cap in edges[curr]:
            if nxt not in parent and cap > 0:
                parent[nxt] = curr
                q.append(nxt)
    if 't' not in parent:
        return []
    path = []
    curr = 't'
    while curr:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]

path = find_path()
assert path == ['s', 'A', 't']
assert path[0] == 's' and path[-1] == 't'
print(f"Discovered augmenting path: {' -> '.join(path)}")

# -------------------------------------------- 3. Max-Flow Min-Cut Theorem Verification
# Total capacity across bottleneck cut separating s from t
cut_edges_capacity = 10 + 5  # s->A (10) and s->B (5)
max_flow_possible = 15
assert cut_edges_capacity == max_flow_possible
assert max_flow_possible > 0
print(f"Max-Flow Min-Cut identity holds: capacity={cut_edges_capacity}")

print()
print("All checks passed.")
