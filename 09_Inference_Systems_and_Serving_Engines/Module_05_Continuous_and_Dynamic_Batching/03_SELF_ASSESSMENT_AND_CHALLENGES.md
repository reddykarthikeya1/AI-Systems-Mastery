# Module 05: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Scheduler CPU GIL Bottleneck under Micro-Steps
**Question**: An inference cluster running continuous batching achieves only 60% GPU utilization despite a deep waiting queue. Profiling shows that GPU kernel execution time is $8 \text{ ms}$ per step, while the Python scheduler loop takes $7.5 \text{ ms}$ per step to inspect request states and update batch tensors. How do you re-architect the scheduling pipeline to decouple GPU execution from CPU overhead?

**Solution**:
1. **Root Cause: Python Interpreter Latency**: Performing per-sequence Python object updates (`list.pop()`, dict lookups, string checks) inside the critical path of each decode step introduces CPU overhead that approaches the duration of the GPU kernel execution, causing GPU execution bubbles.
2. **Remedies**:
   - **Asynchronous Scheduling (Two-Thread Architecture)**: Run the scheduler in a dedicated CPU thread ahead of the GPU execution stream, submitting batches via a double-buffered queue.
   - **C++ Native Scheduler (e.g. vLLM C++ core / TensorRT-LLM)**: Port request state management to C++ using flat integer arrays and atomic bitsets.
   - **CUDA Graphs**: Capture static decode kernel execution graphs to eliminate CPU kernel launch overhead.

---

### Scenario 2: Starvation Mitigation under Extreme Prompt Lengths
**Question**: A continuous batch scheduler prioritizes admitting new prefills to maximize throughput. When a user submits a 32,000-token prompt, the prefill consumes all available KV cache blocks, forcing the engine to preempt and abort 12 in-flight decode requests. Formulate a memory-safe admission policy.

**Solution**:
1. **Strict Memory Budgeting**: Maintain a reserved "decode runway" buffer (e.g. 15% of physical blocks reserved exclusively for ongoing generation).
2. **Chunked Prefill**: Refuse to execute large prompts atomically. Slice the 32,000-token prefill into 512-token chunks and schedule them across 64 consecutive iterations, preserving memory for active decode requests.
