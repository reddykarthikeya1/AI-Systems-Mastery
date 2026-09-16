# Course 11: Master Syllabus & Learning Outcomes

## Detailed Module Breakdown

### Module 01: Agent Cognitive Architectures and Loops
- **Theoretical Foundations**: POMDP formulations, ReAct (Reasoning + Acting), Plan-and-Solve decomposition, Reflexion retrospective critique.
- **Systems Architecture**: Infinite loop detection, action fingerprint hashing, trajectory logging.
- **Laboratory**: Implementing `ReActLoopEngine` with cycle detection and reflexion triggers.

### Module 02: State Machine Graphs & LangGraph Internals
- **Theoretical Foundations**: Google Pregel computation model, Bulk Synchronous Parallel (BSP) supersteps, immutable state snapshots.
- **Systems Architecture**: Typed channel reducers (`operator.add`, overwrite), conditional edges, recursion limit guards.
- **Laboratory**: Implementing `PregelGraphEngine` with state checkpointer and time-travel rewind.

### Module 03: Tool Execution and Constrained Generation
- **Theoretical Foundations**: Grammar-based decoding (CFGs), JSON Schema validation, logit bias masking.
- **Systems Architecture**: Introspecting Python type hints, automatic schema generation, thread timeout bounds.
- **Laboratory**: Implementing `ToolExecutionEngine` with argument coercion and execution guards.

### Module 04: Agent Memory Systems
- **Theoretical Foundations**: Working vs Episodic vs Semantic memory, Stanford Generative Agents retrieval formulation.
- **Systems Architecture**: Multi-factor scoring ($Score = \alpha \cdot \text{recency} + \beta \cdot \text{importance} + \gamma \cdot \text{relevance}$), reflection consolidation.
- **Laboratory**: Implementing `AgentMemoryManager`.

### Module 05: Multi-Agent Collaboration Topologies
- **Theoretical Foundations**: Supervisor-Worker, Swarm dynamic handoffs, multi-agent debate and majority consensus.
- **Systems Architecture**: Call stack depth ceilings, context filtering across handoffs.
- **Laboratory**: Implementing `SwarmEngine` and multi-agent debate consensus.

### Module 06: Sandboxed Code Execution and Security
- **Theoretical Foundations**: Threat modeling, Indirect Prompt Injection, sandbox escape vectors (`__subclasses__`).
- **Systems Architecture**: AST static analysis, subprocess isolation, wall-clock timeouts, regex secret redaction.
- **Laboratory**: Implementing `SandboxedExecutor`.

### Module 07: Human-in-the-Loop and Time Travel
- **Theoretical Foundations**: Breakpoint interrupts, human approval gates, optimistic execution rollback.
- **Systems Architecture**: Non-blocking suspended state persistence, payload modification, branching time-travel.
- **Laboratory**: Implementing `HITLEngine`.

### Module 08: Production Agent Evaluation
- **Theoretical Foundations**: Benchmark design (SWE-bench, WebArena, GAIA), pass@k formulation.
- **Systems Architecture**: Trajectory analysis, Step Efficiency Score, Tool Call Precision, automated regression suite.
- **Laboratory**: Implementing `AgentBenchmarkHarness`.
