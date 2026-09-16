# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is the Swarm handoff pattern more token-efficient than a centralized supervisor in linear workflows?
   - *Answer*: In Swarm handoffs, the active agent directly transfers control without passing messages back through an intermediate coordinator prompt, cutting LLM call count in half.
2. How do you prevent two agents from entering an infinite handoff ping-pong loop?
   - *Answer*: Track the sequence of active agents in a call stack and terminate with an error or fallback if the same agent sequence repeats or exceeds `max_handoff_depth`.
3. What is the primary benefit of multi-agent debate over Single-Agent Self-Consistency?
   - *Answer*: Different agent personas (with divergent system prompts and few-shot biases) avoid shared blind spots and challenge each other's assumptions.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Multi-Agent Coding Swarm with Stale State
**Context**: A 4-agent development swarm (Planner, Architect, Coder, Tester) modifies a shared Git repository. The Coder makes edits based on a design the Planner invalidated 2 minutes prior.
**Question**: Design a synchronization and conflict-resolution mechanism that prevents stale state divergence in asynchronous multi-agent swarms.
**Solution**:
1. Implement a shared monotonic State Version Vector $\vec{V}$.
2. Every task dispatch includes the target version $V_{\text{target}}$.
3. If an agent attempts to commit code against an invalidated version, the commit is rejected with a `StateDivergence` exception, forcing the agent to pull the latest state and replan.
