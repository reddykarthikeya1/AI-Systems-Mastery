# Debug Lab 17 - Answers

Read only after writing your own diagnosis for all three.

---

## Defect 1 - every one-way link added in both directions

**Where:** `route_shipments`.

```python
for a, b, capacity in links:
    network.add_edge(a, b, capacity)
    network.add_edge(b, a, capacity)      # <-- makes the link two-way
```

**Why it produces that output.** `add_edge` already creates the residual
partner - an edge of capacity **0** going the other way, which exists purely so
flow can be taken back. Adding a second real edge with the full capacity turns
every one-way road into a two-way road.

With that, the route `0 -> 1 -> 2 -> 3` becomes usable by driving the wrong way
up link `(2, 1)`. That is 3 containers that cannot legally move, on top of the
2 that can, giving the reported 5. The true answer is **2**: only `0 -> 4 -> 3`
is a legal path.

**The fix.** Add each link once:

```python
for a, b, capacity in links:
    network.add_edge(a, b, capacity)
```

If you genuinely want an undirected edge, the correct encoding is one call with
capacity in both the forward and residual slot - not two calls.

**The general lesson.** The residual edge is not a road. It is an accounting
entry that lets the algorithm change its mind. Confusing the two silently
converts your directed model into an undirected one, and the answer comes back
too *large* - which is the dangerous direction, because a capacity plan that
overstates throughput is the one that fails in production.

---

## Defect 2 - the cut computed from original capacities

**Where:** `find_bottleneck_links`, the reachability search.

```python
if not reachable[nxt] and network.original[edge_id] > 0:
```

**Why it produces that output.** The minimum cut is found by asking which nodes
are still reachable from the source *once the flow is saturated*. That question
is about **residual** capacity - what is left. Asking it with `original` is
asking which nodes were reachable before anything happened, which for a
connected graph is all of them.

If every node is reachable, no edge has a reachable tail and an unreachable
head, so the crossing set is empty. Hence a cut of no links with a capacity of
0, next to a max flow of 2.

**The fix.** One word:

```python
if not reachable[nxt] and network.capacity[edge_id] > 0:
```

**The general lesson.** There is a free correctness check here and it costs two
lines: the capacity of the cut you return must equal the flow you computed.
Assert it. Max-flow min-cut is a theorem, so any discrepancy is a bug in your
code and never a property of the input - and this lab shows the discrepancy is
visible immediately if you bother to look.

---

## Defect 3 - the source edges have capacity 2

**Where:** `assign_drivers`.

```python
for driver in range(drivers):
    network.add_edge(source, driver, 2)     # <-- should be 1
```

**Why it produces that output.** In the flow formulation, the edge from the
super-source into a driver is the only thing that limits how many routes that
driver can take. One unit of flow is one assignment; a capacity of 2 says "this
driver may take two routes".

The route side is still capped at 1, so no route is double-staffed and the
total is still 2 - the maximum. That is exactly why it looks fine: the headline
number is right and only the distribution is wrong.

**The fix.**

```python
network.add_edge(source, driver, 1)
```

**The general lesson.** Reductions fail quietly. The algorithm was correct
throughout - it computed the true maximum flow of the network it was given.
The network just did not mean what the author thought it meant.

When you model a problem as flow, write down what one unit of flow *is* and
what each capacity *forbids*, then check every capacity against that sentence.
And test the shape of the answer, not only its size: an assertion that no
driver appears twice would have caught this on the first run.
