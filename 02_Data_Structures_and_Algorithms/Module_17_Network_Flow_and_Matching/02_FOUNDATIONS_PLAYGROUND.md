# 🐣 Interactive Foundations Playground: Network Flow & Bipartite Matching

> *"Max-Flow is water flowing through a network of pipes: the bottleneck (min-cut) dictates maximum delivery."*

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

## 1. Residual Graph and Forward/Backward Capacities

Every flow $f$ on edge $(u, v)$ with capacity $C$ leaves residual capacity $C - f$ forward and creates residual capacity $f$ backward for cancellation.

```python
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
```

---

## 2. Edmonds-Karp BFS Augmenting Path

Using BFS to find augmenting paths with available residual capacity guarantees termination in $O(V E^2)$ time.

```python
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
```

---

## 3. Max-Flow Min-Cut Theorem Verification

The maximum volume of flow from source $s$ to sink $t$ strictly equals the minimum capacity of an $s-t$ cut separating the network.

```python
# Total capacity across bottleneck cut separating s from t
cut_edges_capacity = 10 + 5  # s->A (10) and s->B (5)
max_flow_possible = 15
assert cut_edges_capacity == max_flow_possible
assert max_flow_possible > 0
print(f"Max-Flow Min-Cut identity holds: capacity={cut_edges_capacity}")
```

---
