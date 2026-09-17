# Module 17: Network Flow and Matching

> **Brand new to this topic?** Start with
> [`02_FOUNDATIONS_PLAYGROUND.md`](02_FOUNDATIONS_PLAYGROUND.md) - the same ideas
> in plain language with runnable code.

Max-flow is the algorithm most people skip and then meet in a Staff-level
screen, because an unusual number of problems are flow problems wearing a
disguise.

| The question | The flow formulation |
| :--- | :--- |
| Assign N workers to M jobs, most assignments | bipartite matching |
| Cheapest set of links to disconnect A from B | minimum cut |
| How many independent routes survive a failure? | edge-disjoint paths |
| Choose projects with shared prerequisites for max profit | project selection |
| Image segmentation, foreground vs background | minimum cut |

## Learning path

| Step | File | What you do |
| :---: | :--- | :--- |
| 1 | [`02_FOUNDATIONS_PLAYGROUND.md`](02_FOUNDATIONS_PLAYGROUND.md) | Plain-language version, runnable |
| 2 | This README | Residual graphs, the two algorithms, the theorem |
| 3 | [`03_try_it_yourself.py`](03_try_it_yourself.py) | Watch augmenting paths being found |
| 4 | [`starter/`](starter) | Implement the engine yourself |
| 5 | [`problems/`](problems) | Six problems, five of them reductions |
| 6 | [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md) | Diagnose three planted defects |
| 7 | [`04_PROJECT_GUIDE.md`](04_PROJECT_GUIDE.md) | Build the whole engine |

---

## 1. The one idea: the residual graph

Push `f` units along an edge of capacity `c` and two things happen:

- the edge has `c - f` capacity left going forward, and
- a **backward** edge appears with capacity `f`.

That backward edge is not a road. It is an accounting entry meaning *"up to `f`
units currently flowing this way could be sent somewhere else instead"*. It is
what lets the algorithm undo an earlier bad decision, and it is the entire
reason a greedy path-picker gets the wrong answer while this gets the right one.

Confusing the residual edge with a real edge silently turns your directed graph
into an undirected one and inflates the answer. That is planted defect 1.

### The graph that proves you need it

```
s -> a (1)     s -> b (1)
a -> b (1)
a -> t (1)     b -> t (1)
```

Take `s -> a -> b -> t` first and every edge on it is saturated. Without
backward edges you are stuck at 1. With them, flow can be pushed back along
`a -> b` and rerouted, reaching the true answer of 2.

## 2. Edmonds-Karp

Repeatedly find *the shortest* augmenting path (so: BFS) and push its bottleneck.
`O(V * E^2)`.

Choosing the shortest path is what bounds the running time. Ford-Fulkerson with
an arbitrary path choice can take time proportional to the *flow value* - and
with irrational capacities may not terminate at all.

## 3. Dinic

<!-- GENERATED_ALGORITHM_DIAGRAM: DINIC_MAX_FLOW START -->

```mermaid
graph LR
  %% Dinic's Algorithm: Level Graph BFS Phase & Admissible Edges
  %% Generated from verified algorithm execution
  classDef default fill:#18181b,stroke:#3f3f46,stroke-width:1px,color:#f4f4f5;
  classDef source fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;
  classDef sink fill:#831843,stroke:#f43f5e,stroke-width:2px,color:#ffffff;
  classDef admissible stroke:#38bdf8,stroke-width:2px,color:#38bdf8;
  subgraph Level_0 ["Level 0 (Dist = 0)"]
    S["S<br/>lvl=0"]:::source
  end
  subgraph Level_1 ["Level 1 (Dist = 1)"]
    A["A<br/>lvl=1"]:::default
    B["B<br/>lvl=1"]:::default
  end
  subgraph Level_2 ["Level 2 (Dist = 2)"]
    C["C<br/>lvl=2"]:::default
    D["D<br/>lvl=2"]:::default
  end
  subgraph Level_3 ["Level 3 (Dist = 3)"]
    T["T<br/>lvl=3"]:::sink
  end

  %% Admissible Edges: level[v] == level[u] + 1 with residual capacity > 0
  S ==>|cap=10 (admissible)| A
  S ==>|cap=10 (admissible)| B
  A ==>|cap=4 (admissible)| C
  A ==>|cap=8 (admissible)| D
  B ==>|cap=9 (admissible)| D
  C ==>|cap=10 (admissible)| T
  D ==>|cap=10 (admissible)| T
```

<!-- GENERATED_ALGORITHM_DIAGRAM: DINIC_MAX_FLOW END -->

One BFS labels every node with its distance from the source - the **level
graph**. A DFS then pushes flow, but only along edges going strictly one level
deeper, until the level graph is saturated. Repeat.

`O(V^2 * E)` in general, and `O(E * sqrt(V))` on unit capacities - which is why
it is the right choice for bipartite matching. The `progress` pointer, which
never retries an edge within a phase, is what makes the blocking flow linear
rather than quadratic.

## 4. Max-flow min-cut

**The maximum flow equals the capacity of the minimum cut.** Not approximately,
not usually - exactly, always.

The constructive proof is short. Run the flow, then explore the *residual* graph
from the source. Everything reachable is the source side; everything else is the
sink side; the original edges crossing that boundary are a minimum cut.

Two things follow that are worth internalising:

1. You get a free correctness check. The capacities of the cut you return must
   sum to the flow you computed. If they do not, your code is wrong - it is a
   theorem, so there is no input for which it fails.
2. Exploring with the *original* capacities instead of the residual ones finds
   everything reachable and therefore returns an empty cut. That is planted
   defect 2, and the free check above catches it immediately.

A graph may have several minimum cuts of equal capacity. Residual exploration
from the source yields the *source-minimal* one.

## 5. Reductions are where the marks are

Only one of the six problems in this module is about implementing the algorithm.
The rest are about building the right graph. Notice what each capacity forbids:

| Capacity | The rule it encodes |
| :--- | :--- |
| `source -> worker = 1` | one job per worker |
| `job -> sink = 1` | one worker per job |
| every edge `= 1` | no edge reused (edge-disjoint paths) |
| `v_in -> v_out = 1` | no node reused (vertex-disjoint paths) |
| `source -> worker = k` | up to `k` shifts per worker |

Flow has no notion of node capacity. To get one, **split the node**: replace `v`
with `v_in -> v_out` and put the capacity on that internal edge. Every original
edge into `v` arrives at `v_in`; every edge out leaves `v_out`.

Setting `source -> worker` to 2 by mistake still produces the maximum *number* of
assignments, so the headline figure looks right while one worker quietly does
everyone's job. That is planted defect 3, and it is the reason to test the shape
of an answer and not only its size.

---

## You have mastered this when you can

- [ ] Explain what a residual edge means, and why it is not a road.
- [ ] Draw the four-node graph where a greedy choice needs to be undone.
- [ ] Say why Edmonds-Karp insists on the *shortest* augmenting path.
- [ ] Explain what a level graph is and what the `progress` pointer prevents.
- [ ] State max-flow min-cut and use it as a self-check on your own code.
- [ ] Construct the minimum cut from a saturated flow, and say which capacities
      the reachability search must use.
- [ ] Model "assign workers to jobs" as a flow network from scratch.
- [ ] Explain node splitting and when you need it.
- [ ] Give a case where greedy matching returns fewer pairs than the maximum.
