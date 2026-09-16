# Debug Lab Solution: Missing Safety Rails Bug

### The Defect
`BrokenColang` bypasses intent recognition and hazard classification entirely, exposing the backend model to severe safety violations.

### The Fix
Implement Llama Guard hazard auditing and canonical intent state routing as shown in `project_solution/nemo_colang_state_machine.py`.
