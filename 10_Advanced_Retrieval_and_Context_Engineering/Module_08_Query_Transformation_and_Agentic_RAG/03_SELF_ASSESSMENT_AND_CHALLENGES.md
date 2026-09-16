# Module 08: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: HyDE Hallucination Poisoning
**Question**: When applying HyDE to a medical diagnosis query, the generator model hallucinated an unapproved pharmaceutical drug in the hypothetical passage. The retriever subsequently matched non-clinical marketing pages promoting that unapproved drug. How do you prevent HyDE hallucination poisoning in high-stakes domains?

**Solution**:
1. **Ensemble Multi-Hypothesis Embedding**: Generate $N=4$ diverse hypothetical passages using temperature $T=0.7$, average their embedding vectors $\bar{v} = \frac{1}{N} \sum v_{\hat{d}_i}$. Hallucinated specifics cancel out, while invariant core terminology reinforces.
2. **Dense-Sparse Guardrail**: Pair HyDE dense retrieval with BM25 keyword retrieval. If key factual entities in the retrieved documents do not appear in the original user query, down-weight the score.
