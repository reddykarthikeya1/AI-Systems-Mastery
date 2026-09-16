# Debug Lab Solution: False Efficiency on Failure Bug

### The Defect
`BrokenHarness` calculates `optimal / actual` even if the agent failed the task, rewarding agents that abort instantly.

### The Fix
Condition efficiency calculation strictly on `success == True` as shown in `project_solution/agent_eval_benchmark.py`.
