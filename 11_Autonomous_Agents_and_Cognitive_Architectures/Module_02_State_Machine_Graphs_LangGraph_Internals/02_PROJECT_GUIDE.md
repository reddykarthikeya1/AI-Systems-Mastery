# Project Guide: Building a Pregel Cyclic State Graph Engine

In this lab, you implement a standalone, zero-dependency version of the LangGraph execution engine.

---

## Implementation Milestones

### Tier 1: Core Pregel Engine & Reducers
- Implement `StateGraph` with support for typed channel reducers (e.g., `operator.add`, overwrite).
- Implement node registration and static directed edges.
- Execute nodes in sequential supersteps.

### Tier 2: Conditional Edges & Cyclic Routing
- Implement dynamic routing via `add_conditional_edge(source, router_func)`.
- Support cyclic graphs with an enforceable `recursion_limit` to prevent runaway recursion.

### Tier 3: State Checkpointing & Time Travel
- Implement `BaseCheckpointer` and in-memory snapshot store.
- Record every superstep with unique monotonically increasing version numbers.
- Add `rewind(step_id)` to restore past graph state and branch execution.
