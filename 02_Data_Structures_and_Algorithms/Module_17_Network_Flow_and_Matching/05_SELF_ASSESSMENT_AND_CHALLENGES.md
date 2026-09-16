# Self-Assessment - Module 17

## Quiz

1. What does a residual edge of capacity 5 from `b` to `a` mean? Is it a road?
2. Draw the smallest graph where a greedy augmenting path must be undone.
3. Why does Edmonds-Karp insist on the *shortest* augmenting path?
4. What is a level graph, and what does the `progress` pointer prevent?
5. State max-flow min-cut. How do you use it as a check on your own code?
6. You have a saturated flow. Give the procedure for reading off the minimum
   cut, and say which capacities the reachability search uses.
7. A graph has two different minimum cuts. Which does residual exploration from
   the source return?
8. Model "assign 5 drivers to 8 routes, one route each" as a flow network. What
   is one unit of flow?
9. Flow has no node capacities. How do you impose one?
10. Greedy matching returned 3 pairs and the maximum is 4. What did greedy do?

## Challenges

**A. Min-cost max-flow.** Add a cost per unit to every edge and find the cheapest
maximum flow, using Bellman-Ford (costs may be negative on residual edges) to
choose the cheapest augmenting path rather than the shortest. This is the
assignment problem in general form.

**B. Sports elimination.** Given current standings and the remaining fixtures,
decide whether a given team can still finish top. Model the remaining games as
flow into a sink, and let the minimum cut tell you which set of teams makes it
impossible.

**C. Scaling.** Implement capacity scaling: only consider edges with residual
capacity at least `delta`, starting at the largest power of two and halving.
Show on a graph with capacities around `10^9` that it beats plain Edmonds-Karp,
and explain why the improvement depends on the capacity magnitudes rather than
the graph size.
