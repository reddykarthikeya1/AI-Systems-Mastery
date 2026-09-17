# Module 05: Multi-Stage Retrieval & Cross-Encoder Reranking


## Hybrid Search Reciprocal Rank Fusion (RRF)

```mermaid
flowchart TD
    Query["User Query"] --> Sparse["BM25 Lexical Keyword Search"]
    Query --> Dense["Dense Semantic Vector Embeddings"]

    Sparse --> TopSparse["Sparse Top-K Ranks"]
    Dense --> TopDense["Dense Top-K Ranks"]

    TopSparse --> RRF["Reciprocal Rank Fusion Formula:<br/>RRF_score(d) = Σ 1 / (k + rank_i(d)) (k=60)"]
    TopDense --> RRF

    RRF --> Merged["Fused Ranked Results (Best of Exact Match & Conceptual Match)"]
```

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[00_try_it_yourself.py](00_try_it_yourself.py)** | Run in terminal (`python 00_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **5** | **[03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **6** | **[02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **7** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **8** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---

## 1. Architecture of Two-Stage Search Pipelines

To balance sub-50ms latency SLAs with high Normalized Discounted Cumulative Gain (NDCG@10), production RAG architectures employ a staged retrieval cascade.

### 1.1 Bi-Encoder vs. Cross-Encoder Mechanics
- **Bi-Encoder**:
  $$s(q, d) = \langle f(q), g(d) \rangle$$
  $f(q)$ and $g(d)$ are computed independently. All document embeddings $g(d)$ are pre-computed offline. Query latency is bounded by fast vector index lookups ($O(\log N)$). However, no cross-attention occurs between query tokens and document tokens.
- **Cross-Encoder**:
  $$s(q, d) = \mathcal{M}_{\text{cross}}([q \circ d])$$
  Full self-attention is evaluated across all cross-token pairs $(t_{q,i}, t_{d,j})$:
  $$\text{Complexity} = O((|q| + |d|)^2)$$
  Computational cost prohibits evaluating all $N$ corpus documents.

### 1.2 Two-Stage Funnel Optimization
$$\mathcal{C} = \text{Retrieve}_{\text{Bi-Encoder}}(q, N_{\text{corpus}}, K_{\text{candidates}}=100)$$
$$\mathcal{R} = \text{Top}_K(\text{Rerank}_{\text{Cross-Encoder}}(q, \mathcal{C}, K_{\text{final}}=5))$$