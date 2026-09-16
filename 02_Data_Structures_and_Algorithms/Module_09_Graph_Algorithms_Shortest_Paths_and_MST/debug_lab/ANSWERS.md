# Debug Lab 09 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Dijkstra processes nodes it has already improved on

**Location:** `dijkstra`, the missing stale-entry check

**The bug:**

```python
d, u = heapq.heappop(heap)
for v, w in adj[u]:         # no check that d is still current
```

**The fix:**

```python
d, u = heapq.heappop(heap)
# heapq has no decrease-key, so improved distances are pushed as new entries
# and the old ones linger. Skip them.
if d > dist[u]:
    continue
for v, w in adj[u]:
```

**Why it matters.** Every time a node's distance improves, a fresh `(dist, node)` entry is pushed and
the previous one stays in the heap. Without the guard, each stale entry is popped
and its neighbours re-relaxed — work that can never improve anything, because a
better distance is already recorded.

The answers stay correct, which is why this passes every correctness test. What
degrades is the complexity: on a dense graph the redundant expansions multiply,
and the algorithm drifts away from its `O(E log V)` guarantee.

One comparison removes it. Recognising that a heap without decrease-key *must*
accumulate stale entries is the transferable part.

**Proved by:** `test_p01_dijkstra`

## Defect 2 — Dijkstra and Bellman-Ford disagree on the same graph

**Location:** `dijkstra` applied to a graph with a negative edge

**The bug:**

```python
# dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, -2)], 0)
# Node 1 is finalised at 4 before the edge (2, 1, -2) is ever considered.
```

**The fix:**

```python
# Dijkstra requires non-negative weights. With any negative edge, use
# Bellman-Ford, which relaxes every edge n-1 times and has no finalisation
# assumption to violate.
dist = bellman_ford(n, edges, source)
```

**Why it matters.** Dijkstra's correctness rests on a single assumption: once a node is popped with
the smallest tentative distance, nothing can improve it, because every remaining
path can only add non-negative weight. A negative edge breaks exactly that
assumption.

Here node 1 is finalised at 4 via the direct edge, and the cheaper route
`0 → 2 → 1` costing `1 + (-2) = -1` is discovered too late to matter. No
exception is raised and no warning is printed — Dijkstra simply returns a larger
number with complete confidence.

This is the single most important algorithm-selection rule in the module: check
the sign of the weights *before* choosing. Negative weights mean Bellman-Ford,
at `O(V·E)` instead of `O(E log V)`, and that cost is not optional.

**Proved by:** `test_p02_bellman_ford`

## Defect 3 — A negative cycle produces finite distances

**Location:** `bellman_ford`, the missing detection pass

**The bug:**

```python
for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
return dist             # no check for further improvement
```

**The fix:**

```python
for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w

# One extra round. Any edge that can STILL be relaxed means a negative cycle
# is reachable, and no shortest path is well defined.
for u, v, w in edges:
    if dist[u] != INF and dist[u] + w < dist[v]:
        return None
return dist
```

**Why it matters.** With a reachable negative cycle there is no shortest path at all: each additional
lap lowers the cost without bound. Returning a finite number asserts an answer to
a question that has none.

The values Bellman-Ford happens to hold after `n-1` rounds are simply where the
relaxation had got to when the loop ran out — plausible, finite, and meaningless.
A routing engine would quote them as prices.

The detection is nearly free: `n-1` rounds suffice for every genuine shortest
path, so any further improvement in one extra round proves a negative cycle. That
extra pass is the difference between an answer and a wrong answer.

**Proved by:** `test_p02_bellman_ford`

## Defect 4 — A disconnected graph still reports a spanning-tree cost

**Location:** `kruskal_mst`, the return statement

**The bug:**

```python
taken += 1
return total            # `taken` is counted and then ignored
```

**The fix:**

```python
taken += 1
# A spanning tree on n nodes needs exactly n-1 edges. Fewer means the graph
# was disconnected and no spanning tree exists.
return total if taken == n - 1 else -1
```

**Why it matters.** Kruskal happily terminates on a disconnected graph — it simply runs out of edges
having built a spanning *forest*. The total it returns is the cost of that
forest, which is a real number and not the answer to the question asked.

A cable-laying plan derived from it would leave sites unconnected while
reporting a complete budget. Nothing in the output distinguishes "the cheapest
tree costs 1" from "there is no tree, and here is the cost of the fragments".

The edge count is the check, and the code already computes it. An unused variable
that shadows a missing validation is worth noticing in review.

**Proved by:** `test_p05_kruskal_mst`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Dijkstra processes nodes it has already improved on | No |
| 2 | Dijkstra and Bellman-Ford disagree on the same graph | No |
| 3 | A negative cycle produces finite distances | No |
| 4 | A disconnected graph still reports a spanning-tree cost | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
