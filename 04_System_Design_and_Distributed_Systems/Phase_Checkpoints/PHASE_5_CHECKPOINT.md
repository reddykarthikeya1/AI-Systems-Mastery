# Phase Checkpoint: Modern AI/ML Systems & High-Scale LLM Serving

> **Phase Scope:** Modules 21–22 (Vector Databases & HNSW Indexing, Distributed LLM Serving & PagedAttention)  
> **Allocated Exam Duration:** 90 Minutes  
> **Evaluation Mode:** Closed-solution, timed architectural defense, capacity math drill, and code audit.

---

## 🎯 The Exam Mission: Architect an Enterprise Retrieval-Augmented Generation (RAG) & LLM Serving Platform

### Executive Scenario
You are the Principal AI Systems Engineer at an enterprise AI platform.
The platform indexes 50,000,000 high-dimensional document embedding vectors (1536-dim, OpenAI text-embedding-3-large) and serves concurrent LLM inference queries across an internal cluster of NVIDIA H100 GPUs.
You must design the Approximate Nearest Neighbor (ANN) vector retrieval pipeline and the high-throughput continuous-batching LLM inference serving engine.

---

## 🏛️ Reference Architectural Blueprint (C4 Container View)

```

                      [ User Query: 'Summarize quarterly earnings...' ]
                                             |
                                 Embedding Generation API
                                             v
               +---------------------------------------------------------+
               |              HNSW Vector Retrieval Engine               |
               |                                                         |
               |   Top Layer (Skip Highway)    (Node 1) ---------> (Node 8)|
               |                                  |                   |  |
               |   Dense Layer 0 (Ground)      (Node 1)->(Node 2)->(Node 8)|
               |                                                         |
               |   Quantization: SQ8 (8-bit compressed vectors in RAM)   |
               +---------------------------------------------------------+
                                             |
                                Top-K Context Chunks
                                             v
               +---------------------------------------------------------+
               |              vLLM Serving Inference Engine              |
               |                                                         |
               |  [ Continuous Batching Scheduler (Iteration-Level) ]    |
               |                            |                            |
               |                            v                            |
               |  [ PagedAttention Non-Contiguous Block Memory Manager ]  |
               |        Logical Tokens -> Virtual Page Table             |
               |                            |                            |
               |                            v                            |
               |  [ Physical GPU VRAM Pools (8x H100 80GB SXM5) ]        |
               +---------------------------------------------------------+

```

---

## 📋 Hard Engineering & Scale Specifications

### 1. Functional Requirements
- **Vector Search Engine:** Build an HNSW index supporting Euclidean and Cosine distance with 8-bit Scalar Quantization (SQ8).
- **Target Recall & Latency:** Achieve $\ge 95\%$ recall@10 with query latency $< 10\text{ms}$ on 50M vectors.
- **PagedAttention KV-Cache Manager:** Implement non-contiguous physical block memory management for autoregressive LLM decoding (vLLM architecture).
- **Continuous Batching Scheduler:** Implement iteration-level batching dynamically interleaving new request Prefill steps with running Decode iterations.
- **GPU Preemption Engine:** Manage GPU Out-of-Memory (OOM) pressure by preempting victim requests via block swapping or prompt recomputation.

### 2. Non-Functional & Hardware Scale Constraints
- **GPU Cluster:** 8x NVIDIA H100 GPUs (80GB VRAM each = 640GB total GPU memory).
- **Vector RAM Budget:** 50,000,000 vectors $	imes$ 1536 float32 dimensions $= 307.2 \text{ GB}$ uncompressed. Must compress via SQ8 to $\le 80 \text{ GB RAM}$.
- **Serving Throughput:** Sustain 500 concurrent active generation streams without GPU memory fragmentation crashes.

---

## 🧮 Quantitative Physics & Mathematical Formulations

### AI Hardware & Memory Calculus
1. **Uncompressed Vector Footprint:**
   $$50,000,000 \text{ vectors} \times 1536 \text{ dims} \times 4 \text{ bytes (float32)} = 307.2 \times 10^9 \text{ bytes} \approx 307.2 \text{ GB}.$$
2. **Scalar Quantization (SQ8) Footprint:**
   $$50,000,000 \text{ vectors} \times 1536 \text{ dims} \times 1 \text{ byte (uint8)} = 76.8 \text{ GB} \implies \mathbf{75\% \text{ memory reduction}}!$$
   Plus min/max scale float32 values per vector ($50M \times 8 \text{ bytes} = 400 \text{ MB}$).
3. **HNSW Graph Link Memory:** With $M = 32$ links per node on Layer 0:
   $$50,000,000 \times 32 \times 4 \text{ bytes} = 6.4 \text{ GB RAM}.$$
4. **KV-Cache Memory Per Token (LLaMA-70B, 80 layers, 64 heads, 128 head_dim, float16):**
   $$\text{Memory per token} = 2 \times 2 \times n_{\text{layers}} \times d_{\text{model}} = 4 \times 80 \times 8192 = 2,621,440 \text{ bytes} \approx \mathbf{2.62 \text{ MB per token}}.$$
   A 2048-token request consumes:
   $$2048 \times 2.62 \text{ MB} \approx 5.37 \text{ GB VRAM} \text{ just for KV cache}!$$
   Under static allocation, 15 concurrent requests exhaust an entire 80GB GPU. PagedAttention eliminates the 60% internal fragmentation waste.

---

