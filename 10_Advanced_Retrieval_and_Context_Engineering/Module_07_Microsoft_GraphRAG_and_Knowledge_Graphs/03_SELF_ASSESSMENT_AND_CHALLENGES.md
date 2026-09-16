# Module 07: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Controlling Entity Extraction LLM Costs
**Question**: Extracting knowledge graphs across a 20-million-word legal repository requires over 40,000 LLM extraction calls. Sizing this with GPT-4o costs $12,000. How do you re-architect the GraphRAG extraction pipeline to reduce indexing costs by $> 90\%$ while preserving relational accuracy?

**Solution**:
1. **Model Distillation / Fine-Tuned SLM**: Fine-tune an open-weights small model (e.g. Llama-3-8B or Qwen-2.5-7B) using synthetic extraction datasets. SLMs execute structured extraction tasks with $> 95\%$ of frontier model accuracy at $10\times$ lower inference cost.
2. **Prompt Optimization**: Use JSON Schema constrained decoding (e.g. Guidance / Outlines) to eliminate retry loops caused by malformed JSON.
3. **Chunk Filtering**: Run a fast NER model (spaCy / GLiNER) first. If a chunk contains zero named entities, bypass the LLM extraction step entirely.

---

### Scenario 2: Hub Node Degeneracy & Context Explosion
**Question**: In an enterprise knowledge graph, generic entities (e.g. "Software", "Company", "Meeting") form super-nodes connected to $> 15,000$ neighbors. When querying, expanding their neighborhood causes immediate context overflow. How do you prevent hub degeneracy?

**Solution**:
Apply **Degree-based Pruning and TF-IDF Relationship Damping**:
Filter out entities whose graph degree exceeds the 99th percentile ($k > k_{\text{threshold}}$).
Weigh edge relevance by inverse relationship frequency so that specific edges (e.g. `is_parent_company_of`) are prioritized over generic associations (`mentioned_in`).
