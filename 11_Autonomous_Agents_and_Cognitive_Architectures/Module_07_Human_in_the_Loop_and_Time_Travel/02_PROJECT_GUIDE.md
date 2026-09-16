# Project Guide: Building an Enterprise HITL and Time-Travel Engine

In this project, you will build an interactive state graph engine supporting breakpoint interrupts, human payload modification, and state rewind / branching.

---

## Three-Tier Implementation Path

### Tier 1: Breakpoint Interrupts & Suspended State
- Implement `interrupt_before` node gates.
- When an execution hits a breakpoint, pause execution and package a `PendingAction` descriptor.

### Tier 2: Resume with Human Modification
- Implement `resume(run_id, approved, payload_override)`.
- If approved, apply overrides and continue execution to the next node.

### Tier 3: Time-Travel Rewind & State Branching
- Implement `fork_from_checkpoint(checkpoint_id, state_edits)`.
- Re-run graph from the forked snapshot.
