# Module 07: Microsoft GraphRAG & Knowledge Graphs

## 1. Algorithmic Architecture of GraphRAG

GraphRAG (Edge et al., Microsoft Research 2024) unifies Knowledge Graph extraction with hierarchical community detection to enable global dataset-wide summarization.

### 1.1 Ingestion & Graph Construction Pipeline
1. **Source Document Chunking**: Raw corpus $\mathcal{D}$ is partitioned into text chunks $c_i$.
2. **Entity & Relationship Extraction**: An extraction LLM identifies typed entities $\mathcal{E}$ and directed relationships $\mathcal{R} \subseteq \mathcal{E} \times \mathcal{E}$.
3. **Hierarchical Community Clustering (Leiden Algorithm)**:
   The graph is partitioned into a hierarchy of non-overlapping communities $C_1, C_2, \dots, C_k$ by maximizing modularity:
   $$\mathcal{H} = \sum_{c} \left[ \frac{e_c}{2m} - \gamma \left(\frac{K_c}{2m}\right)^2 \right]$$
4. **Community Report Generation**: An LLM writes structured natural language reports for each cluster at varying levels of abstraction (macro, meso, micro).

### 1.2 Global Search vs. Local Search Execution
- **Global Search (Map-Reduce)**: For high-level thematic queries, community reports at layer $L$ are scored, selected, and aggregated in parallel via Map-Reduce summarization.
- **Local Search**: For entity-focused queries, the graph traverses immediate 1-hop and 2-hop neighborhoods, combining graph context with raw text chunks.
