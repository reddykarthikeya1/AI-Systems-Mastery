# Debug Lab 08 — Symptoms

> A dependency and connectivity service: island counting, cycle detection,
topological ordering and shortest-hop routing on a grid.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_graph_traversals.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Diagonally touching cells are merged into one island

```
[1] Island counting (orthogonal adjacency only)
      [['1', '1', '0'], ['1', '0', '0'], ['0', '0', '1']] -> 2 (expected 2)
      [['1', '0'], ['0', '1']] -> 1 (expected 2)
      [['1', '0', '1'], ['0', '1', '0'], ['1', '0', '1']] -> 1 (expected 5)
```

**Questions to answer:**

- Which rows disagree with the expected column? What do the disagreeing grids have in common?
- In `[[1,0],[0,1]]` the two land cells touch only at a corner. Should they be one island or two?
- Count the entries in `DIRS`. How many orthogonal neighbours does a grid cell have?

## Symptom 2 — A valid DAG is reported as cyclic

```
[2] Directed cycle detection
      n=2 [(0, 1), (1, 0)]
          reported True   expected True
      n=4 [(0, 1), (0, 2), (1, 3), (2, 3)]
          reported True   expected False
      n=4 [(0, 1), (1, 2), (2, 3)]
          reported False  expected False
      n=5 [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
          reported True   expected False
```

**Questions to answer:**

- Which cases disagree? Draw the second one. Is there any way to follow the arrows and return to where you started?
- In that graph, node 3 is reached twice — once via node 1 and once via node 2. Is being reached twice the same as being in a cycle?
- The DFS has two states: visited and not visited. What third piece of information do you need to distinguish 'on the current path' from 'finished, reached by another route'?

## Symptom 3 — A cyclic graph still returns an ordering

```
[3] Topological ordering
      n=4 [(0, 1), (1, 2), (2, 3)] -> [0, 1, 2, 3] (covers all 4 nodes: True)
      n=2 [(0, 1), (1, 0)] -> [] (covers all 2 nodes: False)
      n=3 [(0, 1), (1, 2), (2, 0)] -> [] (covers all 3 nodes: False)
      (a graph with a cycle has NO valid ordering)
```

**Questions to answer:**

- Look at the `covers all n nodes` column for the cyclic inputs. What does the function return for them?
- The note says a cyclic graph has no valid ordering. Is the returned value an empty list?
- Kahn's algorithm emits a node once its in-degree hits zero. In a cycle, does any node's in-degree ever reach zero?

## Symptom 4 — The hop count is not the shortest

```
[4] Shortest hop count
      [(0, 1), (1, 3), (0, 2), (2, 3)] 0->3 = 2 (expected 2)
      [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)] 0->4 = 4 (expected 1)
      [(0, 1), (1, 2), (2, 3), (0, 3)] 0->3 = 3 (expected 1)

====================================================================
Traversal service complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which rows disagree with the expected column? Is the reported value ever smaller than expected, or always larger?
- The function explores with DFS. When DFS first arrives at the destination, is that arrival guaranteed to be via the fewest hops?
- Which traversal order guarantees that the first arrival at a node is optimal in an unweighted graph?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_num_islands` |
| 2 | `test_p04_has_cycle_directed` |
| 3 | `test_p03_topological_order` |
| 4 | `test_p07_shortest_path_grid` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
