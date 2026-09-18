# Debug Lab Incident Report: State Machine Skips Every Node After the First and Corrupts Saved Checkpoints

- **Severity:** P1 Workflow Correctness
- **Affected Subsystem:** Module_02_State_Machine_Graphs_LangGraph_Internals
- **Reported Impact:** A three-step approval workflow (draft -> review -> publish) silently stopped after the draft step in production, with no error raised. Separately, an audit tool that snapshots state before each node runs (for replay/rollback) found its "before" snapshots had already been overwritten with "after" data, making time-travel debugging impossible.

---

## 🚨 Observable Symptoms & Logs
```text
Graph defined as: A -> B -> C -> END (3 nodes before END)
Path actually executed: ['A']
Node the graph stopped at after one run() call: END (graph engine says done)
Checkpoint captured BEFORE run() was called still reads: ['A']
Is the pre-run checkpoint the exact same object as the post-run state? True
```
The graph was wired as a three-node chain, A -> B -> C -> END, and each node function returns a `"next"` field telling the engine which node to visit next. `BrokenGraphEngine.run()` reports success (it returns normally, no exception), but the executed path shows only `A` ever ran -- `B` and `C` never fired even though the graph explicitly points to them. Separately, a reference to the state dict captured *before* `run()` was called (`checkpoint`) reads the *post-run* value, and `checkpoint is result` is `True` -- the "before" snapshot and the "after" result are literally the same object in memory.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_State_Machine_Graphs_LangGraph_Internals/debug_lab
   ```
2. `broken_graph.py` only defines `BrokenGraphEngine`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_graph import BrokenGraphEngine

   def node_a(state):
       return {"path": state["path"] + ["A"], "next": "B"}

   def node_b(state):
       return {"path": state["path"] + ["B"], "next": "C"}

   def node_c(state):
       return {"path": state["path"] + ["C"], "next": "END"}

   engine = BrokenGraphEngine()
   engine.nodes = {"A": node_a, "B": node_b, "C": node_c}

   state = {"path": []}
   checkpoint = state  # a caller holding a reference to the "before" state, e.g. for undo/replay

   result = engine.run(state, "A")

   print("Graph defined as: A -> B -> C -> END (3 nodes before END)")
   print(f"Path actually executed: {result['path']}")
   print("Node the graph stopped at after one run() call: END (graph engine says done)")
   print(f"Checkpoint captured BEFORE run() was called still reads: {checkpoint['path']}")
   print(f"Is the pre-run checkpoint the exact same object as the post-run state? {checkpoint is result}")
   ```
3. Observe that `path` only ever contains `'A'` despite the graph defining three nodes, and that the object held before the call and the object returned after the call are identical, not two independent snapshots.

---

## 🎯 Your Objective
1. Inspect the `while` loop in `run()` and identify what value `curr` is assigned on every single iteration, regardless of what the node function itself returned.
2. Compare the `state` object passed into `run()` with the object returned from it -- are they the same object, and what does `state.update(...)` do to the object it's called on?
3. Formulate a hypothesis for why only one node ever executes, and why an externally held reference to "the state before `run()`" changes anyway, then check `ANSWERS.md`.
