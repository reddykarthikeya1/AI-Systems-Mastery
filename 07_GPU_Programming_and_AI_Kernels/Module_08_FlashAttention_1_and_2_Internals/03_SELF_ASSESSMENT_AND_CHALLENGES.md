# Self-Assessment & Staff Interview Challenges: FlashAttention

## Architectural Interview Scenarios

### Question 1: SRAM Block Sizing Constraints
**Scenario**: How do you choose the block sizes $B_r$ and $B_c$ for FlashAttention on an NVIDIA A100 (164 KB Shared Memory per SM)?

**Staff-Level Solution**:
Each SM must store:
- $Q_i$ block: $B_r \times d \times 2 \text{ bytes}$ (FP16)
- $K_j$ block: $B_c \times d \times 2 \text{ bytes}$
- $V_j$ block: $B_c \times d \times 2 \text{ bytes}$
- Intermediate outputs / accumulators.
For hidden dimension $d = 128$:
If $B_r = 64, B_c = 64$:
Memory = $(64 \times 128 + 64 \times 128 + 64 \times 128) \times 2 = 49{,}152 \text{ bytes (48 KB)}$.
This fits comfortably within 164 KB, leaving headroom for double-buffered ping-pong staging.
If $B_r$ was set to 256, memory exceeds SRAM capacity, causing launch failure!
