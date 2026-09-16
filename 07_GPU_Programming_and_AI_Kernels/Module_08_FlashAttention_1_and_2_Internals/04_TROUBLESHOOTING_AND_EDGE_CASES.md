# Troubleshooting & Edge Cases: FlashAttention

## Production Traps & Silent Failure Modes

### 1. Causal Masking Inefficiency
- **Symptom**: Causal attention runs at the same speed as bidirectional attention, wasting 50% FLOPs.
- **Root Cause**: Iterating over all $j$ blocks even when $c_{\text{start}} > r_{\text{end}}$ where attention is completely masked out.
- **Fix**: Skip entire blocks where $j \times B_c > (i + 1) \times B_r$. For strictly lower-triangular blocks, bypass the softmax causal mask entirely!
