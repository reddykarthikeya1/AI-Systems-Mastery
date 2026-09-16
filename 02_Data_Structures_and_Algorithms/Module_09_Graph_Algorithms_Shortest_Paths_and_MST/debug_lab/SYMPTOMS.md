# Debug Lab 09 — Symptoms

> A routing and network-planning engine: shortest paths, negative-cost handling,
and minimum spanning trees for laying cable.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_routing_engine.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Dijkstra processes nodes it has already improved on

```
[1] Dijkstra shortest paths (non-negative weights)
      [(0, 1, 4), (0, 2, 1), (2, 1, 2)] -> [0, 3, 1] (expected [0, 3, 1])
      [(0, 1, 10), (0, 2, 1), (2, 3, 1), (3, 1, 1)] -> [0, 3, 1, 2] (expected [0, 3, 1, 2])
```

**Questions to answer:**

- The answers in this section are all correct. Add a counter to the `while heap` loop and print how many pops it performs.
- `heapq` has no decrease-key, so an improved distance is pushed as a new entry. What happens to the old entry?
- When a stale entry is popped, is `d` still equal to `dist[u]`? What does the loop do with it?

## Symptom 2 — Dijkstra and Bellman-Ford disagree on the same graph

```
[2] Dijkstra on a graph containing a negative edge
      [(0, 1, 4), (0, 2, 1), (2, 1, -2)]
          dijkstra     -> [0, -1, 1]
          bellman_ford -> [0, -1, 1]
      (both claim to compute shortest paths from node 0)
```

**Questions to answer:**

- The two functions report different distances for node 1. Which is smaller? Trace the path `0 -> 2 -> 1` by hand and add up its weights.
- Dijkstra finalises a node the first time it is removed from the heap. What is node 1's distance at the moment it is first finalised?
- Can a later edge ever *reduce* a distance that has already been finalised? What kind of edge weight makes that possible?

## Symptom 3 — A negative cycle produces finite distances

```
[3] Negative cycle detection
      [(0, 1, 1), (1, 0, -3)]
          bellman_ford -> [-2, 1]   (a reachable negative cycle exists)
      [(0, 1, 4), (0, 2, 1), (2, 1, -2)]
          bellman_ford -> [0, -1, 1]   (no negative cycle)
      (with a negative cycle, no shortest path is well defined)
```

**Questions to answer:**

- The first graph has a cycle `0 -> 1 -> 0` costing `1 + (-3) = -2`. What happens to the path cost if you go round it twice? Ten times?
- Is there a well-defined shortest distance to node 1 in that graph?
- Bellman-Ford runs n-1 rounds. After those rounds, what would one more round reveal about a graph containing a negative cycle?

## Symptom 4 — A disconnected graph still reports a spanning-tree cost

```
[4] Minimum spanning tree cost
      n=4 [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)] -> 6 (expected 6)
      n=3 [(0, 1, 1)] -> 1 (expected disconnected: no spanning tree exists)
      n=2 [] -> 0 (expected disconnected: no spanning tree exists)
      n=4 [(0, 1, 1), (0, 2, 1), (0, 3, 1)] -> 3 (expected 3)

====================================================================
Routing complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Two of the four cases are disconnected. What did the function return for them?
- A spanning tree on n nodes has exactly n-1 edges. How many edges did the function actually take in those cases?
- The variable `taken` is maintained but never read. What was it for?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_dijkstra` |
| 2 | `test_p02_bellman_ford` |
| 3 | `test_p02_bellman_ford` |
| 4 | `test_p05_kruskal_mst` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
