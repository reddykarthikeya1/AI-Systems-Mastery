# Project Guide: Building a Multi-Agent Swarm and Debate Engine

In this lab, you implement an enterprise multi-agent collaboration engine supporting Swarm-style dynamic handoffs, supervisor delegation, and consensus debate voting.

---

## Three-Tier Implementation Path

### Tier 1: Swarm Agent Handoff Mechanism (Required)
- Implement `Agent` with tools and handoff targets.
- Implement `SwarmEngine.run()`: dynamically transfers execution when a tool returns an `AgentHandoff` signal.
- Enforce `max_handoffs` ceiling to prevent circular delegation.

### Tier 2: Hierarchical Supervisor Orchestrator (Advanced)
- Implement `SupervisorAgent` that decomposes user goals into sub-tasks and delegates to specialized worker agents in parallel.
- Aggregate worker outputs into a final synthesized response.

### Tier 3: Multi-Agent Debate & Consensus Voting (Staff-Level)
- Implement `run_debate(agents, topic, rounds=2)`: allows multiple personas to critique and refine responses.
- Implement majority voting / confidence-weighted consensus resolution.
