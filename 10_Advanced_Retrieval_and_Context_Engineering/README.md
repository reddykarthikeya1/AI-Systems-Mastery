# 10. Advanced Retrieval & Context Engineering

> **The Definitive 10/10 Production Masterclass**: Advanced RAG, Context Optimization, and Retrieval Science. Covers hierarchical AST parsing, parent-child chunking, Anthropic Contextual Retrieval, vector database internals (HNSW multi-layer graph navigation & quantization), Hybrid Search with Reciprocal Rank Fusion (RRF), Cross-Encoder two-stage reranking, ColBERTv2 Late Interaction with MaxSim, Microsoft GraphRAG (hierarchical Leiden community clustering), agentic query transformation, and Needle-in-a-Haystack (NIAH) testing.

---

## Pedagogical Architecture: From Intuition to Principal Retrieval Architect

- **00_FOUNDATIONS_PLAYGROUND.md**: Zero-jargon visual analogies, shredded contract metaphors, and runnable Python snippets.
- **01_README.md**: Rigorous mathematical expositions, HNSW skip-graph routing proofs, and MaxSim token alignment formulations.
- **02_PROJECT_GUIDE.md**: Production design blueprints and architectural invariants.
- **03_SELF_ASSESSMENT_AND_CHALLENGES.md**: 5 Staff/Principal Retrieval interview scenarios with detailed solutions.
- **04_TROUBLESHOOTING_AND_EDGE_CASES.md**: Real-world production post-mortems (entity hub explosion, lost in the middle attention decay, orphan parent leaks).
- **project_solution/**: Fully implemented, verified Python retrieval engines.
- **starter/**: Clean student implementation stubs enforcing the strict grading-loop invariant.

---

## Master Course Roadmap

| # | Module | Core Architectural Scope | Deliverables & Code Engines | Status |
|---|---|---|---|:---:|
| **01** | [Parsing & Hierarchical Chunking](Module_01_Parsing_and_Hierarchical_Chunking/01_README.md) | AST document parsing, table preservation, and parent-child chunking | [Hierarchical Chunker](Module_01_Parsing_and_Hierarchical_Chunking/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **02** | [Contextual Retrieval Architecture](Module_02_Contextual_Retrieval_Architecture/01_README.md) | Anthropic contextual pre-headers, dual dense+sparse indexing, and 49% failure reduction | [Contextual Augmenter](Module_02_Contextual_Retrieval_Architecture/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **03** | [Vector Database Internals](Module_03_Vector_Database_Internals/01_README.md) | HNSW multi-layer skip graphs, greedy routing, product quantization, and DiskANN | [HNSW Graph Simulator](Module_03_Vector_Database_Internals/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **04** | [Hybrid Search & RRF](Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion/01_README.md) | Dense semantic + BM25 sparse search fusion, Cormack RRF formula ($k=60$) | [Hybrid Search RRF Engine](Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **05** | [Multi-Stage Retrieval & Reranking](Module_05_Multi_Stage_Retrieval_and_Reranking/01_README.md) | Two-stage candidate filtering and cross-encoder token-level self-attention | [Two-Stage Reranker](Module_05_Multi_Stage_Retrieval_and_Reranking/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **06** | [ColBERTv2 & Late Interaction](Module_06_ColBERTv2_and_Late_Interaction/01_README.md) | Token-level MaxSim late interaction, residual centroid compression, and PLAID | [ColBERT MaxSim Engine](Module_06_ColBERTv2_and_Late_Interaction/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **07** | [Microsoft GraphRAG & Knowledge Graphs](Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs/01_README.md) | Entity-relationship extraction, Leiden community detection, and global Map-Reduce | [GraphRAG Engine](Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **08** | [Query Transformation & Agentic RAG](Module_08_Query_Transformation_and_Agentic_RAG/01_README.md) | Sub-query decomposition, HyDE hypothetical documents, and corrective relevance grading | [Query Transformer](Module_08_Query_Transformation_and_Agentic_RAG/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **09** | [Context Optimization & NIAH Testing](Module_09_Context_Optimization_and_NIAH_Testing/01_README.md) | Lost-in-the-middle mitigation, U-shaped context reordering, and synthetic NIAH test suites | [Context Optimizer & NIAH](Module_09_Context_Optimization_and_NIAH_Testing/02_PROJECT_GUIDE.md) | 🟢 Complete |

---

## Testing & Verification

```powershell
# Run interactive quickstart demonstration across all modules
python 00_quickstart_interactive_demo.py

# Run full automated test suite
pytest 10_Advanced_Retrieval_and_Context_Engineering -v
ruff check 10_Advanced_Retrieval_and_Context_Engineering
```
