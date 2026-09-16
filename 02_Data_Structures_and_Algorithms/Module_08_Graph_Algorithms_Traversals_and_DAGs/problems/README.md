# Module 08 — Problem Bank

Two decisions dominate this module, and both are easy to get wrong in a way
that still produces plausible output.

**BFS or DFS?** For a shortest path in an unweighted graph it must be BFS —
BFS's first arrival at a node is optimal, DFS's is not. Problem 06 fails
outright with DFS.

**Two visited states or three?** Directed cycle detection needs three (white,
grey, black). With only visited/unvisited you report a cycle for any
re-encountered node, including a diamond, which is a false positive on a valid
DAG. Problem 04 contains exactly that case.

**8 problems** · Easy 0 · Medium 7 · Hard 1

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
| 01 | [Number Of Islands](p01_num_islands.py) | DFS flood fill | Medium | `Time O(rows*cols), Space O(rows*cols)` |
| 02 | [Count Connected Components](p02_count_components.py) | BFS/DFS over an adjacency list | Medium | `Time O(n + E), Space O(n + E)` |
| 03 | [Topological Sort](p03_topological_order.py) | Kahn's algorithm | Medium | `Time O((n + E) log n), Space O(n + E)` |
| 04 | [Detect A Cycle In A Directed Graph](p04_has_cycle_directed.py) | DFS with three colours | Medium | `Time O(n + E), Space O(n + E)` |
| 05 | [Course Schedule](p05_can_finish_courses.py) | Cycle detection on prerequisites | Medium | `Time O(V + E), Space O(V + E)` |
| 06 | [Rotting Oranges](p06_rotting_oranges.py) | Multi-source BFS | Medium | `Time O(rows*cols), Space O(rows*cols)` |
| 07 | [Shortest Path In A Binary Matrix](p07_shortest_path_grid.py) | BFS with 8-directional moves | Medium | `Time O(n^2), Space O(n^2)` |
| 08 | [Word Ladder Length](p08_word_ladder.py) | BFS over an implicit graph | Hard | `Time O(N * L * 26), Space O(N * L)` |

## Patterns covered

- BFS over an implicit graph
- BFS with 8-directional moves
- BFS/DFS over an adjacency list
- Cycle detection on prerequisites
- DFS flood fill
- DFS with three colours
- Kahn's algorithm
- Multi-source BFS

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
