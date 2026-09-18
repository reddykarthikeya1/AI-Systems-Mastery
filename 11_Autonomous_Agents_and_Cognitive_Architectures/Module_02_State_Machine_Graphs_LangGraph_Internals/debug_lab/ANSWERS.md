# Debug Lab Solution & Forensic Post-Mortem

## Incident: State Machine Skips Every Node After the First and Corrupts Saved Checkpoints

---

### 🔍 Forensic Root Cause Analysis
Two independent defects live in the same three lines of `run()`:

```python
while curr != "END":
    state.update(self.nodes[curr](state))
    curr = "END"
```

First, `curr = "END"` is unconditionally executed at the bottom of the loop body on every iteration, regardless of what the node function actually returned. Each node here returns a `"next"` field naming the node that should run after it, but `run()` never reads that field -- it hardcodes termination after exactly one node, no matter how many nodes the graph defines or what any node's own routing decision says.

Second, `state.update(...)` mutates the caller-supplied dict in place rather than producing a new state object per step. A durable graph engine (in the spirit of LangGraph's checkpointing model) needs each step to yield an independent snapshot so a "before" checkpoint can be diffed or replayed against an "after" state. Because `update()` mutates the exact same dict object the caller already holds a reference to, any snapshot taken before `run()` is not actually a snapshot at all -- it is an alias that silently reflects post-run data the instant the mutation happens.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedGraphEngine:
    def __init__(self):
        self.nodes = {}

    def run(self, state, start):
        curr = start
        while curr != "END":
            update = dict(self.nodes[curr](state))
            next_node = update.pop("next", "END")
            state = {**state, **update}   # new dict every step -- no aliasing
            curr = next_node
        return state
```

The next node to visit now comes exclusively from the node function's own `"next"` field instead of being hardcoded, so the engine walks the full chain. Building a fresh dict each step (`{**state, **update}`) instead of mutating in place means any reference a caller held to an earlier state remains an independent, untouched snapshot.

---

### 🛡️ Production Prevention Invariants
1. **Routing Must Come From the Node, Never Be Hardcoded:** Every step transition should be driven exclusively by data the node function returns; a loop that always takes the same exit path regardless of that data is not implementing a graph at all.
2. **State Updates Must Not Alias:** State transitions should build a new object (or an explicit deep copy) per step, never mutate the object a caller may be holding a reference to.
3. **Checkpoint Immutability Test:** Add a regression test asserting that a state snapshot captured before a step's execution is unequal to, and not the same object as, the state returned after it.
