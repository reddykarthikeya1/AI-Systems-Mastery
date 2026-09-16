# Debug Lab Solution: RCE Vulnerability

### The Defect
`BrokenCodeRunner` directly executes code inside the parent Python interpreter, allowing full host takeover.

### The Fix
Implement AST verification, subprocess separation, and timeout guards as shown in `project_solution/sandboxed_executor.py`.
