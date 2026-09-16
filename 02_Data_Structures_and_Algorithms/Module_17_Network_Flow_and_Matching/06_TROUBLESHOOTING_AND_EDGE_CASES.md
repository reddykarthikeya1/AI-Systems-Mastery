# Troubleshooting - Module 17

## The answer is too small on some graphs and right on others

You are not crediting the residual edge. `cap[e] -= f` without `cap[e ^ 1] += f`
gives correct answers on any graph that never needs to reroute - which includes
most simple test cases, and none of the interesting ones. See the four-node
graph in the README.

## The answer is too large

You added each edge twice, once in each direction, turning a directed graph into
an undirected one. `add_edge` already creates the reverse entry - at capacity 0,
deliberately. Debug lab defect 1.

## The minimum cut comes back empty

Reachability is being computed over the original capacities instead of the
residual ones. Debug lab defect 2. The check that catches it: cut capacity must
equal the flow.

## My cut differs from the expected one but has the same capacity

Both are correct. A graph can have several minimum cuts. The tests expect the
*source-minimal* one, which is what residual exploration from the source
produces.

## `min_cut` returns 0 the second time I call it

The network still has the first run's flow in it. This engine's `min_cut` calls
`reset()` first for exactly that reason. If you write your own, decide whether it
resets and document it - a function whose answer depends on whether it has been
called before is a trap.

## Dinic recurses too deeply

The blocking-flow DFS is recursive here for readability. On a graph with a very
long path it can exceed Python's recursion limit. Rewrite it with an explicit
stack, or raise the limit knowingly - do not silently bump it in library code.

## Bipartite matching assigns one worker several jobs

The source-to-worker capacity is not 1. Debug lab defect 3. Note that the total
count still comes out right, so only a test that checks the *shape* of the
answer catches it.

## Infinite loop

Some edge has negative residual capacity, so `capacity > 0` keeps finding a path
that pushes nothing. That happens if your bottleneck is not the minimum over the
whole path - check you are taking `min` across every edge, not just the last one.

## Float capacities

Do not. Ford-Fulkerson with irrational capacities can fail to terminate, and
with floats you get the practical version of that: an augmenting path of
`1e-17`, forever. Scale to integers.

## Very large capacities

`10^9` per edge is fine; the running time of Edmonds-Karp depends on `V` and `E`,
not the capacity values. Plain Ford-Fulkerson does depend on them, which is one
more reason to use BFS.
