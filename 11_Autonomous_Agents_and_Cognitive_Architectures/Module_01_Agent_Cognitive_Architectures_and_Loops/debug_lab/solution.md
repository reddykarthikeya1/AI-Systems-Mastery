# Debug Lab Solution: Action Loop Bug

### The Defect
In `BrokenReActEngine`, the loop runs `while True:` without maintaining a fingerprint hash of past actions or checking an iteration limit. If the LLM generates the same action repeatedly, the agent burns tokens infinitely.

### The Fix
Implement `_action_fingerprints` and `max_steps` ceiling as demonstrated in `project_solution/react_loop_sim.py`.