### 💥 AI Serving Outage & Edge Scenarios
1. **GPU Memory Thrashing on Long Prompt Bursts:** 50 requests with 3,000-token prompts arrive simultaneously. Available GPU VRAM drops to 0. Your scheduler must preempt lower-priority requests using swap or prompt recomputation without crashing the server process.
2. **HNSW Vector Recall Collapse Under Outliers:** Adding unnormalized embedding vectors with extreme values expands the quantization range, compressing 99% of normal vector dimensions into 2 integer bins. Your engine must apply percentile clipping before SQ8 mapping.
3. **Draft Model Divergence in Speculative Decoding:** The small draft model outputs tokens that the large verification model repeatedly rejects (0% acceptance rate), doubling inference latency. Your engine must dynamically fall back to standard decoding.

---

## 📊 100-Point Comprehensive Grading Rubric

| Dimension | Evaluation Criteria | Maximum Points |
| :--- | :--- | :---: |
| **Vector Geometry & Quantization** | Distance metrics, SQ8 min/max calibration, and percentile clipping for outlier handling | 20 pts |
| **HNSW Graph Mechanics** | Skip-list hierarchy, greedy routing, Beam Search, and $efSearch$ vs recall tuning | 20 pts |
| **KV-Cache Memory Calculus** | Prefill vs Decode phases, layer-head memory sizing, and fragmentation root cause analysis | 20 pts |
| **PagedAttention Architecture** | Logical-to-physical block table translation and zero internal memory fragmentation | 20 pts |
| **Continuous Batching & Preemption**| Iteration-level scheduling, slot filling, and swap vs. recompute preemption policies | 20 pts |

**Passing Gate Threshold:** **85 / 100 Points** is required to officially certify and unlock the next phase.

---

## 🎙️ Diagnostic Oral Defense Questions (Staff-Level Panel)

Prepare to answer and defend these exact questions on a whiteboard during the review panel:

1. **Why is Exact kNN search ($O(N \cdot D)$) computationally prohibitive for 50M vectors, and how does HNSW achieve sub-linear $O(\log N)$ search time?**
2. **Explain the mathematical reason why Autoregressive Decode is memory-bandwidth-bound while Prefill is compute-bound.**
3. **How does PagedAttention mirror operating system virtual memory paging with page tables and physical page frames?**
4. **What causes internal memory fragmentation in static LLM serving architectures, and why does variable-length generation make it unavoidable without paging?**
5. **How does Speculative Decoding accelerate inference latency without altering the mathematical output probability distribution of the target model?**

---

## 🚦 Pre-Flight Submission & Quality Checklist

Before submitting your phase architecture for certification, verify:
- [ ] All quantitative capacity math equations use explicit powers of 10 and real-world hardware latencies.
- [ ] API endpoints specify HTTP verbs, status codes, request bodies, and idempotency headers.
- [ ] Data models define primary keys, partition keys, sharding strategies, and secondary indexes.
- [ ] No single point of failure (SPOF) exists in either the control plane or the data path.
- [ ] Failure modes (split-brain, clock skew, thundering herds, cascading timeouts) have explicit mitigations.
- [ ] All starter exercises and unit tests in this phase pass with a 100% success rate (`pytest`).


---

## 🚦 Pre-Flight Gate: Verify Before You Start

**Do not start until all of this is green.** Sitting a timed exam on a broken
checkout means spending the clock on setup instead of on architecture.

```bash
# From the course root.
pytest Module_21_Vector_Database_HNSW_Index_Milvus \n      Module_22_Distributed_LLM_Serving_PagedAttention_vLLM       -q

python tools/check_links.py --quiet
ruff check .
```

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer for the duration above. When it ends, stop and score what exists. |
| **No solution exists** | There is deliberately no reference answer for this exam. The rubric *is* the specification. |
| **Modules are open-book** | Re-read any README, notebook or troubleshooting guide. That is what the job looks like. |
| **`project_solution/` is closed-book** | Do not open the module solutions during the exam. Copying them measures nothing. |
| **Numbers or it did not happen** | Every capacity claim needs arithmetic you can show. "It scales" scores zero. |
| **Name your tradeoffs** | A design with no stated downside is an unexamined design, and the rubric penalises it. |

---

## 🔬 Self-Verification Harness

Produce this evidence before scoring yourself. The rubric grades **evidence**,
not intent.

```bash
# 1. Your design's code runs at all
python -m your_design               # must not traceback

# 2. Your own tests pass
pytest your_tests.py -v             # paste the summary line

# 3. It is clean
ruff check .

# 4. Your capacity numbers are reproducible
python your_capacity_math.py        # prints QPS, bandwidth, storage, cache size
```

A design document with no runnable artefact caps at the analysis criteria only.

---

## ⏱️ If You Run Out of Time

1. **Submit the working subset.** Comment out anything that does not run - a
   broken import forfeits every point in the file.
2. **Write down what is missing**, one line per requirement. Naming your own gap
   accurately is a senior skill and earns analysis credit.
3. **Keep your numbers.** Capacity math for the parts you finished outscores
   hand-waving about the parts you did not.

---

## 🔁 If You Score Below the Threshold

1. Identify the **rubric row** you lost the most points on.
2. Re-read: **Module 21's recall/latency tradeoff and Module 22's KV-cache accounting**.
3. Work that module's `debug_lab/` - it drills the exact failure modes this
   exam punishes.
4. Re-take with the numbers changed (different DAU, different payload size) so
   you are re-deriving rather than recalling.

Re-taking a checkpoint is normal. Advancing past one you failed is not, because
every later phase assumes this one.

---

## 🎓 What This Checkpoint Measures

The modules in scope taught you a set of techniques. This exam tests
**whether you can reason about AI-era infrastructure with the same rigour as the classics**.

That is deliberately different from the module quizzes, which check whether each
piece landed. Here nobody tells you which technique to reach for. Choosing well,
under a clock, with no answer key, is the closest this course gets to the real
thing.
