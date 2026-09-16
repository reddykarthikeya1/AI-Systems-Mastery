# Troubleshooting & Edge Cases: Fused Activations & Normalization

## Production Traps & Silent Failure Modes

### 1. NaN Propagation from Negative Epsilon or Underflow
- **Symptom**: Loss becomes NaN within 50 iterations of LLM pre-training.
- **Root Cause**: When inputs $x$ are zero or near-zero, $\text{RMS}(x) = \sqrt{0 + \epsilon}$. If $\epsilon$ is too small (e.g. $10^{-12}$) or floats round down, division by zero occurs.
- **Fix**: Standardize $\epsilon = 10^{-5}$ or $10^{-6}$ and clamp variance $\max(\text{var}, 0.0)$.
