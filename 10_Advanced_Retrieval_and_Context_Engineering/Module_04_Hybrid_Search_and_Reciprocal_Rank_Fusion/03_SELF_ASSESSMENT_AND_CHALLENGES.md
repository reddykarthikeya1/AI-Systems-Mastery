# Module 04: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Convex Score Combination vs. RRF Calibration
**Question**: An engineer proposes replacing RRF with a linear weighted score sum:
$$S(d) = \alpha \cdot S_{\text{dense}}(d) + (1 - \alpha) \cdot S_{\text{sparse}}(d)$$
Explain why this linear combination degrades in production unless an online Platt scaling or min-max normalization pipeline is maintained, and why RRF is robust against this defect.

**Solution**:
1. **Score Non-Stationarity**:
   - Cosine similarity scores for dense models are bounded in $[-1, 1]$, with practical semantic matches clustering in $[0.65, 0.95]$.
   - BM25 scores are unbounded $[0, \infty)$; a short query with rare terms might yield max BM25 of 28.5, while a long query with common words yields max BM25 of 4.2.
   - Fixed parameter $\alpha = 0.5$ will cause BM25 to dominate by $10\times$ on rare-term queries, and dense search to dominate on generic queries.
2. **RRF Robustness**: RRF relies exclusively on relative order $\text{rank}(d) \in \{1, 2, \dots\}$. Whether the raw score was 4.2 or 285.0, the top hit has rank 1. It operates with zero score calibration maintenance.

---

### Scenario 2: Latency Imbalance in Asynchronous Hybrid Execution
**Question**: BM25 inverted index lookup takes $1.5 \text{ ms}$, while dense embedding generation plus ANN search takes $35 \text{ ms}$. How should the serving tier orchestrate hybrid execution to minimize P99 latency?

**Solution**:
1. Launch BM25 search and dense embedding inference concurrently using asynchronous coroutines (`asyncio.gather` / concurrent thread pool).
2. Begin lexical scoring immediately on CPU while the GPU evaluates embedding Tensor Cores.
3. Apply RRF as soon as both coroutines resolve, bounding overall latency to $\max(T_{\text{sparse}}, T_{\text{dense}}) + T_{\text{rrf}} \approx 35 + 0.2 \approx 35.2 \text{ ms}$.
