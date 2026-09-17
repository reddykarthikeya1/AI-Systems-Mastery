# Design Rationale: Grounded RAG Agent & Deterministic Tool Calling Engine

## Architectural Overview
An enterprise AI reasoning subsystem featuring high-dimensional vector embeddings, cosine similarity top-$K$ indexing, retrieval-augmented generation (RAG), and Pydantic tool calling guardrails.

## Key Design Decisions
1. **Grounded RAG Retrieval Pipeline:** Queries retrieve relevant proprietary context passages before prompting the model, eliminating factual hallucinations.
2. **Pydantic-Enforced Tool Calling Guardrails:** Model tool invocation decisions emit structured JSON validated directly against Pydantic schemas before executing external Python actions.
3. **Vectorized Cosine Similarity Search:** Dense embeddings are compared using normalized vector dot products, achieving sub-millisecond semantic search over knowledge bases.

## Rejected Alternatives
1. **Executing Raw Model-Generated Code (`eval()`):**
   - *Reason for Rejection:* Executing unvalidated LLM output with `eval()` or unconstrained shell calls introduces fatal Remote Code Execution vulnerabilities.
2. **Fine-Tuning Models for Dynamic Knowledge Storage:**
   - *Reason for Rejection:* Fine-tuning is expensive, slow, and alters model behavior without guaranteeing factual accuracy. RAG provides instant, verifiable knowledge updates.

## Invariants & Guarantees
- Tool calls with malformed arguments are rejected before execution.
- Retrieved context is isolated with strict XML boundary delimiters.

## Verification
```bash
pytest test_rag_agent.py -v
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |

