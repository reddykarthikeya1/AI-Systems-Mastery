# Module 04: Hybrid Search & Reciprocal Rank Fusion (RRF)

## 1. Theoretical Foundations of Multi-Channel Information Retrieval

Dense semantic retrieval (bi-encoder embeddings) and sparse lexical retrieval (BM25 / SPLADE) exhibit complementary failure modes:
- **Dense Retrieval**: Excels at semantic paraphrasing, cross-lingual retrieval, and conceptual intent. Fails on exact serial numbers, acronyms, code identifiers, and out-of-vocabulary entities.
- **Sparse Lexical Retrieval (BM25)**: Excels at exact term matching and rare keywords. Fails on vocabulary mismatch and synonyms.

### 1.1 Reciprocal Rank Fusion (Cormack et al., SIGIR 2009)
Given a set of candidate document rankings $\mathcal{R}$, RRF calculates a fused relevance score:
$$\text{RRF\_Score}(d) = \sum_{r \in \mathcal{R}} \frac{1}{k + \text{rank}_r(d)}$$
where:
- $\text{rank}_r(d) \in \{1, 2, \dots\}$ is the 1-based ordinal ranking of document $d$ in retriever $r$.
- $k \in \mathbb{N}$ (typically $k=60$) is the ranking regularization hyper-parameter.

### 1.2 Mathematical Properties of RRF
1. **Scale Invariance**: RRF operates strictly on permutations (ordinal ranks) rather than cardinal score magnitudes, eliminating the need for calibration across diverse query categories.
2. **Monotonicity**: If document $d$ improves its rank in any constituent list without decreasing in others, its RRF score increases strictly monotonically.
3. **Outlier Damping**: The hyper-parameter $k=60$ mitigates the undue influence of high ranks in a single uncalibrated retriever.
