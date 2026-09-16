# Debug Lab 08 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Diagonally touching cells are merged into one island

**Location:** `num_islands`, the `DIRS` tuple

**The bug:**

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1))      # the last four are diagonals
```

**The fix:**

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))    # orthogonal only
```

**Why it matters.** Eight directions include the four diagonals, so cells that touch only at a
corner get flood-filled together. The problem defines adjacency as horizontal or
vertical only.

The count is always a plausible small integer and is *correct* on any grid whose
land happens not to touch diagonally — which includes most hand-drawn examples.
A checkerboard is the clean discriminator: eight separate cells become one.

Adjacency is a modelling decision, not an implementation detail. Write down
whether diagonals count before writing the direction list.

**Proved by:** `test_p01_num_islands`

## Defect 2 — A valid DAG is reported as cyclic

**Location:** `has_cycle_directed`, the visited check

**The bug:**

```python
for v in adj[u]:
    if visited[v]:
        return True     # ANY revisit is called a cycle, including a re-convergence
```

**The fix:**

```python
WHITE, GREY, BLACK = 0, 1, 2
colour = [WHITE] * n

def dfs(u: int) -> bool:
    colour[u] = GREY                # on the current path
    for v in adj[u]:
        if colour[v] == GREY:       # a back edge - a real cycle
            return True
        if colour[v] == WHITE and dfs(v):
            return True
    colour[u] = BLACK               # finished; a later visit is harmless
    return False
```

**Why it matters.** Two states cannot express the distinction the problem needs. A node already
`visited` may be on the current DFS path — which is a genuine cycle — or it may
be finished, reached earlier by a different route, which a DAG is entirely
allowed to do.

The diamond `0→1→3, 0→2→3` is the minimal counterexample: node 3 is reached
twice and the function calls it a cycle. In a build system that means a
perfectly valid dependency graph is rejected as circular, and the error message
points at nothing real.

Three colours: WHITE untouched, GREY on the current path, BLACK done. Only a
GREY neighbour is a back edge.

**Proved by:** `test_p04_has_cycle_directed`

## Defect 3 — A cyclic graph still returns an ordering

**Location:** `topological_order`, the return statement

**The bug:**

```python
return out              # returns a PARTIAL order for a cyclic graph
```

**The fix:**

```python
# Fewer than n emitted means the remainder are stuck in a cycle.
return out if len(out) == n else []
```

**Why it matters.** Kahn's algorithm already detects cycles for free — nodes inside one never reach
in-degree zero, so they are never emitted. The information is right there in
`len(out)`, and the function throws it away.

Callers receive a shorter list that is a perfectly valid ordering *of the nodes
it contains*, with the cyclic ones silently absent. A build system would run a
subset of the targets and report success.

Checking the length is one comparison, and it converts a partial answer into an
explicit failure signal.

**Proved by:** `test_p03_topological_order`

## Defect 4 — The hop count is not the shortest

**Location:** `shortest_hops`, the traversal strategy

**The bug:**

```python
def dfs(u, depth, seen):
    if u == dst:
        if best[0] == -1:
            best[0] = depth     # the FIRST DFS arrival, not the shortest
        return
```

**The fix:**

```python
# BFS: the first arrival at a node is optimal in an unweighted graph.
queue = deque([(src, 0)])
seen = {src}
while queue:
    u, depth = queue.popleft()
    if u == dst:
        return depth
    for v in adj[u]:
        if v not in seen:
            seen.add(v)
            queue.append((v, depth + 1))
return -1
```

**Why it matters.** DFS commits to one branch and follows it to the end, so the first time it reaches
the destination it may have taken a long detour. Recording that first arrival
gives *a* path length, not the minimum.

The returned number is a real path length — the route exists — so it survives any
check that only asks "is this reachable?". It is simply not the shortest, and how
wrong it is depends on which neighbour happens to be listed first, so the same
graph with its edges reordered gives a different answer.

BFS explores by distance, so its first arrival at any node is already optimal.
For unweighted shortest paths that is not an optimisation, it is the correctness
argument.

**Proved by:** `test_p07_shortest_path_grid`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Diagonally touching cells are merged into one island | No |
| 2 | A valid DAG is reported as cyclic | No |
| 3 | A cyclic graph still returns an ordering | No |
| 4 | The hop count is not the shortest | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
