# Module 08: Query Transformation & Agentic RAG


## ColBERT Late Interaction Token Similarity Matrix

```mermaid
flowchart TD
    Q_Tokens["Query Tokens: [q0, q1, ..., qn]"] --> Mat["Late Interaction Similarity Matrix (Cosine Sim)"]
    D_Tokens["Document Tokens: [d0, d1, ..., dm]"] --> Mat
    Mat --> MaxSim["MaxSim Operator: For each query token, take max similarity across all doc tokens"]
    MaxSim --> Sum["Sum MaxSim scores -> Final Document Relevance Score"]
```

## 1. Architectural Foundations of Query Translation

Raw user inputs often suffer from semantic underspecification, multi-hop dependencies, and vocabulary mismatch.

### 1.1 Decomposition Algorithms
Given complex query $Q$:
$$\mathcal{Q} = \text{Decompose}(Q) = \{q_1, q_2, \dots, q_k\}$$
Sub-queries are dispatched concurrently to retrieval channels, and candidate sets are unified via union or reciprocal rank fusion.

### 1.2 Hypothetical Document Embeddings (HyDE; Gao et al., 2022)
Instead of embedding user query $q \in \mathbb{R}^{d}$:
1. Generate hypothetical document: $\hat{d} = \mathcal{M}_{\text{gen}}(q)$.
2. Embed the hypothetical document: $v_{\hat{d}} = \text{Embed}(\hat{d})$.
3. Retrieve documents nearest to $v_{\hat{d}}$:
   $$\mathcal{D}^* = \arg\max_{d \in \mathcal{D}} \langle v_{\hat{d}}, \text{Embed}(d) \rangle$$
HyDE shifts the search representation from question space to answer space, eliminating the asymmetric distance distortion in bi-encoder embeddings.