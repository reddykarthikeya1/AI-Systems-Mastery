# Module 05: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Reranking

### Bug 1: Cross-Encoder Score Inversion from Missing Normalization
- **Symptom**: Reranker outputs negative logits (e.g. $-4.2, -1.8$), causing threshold filters to discard valid documents.
- **Root Cause**: Raw cross-encoder heads output uncalibrated classification logits.
- **Fix**: Apply sigmoid transform $\sigma(s) = \frac{1}{1 + e^{-s}}$ to normalize relevance scores into $[0.0, 1.0]$.
