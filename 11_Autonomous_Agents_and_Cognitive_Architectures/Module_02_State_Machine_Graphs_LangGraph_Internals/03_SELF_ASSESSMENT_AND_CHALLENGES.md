# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge
1. Why is Pregel superstep execution superior to naive asyncio event loops for agent state?
   - *Answer*: Determinism. All nodes read from an immutable snapshot of the prior superstep, eliminating dirty reads and race conditions.
2. How do channel reducers resolve concurrent state updates from parallel nodes?
   - *Answer*: Instead of mutating state directly, parallel nodes yield delta values that are combined deterministically by a single reducer function (e.g., list append or mathematical summation).
3. What is the role of the `END` pseudo-node?
   - *Answer*: It serves as the terminal sink in the directed graph, signaling the execution engine to halt superstep scheduling and return the final state.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Scaling Distributed Agent Checkpoints to 100,000 Concurrent Users
**Context**: An enterprise customer support platform runs LangGraph agents for 100k concurrent active calls. Checkpointing every single tool call to PostgreSQL creates write IOPS saturation.
**Question**: Architect a multi-tiered checkpointing strategy that guarantees zero lost state while reducing database write load by 90%.
**Solution**:
1. Store intra-session supersteps in an in-memory Redis ring buffer with write-behind persistence.
2. Flush to durable PostgreSQL only at critical state transitions: external API tool calls, Human-in-the-Loop breakpoints, and session termination.
3. Use delta-compression for state snapshots, storing only JSON diffs against the initial session state rather than full context copies.
