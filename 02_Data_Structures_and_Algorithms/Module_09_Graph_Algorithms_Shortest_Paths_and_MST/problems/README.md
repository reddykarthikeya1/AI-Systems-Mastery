# Module 09 — Problem Bank

Which shortest-path algorithm you need is decided entirely by the edge weights,
and it is worth committing to memory:

* **all weights equal** → BFS, `O(V + E)`
* **weights ≥ 0** → Dijkstra, `O(E log V)`
* **any negative weight** → Bellman-Ford, `O(V·E)`, and it detects negative
  cycles
* **at most k edges** → Bellman-Ford by rounds; Dijkstra's greedy invariant does
  not survive a hop limit

Running Dijkstra on a graph with a negative edge does not error. It returns a
wrong answer, confidently. Problem 02 contains that exact graph.

**8 problems** · Easy 0 · Medium 5 · Hard 3

---

## How to work these

```bash
cd problems
python -m pytest tests -q                 # all of this module's problems
python -m pytest tests -q -k p03          # just problem 3
```

Every problem must **fail** before you start — each stub raises
`NotImplementedError`. Fill in `pNN_<slug>.py`, not the solution file.

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Jumping to the reference solution costs you the exact skill the problem
exists to build.

When you are done, compare against `solutions/pNN_<slug>.py` — not to check the
answer, which the tests already did, but to compare *approach* and complexity.

---

## Problems

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Dijkstra's Shortest Paths](p01_dijkstra.py) | Dijkstra with a heap | Medium | `Time O(E log V), Space O(V + E)` |
| 02 | [Bellman-Ford With Negative Cycle Detection](p02_bellman_ford.py) | Bellman-Ford | Hard | `Time O(V*E), Space O(V)` |
| 03 | [Network Delay Time](p03_network_delay.py) | Dijkstra, single-source maximum | Medium | `Time O(E log V), Space O(V + E)` |
| 04 | [Cheapest Flight With At Most K Stops](p04_cheapest_flights_k_stops.py) | Bellman-Ford by rounds | Hard | `Time O(k*E), Space O(V)` |
| 05 | [Minimum Spanning Tree (Kruskal)](p05_kruskal_mst.py) | Sort edges + union-find | Medium | `Time O(E log E), Space O(V)` |
| 06 | [Minimum Spanning Tree (Prim)](p06_prim_mst.py) | Prim with a heap | Medium | `Time O(E log V), Space O(V + E)` |
| 07 | [Redundant Connection](p07_redundant_connection.py) | Union-find cycle detection | Medium | `Time O(n α(n)), Space O(n)` |
| 08 | [Minimum Cost To Connect All Points](p08_min_cost_connect_points.py) | MST on a complete graph | Hard | `Time O(n^2 log n), Space O(n)` |

## Patterns covered

- Bellman-Ford
- Bellman-Ford by rounds
- Dijkstra with a heap
- Dijkstra, single-source maximum
- MST on a complete graph
- Prim with a heap
- Sort edges + union-find
- Union-find cycle detection

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
