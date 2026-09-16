# Master Syllabus: 10. Advanced Retrieval & Context Engineering

> 9 Core Modules · Production Reference Implementations · Staff-Level Systems Architecture · 10/10 Masterclass

## Course Curriculum Matrix

| # | Module | Core Architectural Topics | Hands-on Project Deliverable |
|---|---|---|---|
| **01** | [Parsing & Hierarchical Chunking](Module_01_Parsing_and_Hierarchical_Chunking/01_README.md) | AST parsing, table preservation, parent-child chunk hierarchy | [Hierarchical Chunker](Module_01_Parsing_and_Hierarchical_Chunking/02_PROJECT_GUIDE.md) |
| **02** | [Contextual Retrieval Architecture](Module_02_Contextual_Retrieval_Architecture/01_README.md) | Anthropic contextual pre-headers, dual dense+sparse index enrichment | [Contextual Augmenter](Module_02_Contextual_Retrieval_Architecture/02_PROJECT_GUIDE.md) |
| **03** | [Vector Database Internals](Module_03_Vector_Database_Internals/01_README.md) | HNSW multi-layer graphs, greedy routing, product quantization | [HNSW Graph Simulator](Module_03_Vector_Database_Internals/02_PROJECT_GUIDE.md) |
| **04** | [Hybrid Search & RRF](Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion/01_README.md) | Dense vector + BM25 sparse search fusion, Cormack RRF formula | [Hybrid Search RRF Engine](Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion/02_PROJECT_GUIDE.md) |
| **05** | [Multi-Stage Retrieval & Reranking](Module_05_Multi_Stage_Retrieval_and_Reranking/01_README.md) | Bi-encoder candidate filtering + Cross-encoder token cross-attention | [Two-Stage Reranker](Module_05_Multi_Stage_Retrieval_and_Reranking/02_PROJECT_GUIDE.md) |
| **06** | [ColBERTv2 & Late Interaction](Module_06_ColBERTv2_and_Late_Interaction/01_README.md) | Token-level MaxSim late interaction, residual centroid compression | [ColBERT MaxSim Engine](Module_06_ColBERTv2_and_Late_Interaction/02_PROJECT_GUIDE.md) |
| **07** | [Microsoft GraphRAG & Knowledge Graphs](Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs/01_README.md) | Entity-relationship extraction, Leiden community detection, global Map-Reduce | [GraphRAG Engine](Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs/02_PROJECT_GUIDE.md) |
| **08** | [Query Transformation & Agentic RAG](Module_08_Query_Transformation_and_Agentic_RAG/01_README.md) | Sub-query decomposition, HyDE hypothetical documents, corrective grading | [Query Transformer](Module_08_Query_Transformation_and_Agentic_RAG/02_PROJECT_GUIDE.md) |
| **09** | [Context Optimization & NIAH Testing](Module_09_Context_Optimization_and_NIAH_Testing/01_README.md) | Lost-in-the-middle mitigation, U-shaped context reordering, synthetic NIAH | [Context Optimizer & NIAH](Module_09_Context_Optimization_and_NIAH_Testing/02_PROJECT_GUIDE.md) |
