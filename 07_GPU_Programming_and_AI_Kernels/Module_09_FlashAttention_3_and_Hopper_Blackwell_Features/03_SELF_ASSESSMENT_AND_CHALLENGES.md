# Self-Assessment & Staff Interview Challenges: Hopper & FlashAttention-3

## Architectural Interview Scenarios

### Question 1: FP8 Dynamic Range vs Precision (E4M3 vs E5M2)
**Scenario**: In FlashAttention-3 with FP8 Tensor Cores, which FP8 format is selected for $Q, K, V$ matrix multiplication and why?

**Staff-Level Solution**:
NVIDIA Hopper supports two 8-bit floating point formats:
1. **E4M3** (1 sign, 4 exponent, 3 mantissa bits, bias=7):
   - Maximum representable value $\approx 448$. Higher precision (3 mantissa bits).
   - Ideal for activations and weights where dynamic range is bounded.
2. **E5M2** (1 sign, 5 exponent, 2 mantissa bits, bias=15):
   - Maximum value $\approx 57{,}344$. Same dynamic range as FP16, but only 2 bits of precision.
   - Ideal for gradients.
**Selection**: FlashAttention-3 uses **E4M3** for $Q, K, V$ to maximize numerical precision during attention scoring, coupled with per-tile block-scaling factors to prevent overflowing the 448 dynamic range limit.
