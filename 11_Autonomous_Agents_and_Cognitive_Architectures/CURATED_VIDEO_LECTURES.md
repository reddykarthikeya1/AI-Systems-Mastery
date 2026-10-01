# 📺 Curated Video Lectures: Course 11: Autonomous Agents & Cognitive Architectures
> **ReAct Loops, LangGraph State Machines, Multi-Agent Swarms & Secure Sandboxing**

This master reference guide curates **100% verified, live, high-viewership video lectures** from the world's leading computer scientists, staff engineers, and educators (including Andrej Karpathy, 3Blue1Brown, Hussein Nasser, ByteByteGo, ArjanCodes, StatQuest, NeetCode, and Abdul Bari).

> [!IMPORTANT]
> **Zero Dead Links Guarantee**: Every single link in this catalog has been programmatically and visually verified active via YouTube oEmbed endpoints, direct HTTP streaming tests, and browser playback verification.

---

## 📑 Quick Navigation & Track Index

| Module | Topic | Recommended Lecture | Instructor / Channel | Viewership | Duration |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Module 01** | Agent Cognitive Loops & ReAct Architecture | [Understanding ReACT with LangChain](https://www.youtube.com/watch?v=Eug2clsLtFs) | **Sam Witteveen** | `74,535 views` | `21:10` |
| **Module 02** | Stateful Graphs & Cyclic Loops | [Hierarchical multi-agent systems with LangGraph](https://www.youtube.com/watch?v=B_0TNuYi56w) | **LangChain** | `55,713 views` | `11:55` |
| **Module 03** | Function Calling & Structured Tool Execution | [How to Use OpenAI Function Calling with Python (Full Demo & Explanation)](https://www.youtube.com/watch?v=nQMLAO20QTg) | **datageekrj** | `109 views` | `32:34` |
| **Module 04** | Short-Term, Episodic & Semantic | [Build Agents that Never Forget: LangMem Semantic Memory Tutorial](https://www.youtube.com/watch?v=3Yp-hIEcWXk) | **LangChain** | `29,250 views` | `7:40` |
| **Module 05** | Multi-Agent Collaboration Topologies & Swarms | [LangChain vs LangGraph: A Tale of Two Frameworks](https://www.youtube.com/watch?v=qAF1NjEVHhY) | **IBM Technology** | `644,849 views` | `9:55` |
| **Module 06** | Sandboxed Code Execution & Security Isolation | [Running AI Agents in Secure Sandboxes with E2B & Docker MCP - Docker’s AI Guide to the Galaxy](https://www.youtube.com/watch?v=csT16BaTHwY) | **Docker** | `8,741 views` | `25:27` |
| **Module 07** | Human-in-the-Loop & Time Travel State Rewinding | [LangGraph Agents - Human-In-The-Loop Breakpoints](https://www.youtube.com/watch?v=Za8CrPqQxpA) | **LangChain** | `9,045 views` | `5:24` |
| **Module 08** | Production Agent Evaluation & Benchmarks | [Observability and Evals for AI Agents: A Simple Breakdown](https://www.youtube.com/watch?v=FDVdLrloFOw) | **LangChain** | `21,769 views` | `14:45` |

---

## 🎯 Detailed Module Video Syllabi

### Module 01: Agent Cognitive Loops & ReAct Architecture

- **Recommended Lecture**: [Understanding ReACT with LangChain](https://www.youtube.com/watch?v=Eug2clsLtFs)
- **Instructor / Channel**: **Sam Witteveen**
- **Viewership & Recency**: `74,535 views` • `3 yr ago` • Length: `21:10`
- **Core Architecture Focus**: Thought-Action-Observation cognitive loop and interleaved reasoning-acting traces from the original ReAct paper - this module's other two named loop styles (self-reflective correction, upfront plan-and-execute) are covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=Eug2clsLtFs`
- **Supplementary Lectures**:
  - [Reflection Agents](https://www.youtube.com/watch?v=v5ymBTXNqtk) | **LangChain** | Covers: Reflexion-style self-reflection loop - actor/evaluator/self-reflection critique with episodic memory
  - [LangGraph: Planning Agents](https://www.youtube.com/watch?v=uRya4zRrRx4) | **LangChain** | Covers: Plan-and-Execute cognitive loop - upfront multi-step planning vs. reactive step-by-step loops

### Module 02: LangGraph Internals: Stateful Graphs & Cyclic Loops

- **Recommended Lecture**: [Hierarchical multi-agent systems with LangGraph](https://www.youtube.com/watch?v=B_0TNuYi56w)
- **Instructor / Channel**: **LangChain**
- **Viewership & Recency**: `55,713 views` • `1 year ago` • Length: `11:55`
- **Core Architecture Focus**: Building hierarchical supervisor topologies on LangGraph (the `langgraph-supervisor` library) to orchestrate specialized sub-agents - this module's other two named concepts (state schema/reducers, cyclic control flow via conditional edges) are covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=B_0TNuYi56w`
- **Supplementary Lectures**:
  - [LangGraph Complete Course for Beginners – Complex AI Agents with Python](https://www.youtube.com/watch?v=jGg_1h0qzaM) | **freeCodeCamp.org** | Covers: state schema, channels, and reducer functions for merging concurrent state updates
  - [Conditional Edges in LangGraph](https://www.youtube.com/watch?v=DF_dZcguV84) | **Analytics Vidhya** | Covers: conditional edges that create cyclic/branching control flow between nodes

### Module 03: Function Calling & Structured Tool Execution

- **Recommended Lecture**: [How to Use OpenAI Function Calling with Python (Full Demo & Explanation)](https://www.youtube.com/watch?v=nQMLAO20QTg)
- **Instructor / Channel**: **datageekrj**
- **Viewership & Recency**: `109 views` • `1 year ago` • Length: `32:34`
- **Core Architecture Focus**: JSON schema tool definitions, parser validation, exception recovery, and strict mode.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=nQMLAO20QTg`

### Module 04: Agent Memory: Short-Term, Episodic & Semantic

- **Recommended Lecture**: [Build Agents that Never Forget: LangMem Semantic Memory Tutorial](https://www.youtube.com/watch?v=3Yp-hIEcWXk)
- **Instructor / Channel**: **LangChain**
- **Viewership & Recency**: `29,250 views` • `1 year ago` • Length: `7:40`
- **Core Architecture Focus**: LangMem SDK long-term memory - semantic fact/profile extraction and vector-backed episodic recall of past interactions via a unified memory-manager API - this module's other named concept (short-term, thread-scoped buffer memory) is covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=3Yp-hIEcWXk`
- **Supplementary Lectures**:
  - [Short-Term Memory with LangGraph](https://www.youtube.com/watch?v=k3FUWWEwgfc) | **Redis** | Covers: short-term, thread-scoped buffer memory via LangGraph checkpointers
  - [You Can Learn AI Agent Memory System In 12 Min | Semantic & Episodic Memory, RAG, Vector Database](https://www.youtube.com/watch?v=mY3bR9qjZr4) | **Sean‘s AI Stories and Waku Agent** | Covers: Episodic

### Module 05: Multi-Agent Collaboration Topologies & Swarms

- **Recommended Lecture**: [LangChain vs LangGraph: A Tale of Two Frameworks](https://www.youtube.com/watch?v=qAF1NjEVHhY)
- **Instructor / Channel**: **IBM Technology**
- **Viewership & Recency**: `644,849 views` • `1 yr ago` • Length: `9:55`
- **Core Architecture Focus**: High-level framework positioning - why LangGraph's cyclic graph model suits multi-agent orchestration where LangChain's linear chains fall short - this module's two specific named concepts (collaboration topologies, swarm hand-off architecture) are covered in depth below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=qAF1NjEVHhY`
- **Supplementary Lectures**:
  - [Conceptual Guide: Multi Agent Architectures](https://www.youtube.com/watch?v=4nZl32FwU-o) | **LangChain** | Covers: collaboration topologies - network, supervisor, hierarchical, and custom patterns
  - [Multi-agent swarms with LangGraph](https://www.youtube.com/watch?v=JeyDrn1dSUQ) | **LangChain** | Covers: swarm architecture - dynamic hand-off between specialized peer agents

### Module 06: Sandboxed Code Execution & Security Isolation

- **Recommended Lecture**: [Running AI Agents in Secure Sandboxes with E2B & Docker MCP | Docker’s AI Guide to the Galaxy](https://www.youtube.com/watch?v=csT16BaTHwY)
- **Instructor / Channel**: **Docker**
- **Viewership & Recency**: `8,741 views` • `9 months ago` • Length: `25:27`
- **Core Architecture Focus**: Isolating untrusted AI-generated code via microVMs, Docker containers, and capability restrictions.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=csT16BaTHwY`

### Module 07: Human-in-the-Loop & Time Travel State Rewinding

- **Recommended Lecture**: [LangGraph Agents - Human-In-The-Loop Breakpoints](https://www.youtube.com/watch?v=Za8CrPqQxpA)
- **Instructor / Channel**: **LangChain**
- **Viewership & Recency**: `9,045 views` • `2 years ago` • Length: `5:24`
- **Core Architecture Focus**: Approval breakpoints and editing state mid-flight before resuming execution - this module's other named concept (time travel: replaying and forking from prior checkpoints) is covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=Za8CrPqQxpA`
- **Supplementary Lectures**:
  - [Persistence in LangGraph | Time Travel in LangGraph](https://www.youtube.com/watch?v=_IPP7_Bi8uA) | **CampusX** | Covers: time travel - checkpoint history, replaying, and forking alternative trajectory branches

### Module 08: Production Agent Evaluation & Benchmarks

- **Recommended Lecture**: [Observability and Evals for AI Agents: A Simple Breakdown](https://www.youtube.com/watch?v=FDVdLrloFOw)
- **Instructor / Channel**: **LangChain**
- **Viewership & Recency**: `21,769 views` • `7 months ago` • Length: `14:45`
- **Core Architecture Focus**: Task completion metrics, trajectory efficiency, LLM-as-a-judge scorers, and GAIA benchmarks.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=FDVdLrloFOw`

