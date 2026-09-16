# Debug Lab Solution: Synchronous Blocking Bug

### The Defect
`BrokenHITL` halts the thread using blocking CLI input, preventing scaling or persistence across restarts.

### The Fix
Implement non-blocking suspension and state serialization as shown in `project_solution/hitl_time_travel_sim.py`.
