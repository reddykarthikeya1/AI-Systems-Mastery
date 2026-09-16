# Self-Assessment & Staff Interview Challenges: Fused Activations & Normalization

## Architectural Interview Scenarios

### Question 1: Numerical Stability in FP16 RMSNorm
**Scenario**: In FP16, numbers above 65,504 overflow to infinity. When computing $\sum x_i^2$ for hidden dimension $d = 8{,}192$, values frequently overflow. How do you prevent this in a fused kernel?

**Staff-Level Solution**:
Compute the intermediate reduction in **FP32 accumulation registers**:
- Read inputs as FP16 (`half` / `bfloat16`).
- Cast to `float` (FP32) before squaring: `float val = (float)x[i]; sum_sq += val * val;`.
- Compute reciprocal square root in FP32: `float r_rms = rsqrtf(sum_sq / d + eps);`.
- Multiply back and cast to FP16 upon storing to memory: `y[i] = (half)(val * r_rms * (float)weight[i]);`.
This prevents all overflow without sacrificing HBM memory bandwidth.
