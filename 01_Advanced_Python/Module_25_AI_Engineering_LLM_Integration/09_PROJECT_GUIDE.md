# Module_25_AI_Engineering_LLM_Integration: Project Implementation Guide

**Deliverable:** a production Retrieval-Augmented Generation (RAG) agent featuring semantic vector search, chunking with overlap, and tool-calling.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_rag_agent.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Semantic Text Chunking
Implement sentence-boundary aware chunking with sliding-window overlap to preserve context across boundaries.

### Step 2 — Vector Embeddings Engine
Implement `TfidfSvdEmbedder` computing real, offline dense vector embeddings using TF-IDF and TruncatedSVD.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_rag_agent.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Cosine Similarity Vector Index
Implement vector search calculating cosine distance between query embeddings and document chunks.

### Step 4 — Tool-Calling Knowledge Agent
Implement `RAGAgent` combining vector retrieval with structured tool calling and response synthesis.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/rag_agent.py`, change cosine similarity calculation to use Euclidean distance without normalization.
Run:
```bash
pytest ../project_solution/test_rag_agent.py -k test_semantic_search_retrieval -v
```
Watch the test fail when relevance ranking inverts top results, then restore cosine similarity.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_rag_agent.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Hybrid Dense + BM25 Sparse Search:** Implement reciprocal rank fusion (RRF) combining keyword search with dense vectors.
2. **Context Compression Re-ranking:** Filter retrieved chunks using an LLM or cross-encoder re-ranker before prompting.
3. **Conversational Memory Window:** Track multi-turn conversation history with token budget management.
4. **HNSW Vector Index:** Integrate a high-dimensional Hierarchical Navigable Small World index for sub-millisecond retrieval.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_semantic_search_retrieval` | Proves vector search retrieves relevant chunks matching semantic query |
| `test_chunking_preserves_sentence_boundaries` | Proves text chunking does not fracture words across chunks |
| `test_chunk_overlap_prevents_boundary_loss` | Proves sliding window overlap retains facts spanning boundaries |
| `test_rag_agent_tool_calling` | Proves agent selects and executes appropriate tools based on query |
| `test_empty_query_safe_handling` | Proves empty or malformed queries return empty results without crashing |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain dense vector embeddings vs sparse keyword search (BM25)
- [ ] Implement sentence-boundary aware text chunking with configurable overlap
- [ ] Compute cosine similarity accurately using vectorized NumPy operations
- [ ] Design Retrieval-Augmented Generation (RAG) workflows that ground LLM answers in facts
- [ ] Implement tool-calling agent loops with structured input/output schemas
- [ ] Avoid simulated technology anti-patterns (e.g. using SHA-256 hashes as embeddings)
- [ ] Evaluate retrieval precision, recall, and hallucination rates systematically
