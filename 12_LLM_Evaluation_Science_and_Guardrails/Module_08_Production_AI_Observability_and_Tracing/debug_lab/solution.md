# Debug Lab Solution: Missing Telemetry & Cost Bug

### The Defect
`BrokenTracer` records only raw tokens, ignoring latency breakdowns (TTFT/TPOT) and dollar cost calculation.

### The Fix
Implement OTel GenAI attributes, monotonic duration timing, and pricing tables as shown in `project_solution/genai_telemetry_tracer.py`.
