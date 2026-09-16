# Project Guide - Module 17

Build the flow engine in [`starter/network_flow_engine.py`](starter/network_flow_engine.py).

```bash
cd starter
python -m pytest ../project_solution -q      # must FAIL until you write the code
```

## Tier 1 - the graph and one algorithm

1. `FlowNetwork.__init__` and `add_edge`. Get the paired-edge layout right: edge
   `i` and its residual partner `i ^ 1`, the partner starting at capacity 0.
   Everything else depends on this.
2. `flow_on` and `reset`.
3. `edmonds_karp`. BFS for a path, find its bottleneck, push, repeat.

Check yourself on the textbook graph: the answer is 23.

## Tier 2 - the theorem

4. `min_cut`. Run the flow, then explore the residual graph from the source.
   Assert that the capacities of your cut sum to the flow before you move on.

## Tier 3 - the faster algorithm and the reductions

5. `dinic`. Level graph by BFS, blocking flow by DFS, and the `progress` pointer
   so no edge is retried within a phase.
6. `bipartite_matching` and `greedy_matching`.
7. `max_profit_projects`. The middle edges need effectively infinite capacity -
   work out why before writing it.

## Checkpoints

- After tier 1: `test_textbook_network` and
  `test_flow_must_be_undone_to_reach_the_optimum`. The second is the one that
  fails if you forgot the residual credit.
- After tier 2: `test_min_cut_edges_really_disconnect_the_sink`.
- After tier 3: `test_edmonds_karp_and_dinic_agree_on_random_graphs`, 300 random
  graphs cross-checking your two algorithms against each other.

## If you are stuck

Print the residual capacities after each augmentation on a four-node graph. If a
backward edge never becomes non-zero, you have not written the `cap[e ^ 1] +=`
line, and every test that needs a reroute will fail while the simple ones pass.
