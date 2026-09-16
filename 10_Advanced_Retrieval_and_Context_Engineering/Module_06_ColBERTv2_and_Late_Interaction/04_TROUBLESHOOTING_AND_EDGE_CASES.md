# Module 06: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in ColBERT Serving

### Bug 1: Vector Dimension Mismatch in MaxSim Matrix Multiplication
- **Symptom**: `RuntimeError: The size of tensor a (128) must match the size of tensor b (768)`.
- **Root Cause**: Standard BERT output is dimension 768, but ColBERT projects token embeddings down to linear bottleneck dimension $d=128$. Forgetting the projection layer causes $6\times$ memory explosion and dimension mismatches.
- **Fix**: Always apply the trained linear projection layer: $E_{\text{projected}} = \text{LayerNorm}(W_{\text{proj}} \cdot H_{\text{bert}})$.
