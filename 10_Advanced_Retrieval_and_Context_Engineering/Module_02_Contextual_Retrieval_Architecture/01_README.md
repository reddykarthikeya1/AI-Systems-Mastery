# Module 02: Contextual Retrieval Architecture


## Contextual Retrieval: Prepending Global Context

```mermaid
flowchart TD
    subgraph Problem["Isolated Chunk Context Loss"]
        RawChunk["Chunk: 'The company grew revenue by 12% in Q3.'<br/>(Which company? Which year?)"]
    end

    subgraph Solution["Contextual Retrieval (Anthropic Pattern)"]
        LLM["Prompt Claude: Generate 50-word context summary using entire document"]
        Context["Context: 'In Apple Inc 2023 10-K filing financial results section...'"]
        Enriched["Enriched Chunk = Context + Raw Chunk"]
    end

    RawChunk --> LLM --> Context --> Enriched
```

## 1. Algorithmic Principles of Contextual Retrieval

Contextual Retrieval (Anthropic, 2024) solves the semantic isolation defect inherent in localized text chunking.

### 1.1 Mathematical Formulation
Let document $\mathcal{D}$ consist of chunks $(c_1, c_2, \dots, c_m)$.
In naive retrieval, embedding is applied to isolated text:
$$v_i = \text{Embed}(c_i)$$

In Contextual Retrieval, an auxiliary model $\mathcal{M}_{\text{context}}$ generates contextual prefix $p_i$:
$$p_i = \mathcal{M}_{\text{context}}(\mathcal{D}, c_i)$$
The augmented chunk $\tilde{c}_i$ is formed:
$$\tilde{c}_i = p_i \circ c_i$$
$$\tilde{v}_i = \text{Embed}(\tilde{c}_i)$$

### 1.2 Dual Indexing: Dense + BM25 Synergy
Contextual augmentation provides compounding benefits across both retrieval channels:
1. **Dense Vector Search**: Moves chunk vectors closer to broad semantic entity clusters (e.g. company names, domain taxonomy).
2. **Sparse Lexical Search (BM25)**: Adds critical exact keyword terms that are otherwise absent from localized pronouns ("the company", "it", "they").
Combining Contextual Dense + Contextual BM25 reduces retrieval failure rate by **up to $49\%$** compared to naive RAG.