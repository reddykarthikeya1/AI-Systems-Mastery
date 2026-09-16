# Module 05: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Candidate Pool Sizing ($K_{\text{candidates}}$) Trade-off
**Question**: An engineer observes that increasing $K_{\text{candidates}}$ from 50 to 250 increases retrieval recall by 1.2% but increases P99 reranking latency from $22 \text{ ms}$ to $110 \text{ ms}$, violating the serving SLA. Formulate an optimization strategy.

**Solution**:
1. **Root Cause**: Cross-encoder latency scales linearly with candidate count $K$: $T \approx K \times \frac{\text{FLOPs}_{\text{pair}}}{\text{Throughput}}$.
2. **Remedy**:
   - Cap $K_{\text{candidates}} = 50$.
   - Improve Stage 1 recall without increasing $K$ by adopting **Hybrid Search (BM25 + Dense RRF)** in Stage 1. Hybrid search increases recall from 78% to 92% within the top 50 candidates, eliminating the need to expand $K$ to 250.
   - Use dynamic early exit or distilled lightweight rerankers (e.g. BGE-Reranker-Small or FlashRank ONNX runtime).

---

### Scenario 2: Document Truncation in Cross-Encoders
**Question**: When candidate passages exceed the cross-encoder context window (512 tokens), how should long passages be scored without silent tail truncation?

**Solution**:
Slice candidate passages into sliding sub-passages of 256 tokens with 64-token overlap.
Score each sub-passage against query $q$: $s_i = \text{CrossEncoder}(q, p_i)$.
Aggregate passage score via **Max-Pooling**:
$$S(q, D) = \max_{i} s_i$$
This ensures facts situated at the end of long documents are scored with full cross-attention fidelity.
