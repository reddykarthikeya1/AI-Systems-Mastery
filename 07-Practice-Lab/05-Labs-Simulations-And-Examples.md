# Labs, Simulations and Runnable Examples

> Everything here runs offline with Python 3.10 or newer. Each script prints what it demonstrates and ends with assertions, so a clean exit means the claim held on your machine. Run them from the repository root.

## Python (Track 1)

| Script | What it shows | Run |
| :--- | :--- | :--- |
| `01-Python-Mastery/labs/01_race_condition_hunter.py` | ================================================================================ LAB 01: Multi-Threaded Race Condition Hunter & Fix ==================================================================== | `python 01-Python-Mastery/labs/01_race_condition_hunter.py` |
| `01-Python-Mastery/labs/02_async_starvation_lab.py` | ================================================================================ LAB 02: Asyncio Event Loop Starvation & Threadpool Offloading ========================================================= | `python 01-Python-Mastery/labs/02_async_starvation_lab.py` |
| `01-Python-Mastery/labs/03_memory_leak_debugger.py` | ================================================================================ LAB 03: Memory Leak Hunting & Tracemalloc Profiling =================================================================== | `python 01-Python-Mastery/labs/03_memory_leak_debugger.py` |
| `01-Python-Mastery/labs/04_measure_memory_claims.py` | Lab 4: measure the memory claims made in Chapter 5 on YOUR Python version. | `python 01-Python-Mastery/labs/04_measure_memory_claims.py` |
| `01-Python-Mastery/labs/05_benchmarks.py` | Benchmarks behind the performance numbers quoted in the chapters. | `python 01-Python-Mastery/labs/05_benchmarks.py` |

## Low-Level Design (Track 2)

| Script | What it shows | Run |
| :--- | :--- | :--- |
| `02-Low-Level-Design/labs/01_concurrency_stress_test.py` | =============================================================================== LLD Concurrency Lab: Readers-Writer Lock (RWLock) vs Standard Mutex Benchmark ========================================== | `python 02-Low-Level-Design/labs/01_concurrency_stress_test.py` |

## High-Level Design (Track 3)

| Script | What it shows | Run |
| :--- | :--- | :--- |
| `03-High-Level-Design/simulations/bloom_filter.py` | =============================================================================== Bloom Filter Simulator & Mathematical Verifier ========================================================================= | `python 03-High-Level-Design/simulations/bloom_filter.py` |
| `03-High-Level-Design/simulations/consistent_hashing_ring.py` | ================================================================================ SIMULATION 01: Consistent Hash Ring with Virtual Nodes ================================================================ | `python 03-High-Level-Design/simulations/consistent_hashing_ring.py` |
| `03-High-Level-Design/simulations/distributed_rate_limiter.py` | =============================================================================== Distributed Rate Limiter Simulator: Sliding Window Log vs Token Bucket ================================================= | `python 03-High-Level-Design/simulations/distributed_rate_limiter.py` |
| `03-High-Level-Design/simulations/raft_consensus_simulator.py` | ================================================================================ SIMULATION 02: Raft Distributed Consensus Simulator (Leader Election) ================================================= | `python 03-High-Level-Design/simulations/raft_consensus_simulator.py` |

## Agentic AI (Track 4)

| Script | What it shows | Run |
| :--- | :--- | :--- |
| `04-Agentic-AI/simulations/pure_python_hnsw.py` | =============================================================================== Hierarchical Navigable Small World (HNSW) Pure-Python Vector Index ===================================================== | `python 04-Agentic-AI/simulations/pure_python_hnsw.py` |
| `04-Agentic-AI/examples/ex01_tool_loop.py` | Example 1: a ReAct-style tool-calling loop with budgets, error handling and loop detection. | `python 04-Agentic-AI/examples/ex01_tool_loop.py` |
| `04-Agentic-AI/examples/ex02_langgraph_hitl.py` | Example 2: a real LangGraph agent: typed state + reducers, a tool loop, a checkpointer, and a human approval interrupt (human-in-the-loop) that resumes where it paused. | `python 04-Agentic-AI/examples/ex02_langgraph_hitl.py` |
| `04-Agentic-AI/examples/ex03_hybrid_rag.py` | Example 3: a complete, dependency-free hybrid RAG retrieval pipeline with evaluation. | `python 04-Agentic-AI/examples/ex03_hybrid_rag.py` |
| `04-Agentic-AI/examples/ex04_mcp_server.py` | Example 4: a real MCP server (official Python SDK, mcp==2.3.0). | `python 04-Agentic-AI/examples/ex04_mcp_server.py` |
| `04-Agentic-AI/examples/ex05_eval_harness.py` | Example 5: an agent evaluation harness: repeated trials, pass@k vs pass^k, confidence intervals. | `python 04-Agentic-AI/examples/ex05_eval_harness.py` |

## DSA (Track 5)

| Script | What it shows | Run |
| :--- | :--- | :--- |
| `05-DSA-Interview-Playbook/simulations/run_all_dsa_benchmarks.py` | =============================================================================== DSA Core Patterns Test Runner & Verification Suite ===================================================================== | `python 05-DSA-Interview-Playbook/simulations/run_all_dsa_benchmarks.py` |

## Agentic examples: the test suite

```text
pip install -r 04-Agentic-AI/examples/requirements.txt
cd 04-Agentic-AI/examples && pytest -q
```

The examples use a scripted fake model, so no API key is needed. Real providers are reached through `llm.py` (`LLM_PROVIDER=anthropic` or `openai`, plus `LLM_MODEL`); both adapters are unit-tested with stub clients only.

## Optional local services for the Python labs

`01-Python-Mastery/labs/docker-compose.yml` starts Postgres, Redis and Kafka for readers who want to run the database, queue and streaming chapters against real services. It is optional: every chapter has an offline version.

