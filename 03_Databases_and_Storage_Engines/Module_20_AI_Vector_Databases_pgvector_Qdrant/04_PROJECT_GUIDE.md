# Module 20 AI Vector Databases pgvector Qdrant: Project Guide

## 📌 Project Overview: Semantic Document Retrieval Engine with HNSW & Metadata Filtering

This comprehensive guide walks you step-by-step through building the project for **AI Vector Databases: pgvector & Qdrant HNSW Similarity**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **Vector embeddings, distance metrics (Cosine, L2, Dot), HNSW graph indexing, and payload filtering**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Generate mock vector embeddings and compute cosine similarity. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Build a semantic search service using Qdrant (in-memory / live) and pgvector, supporting HNSW approximate nearest neighbor search with strict metadata payload filters. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Implement an ANN recall benchmark evaluating Top-K retrieval precision against exact brute-force flat search across varying graph ef_search parameters. |

---

## 1. Architectural Blueprint & Data Flow

```text
       ┌────────────────────────────────────────────────────────┐
       │                   Application Layer                    │
       └───────────────────────────┬────────────────────────────┘
                                   │
              ┌────────────────────┴───────────────────┐
              │                                        │
     ┌────────▼──────────┐                   ┌─────────▼─────────┐
     │  Track A (Model)  │                   │  Track B (Live)   │
     │ Pure-Python Engine│                   │ Real Driver / DB  │
     │ Internal Mechanics│                   │ Production Engine │
     └────────┬──────────┘                   └─────────┬─────────┘
              │                                        │
              └────────────────────┬───────────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │   Reconciliation Test     │
                     │  Validates Shared Semantics│
                     └───────────────────────────┘
```

---

## 2. Directory Structure & Key Files

```text
Module_20_AI_Vector_Databases_pgvector_Qdrant/
├── README.md                                 # Core theory, diagrams, and operational syllabus
├── PROJECT_GUIDE.md                          # This 3-tier guided project specification
├── TROUBLESHOOTING_AND_EDGE_CASES.md         # Production error signatures and debugging runbooks
├── SELF_ASSESSMENT_AND_CHALLENGES.md         # 10 diagnostic questions + coding challenges
├── starter/                                  # Skeleton code with exercises and hints
└── project_solution/                         # Reference implementations & full test suites
    ├── conftest.py                           # Pytest fixtures and isolated configuration
    ├── *_engine.py                           # Track A: In-memory reference engine
    ├── test_*_engine.py                      # Track A verification tests
    ├── *_live.py                             # Track B: Real driver & client operations
    └── test_*_live.py                        # Track B integration & reconciliation tests
```

---

## 3. Step-by-Step Implementation Roadmap

### Phase 1: Environment & Setup
1. Verify required Python packages are installed: `pip install -e .`
2. If working with live database engines, ensure local services are running via Docker:
   ```bash
   docker compose up -d
   ```
3. Run existing baseline tests to verify environment health:
   ```bash
   pytest Module_20_AI_Vector_Databases_pgvector_Qdrant -v
   ```

### Phase 2: Building Core Capabilities (Tier 1 & 2)
1. Complete the starter exercises in `starter/`.
2. Ensure all unit tests pass with zero assertion failures.
3. Validate operational behaviors against Track B live implementations.

### Phase 3: Architect Stretch (Tier 3)
1. Implement the advanced stretch challenge specified in Tier 3.
2. Add dedicated test cases verifying boundary conditions, concurrency limits, and failure recovery.
3. Profile execution performance and record latency/throughput improvements.

---

## 4. Verification & Self-Check Checklist

- [ ] All Track A unit tests pass: `pytest Module_20_AI_Vector_Databases_pgvector_Qdrant/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_20_AI_Vector_Databases_pgvector_Qdrant/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Explain what an embedding is and why cosine distance is the usual metric
- [ ] Compare HNSW and IVFFlat on build time, memory, and recall
- [ ] Explain what recall means for an approximate index and how to measure it
- [ ] Decide between `pgvector` and a dedicated vector database, with reasons
- [ ] Combine a metadata filter with a vector search and explain the cost
- [ ] Explain why a cryptographic hash cannot serve as an embedding

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
