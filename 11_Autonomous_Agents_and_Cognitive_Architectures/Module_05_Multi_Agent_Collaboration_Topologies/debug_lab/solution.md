# Debug Lab Solution: Infinite Swarm Handoff Bug

### The Defect
`BrokenSwarm` delegates endlessly without a handoff ceiling or trajectory history.

### The Fix
Implement `max_handoffs` and handoff tracking as shown in `project_solution/multi_agent_swarm.py`.
