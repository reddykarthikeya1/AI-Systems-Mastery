# Project Guide: Building an Enterprise ReAct & Reflexion Loop Engine

In this hands-on lab, you will implement an autonomous ReAct loop engine with cycle detection, reflexion triggers, and execution safety bounds.

---

## Three-Tier Implementation Path

### Tier 1: Core ReAct Cycle (Required)
- Implement `parse_agent_output(raw_text: str) -> ParsedStep`: Extracts Thought, Tool Name, Tool Arguments, or Final Answer using robust regex / structured delimiters.
- Implement `execute_step(step: ParsedStep) -> StepResult`: Safely invokes registered tools and captures observations.
- Build the iterative control loop bounded by `max_steps`.

### Tier 2: Cycle Detection & Reflexion (Advanced)
- Implement trajectory hashing: compute a deterministic signature for every tool call.
- Detect 2-cycles (A -> B -> A -> B) and immediate loops (A -> A).
- When a loop or exception occurs, generate a `ReflexionPrompt` that forces the agent to alter its trajectory.

### Tier 3: Production Telemetry & Context Management (Staff-Level)
- Implement context window budget trimming: prune observations older than $N$ steps while keeping the system prompt and goal intact.
- Emit JSONL traces of every step with execution latency, token counts, and outcome flags.
