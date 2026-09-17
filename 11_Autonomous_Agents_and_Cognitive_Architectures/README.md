# Course 11: Autonomous Agents & Cognitive Architectures

Design, sandbox, orchestrate, and evaluate resilient autonomous multi-agent systems. Build ReAct loops, deterministic state machines, memory topologies, tool-calling pipelines, and consensus protocols.

---

## 1. Course Architecture & Mental Model

This course moves far beyond toy single-prompt completions to teach the engineering principles required to build, sandbox, orchestrate, and evaluate resilient autonomous systems:

```
                  +----------------------------------------------+
                  |           User Goal / Enterprise Query       |
                  +----------------------------------------------+
                                         |
                                         v
   +---------------------------------------------------------------------------+
   | Cognitive Control Loop (ReAct / Reflexion)                                |
   | - State Machine Graph (LangGraph / Pregel Supersteps)                      |
   | - Typed Tool Execution Engine & JSON Schema Dispatch                      |
   | - Hierarchical Memory: Working Context, Episodic Vectors, Reflections     |
   +---------------------------------------------------------------------------+
          |                               |                          |
          v                               v                          v
   [ Multi-Agent Swarms ]      [ Sandboxed Execution ]    [ Human-in-the-Loop ]
   - Handoff Routing           - AST Security Gate        - Approval Breakpoints
   - Consensus Debate          - Subprocess Quotas        - State Time Travel
          |                               |                          |
          +-------------------------------+--------------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |  Production Evaluation (SWE-bench / Metrics) |
                  +----------------------------------------------+
```

---

## 2. Module Index

| Module | Title | Core Focus | Project Solution |
| :--- | :--- | :--- | :--- |
| **01** | [Agent Cognitive Architectures & Loops](Module_01_Agent_Cognitive_Architectures_and_Loops/01_README.md) | ReAct, Reflexion, Cycle Detection, Trajectories | `react_loop_sim.py` |
| **02** | [State Machine Graphs & LangGraph](Module_02_State_Machine_Graphs_LangGraph_Internals/01_README.md) | Pregel Supersteps, Channel Reducers, Checkpointing | `pregel_graph_engine.py` |
| **03** | [Tool Execution & Constrained Generation](Module_03_Tool_Execution_and_Constrained_Generation/01_README.md) | Reflection Schema Generation, Type Coercion, Timeouts | `tool_execution_engine.py` |
| **04** | [Agent Memory Systems](Module_04_Agent_Memory_Systems/01_README.md) | Working Buffer, Episodic Multi-Factor Retrieval, Reflection | `agent_memory_manager.py` |
| **05** | [Multi-Agent Collaboration Topologies](Module_05_Multi_Agent_Collaboration_Topologies/01_README.md) | Swarm Handoffs, Supervisor Delegation, Consensus Debate | `multi_agent_swarm.py` |
| **06** | [Sandboxed Code Execution & Security](Module_06_Sandboxed_Code_Execution_and_Security/01_README.md) | AST Safety Filtering, Subprocess Isolation, Secret Redaction | `sandboxed_executor.py` |
| **07** | [Human-in-the-Loop & Time Travel](Module_07_Human_in_the_Loop_and_Time_Travel/01_README.md) | Interrupt Gates, Resume Overrides, Checkpoint Rewind | `hitl_time_travel_sim.py` |
| **08** | [Production Agent Evaluation](Module_08_Production_Agent_Evaluation/01_README.md) | SWE-bench Harness, Step Efficiency, Tool Accuracy | `agent_eval_benchmark.py` |

---

## 3. Verification & Grading Loop

Every module adheres strictly to the repository test contract:
```bash
# Run interactive quickstart demonstration across all modules
python 00_quickstart_interactive_demo.py

# Run full automated test suite
pytest 11_Autonomous_Agents_and_Cognitive_Architectures -v
ruff check 11_Autonomous_Agents_and_Cognitive_Architectures
```
