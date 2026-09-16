# 🐣 W3Schools-Style Playground: FlashAttention-1 & 2 Internals

> *"Standard attention is an IO disaster: it writes an enormous $N \times N$ matrix to GPU memory only to read it right back. FlashAttention tiles $Q, K, V$ into fast SRAM and uses running online softmax to compute the exact same result with $O(N)$ memory and up to $4\times$ speedup."*

---

## 1. The $O(N^2)$ VRAM Crisis

Standard Multi-Head Attention computes:
$$S = \frac{Q K^T}{\sqrt{d_k}} \in \mathbb{R}^{N \times N}$$
$$P = \text{softmax}(S) \in \mathbb{R}^{N \times N}$$
$$O = P V \in \mathbb{R}^{N \times d_k}$$

If sequence length $N = 64{,}000$:
- The matrix $S$ has $64{,}000^2 \approx 4.1 \text{ billion elements}$.
- In FP16 ($2 \text{ bytes}$), storing $S$ takes **8.2 GB per attention head**!
- With 32 heads, that's **262 Gigabytes of VRAM for one single layer**! Immediate CUDA Out-Of-Memory!

---

## 2. Tri Dao's Secret: IO-Aware SRAM Tiling

Your GPU has ~100-228 KB of ultra-fast **SRAM (Shared Memory)** per SM.
FlashAttention breaks matrices into small blocks that fit perfectly in SRAM:
1. Divide $Q$ into blocks of size $B_r \times d$ (e.g. $64 \times 128$).
2. Divide $K$ and $V$ into blocks of size $B_c \times d$ (e.g. $64 \times 128$).
3. Load block $Q_i$ into SRAM.
4. Loop through $K_j, V_j$:
   - Compute block attention scores: $S_{ij} = Q_i K_j^T / \sqrt{d}$.
   - Update running maximum $m_i$ and running normalizer $l_i$.
   - Accumulate output block $O_i$ in fast registers!
5. Write $O_i$ back to HBM **once**!

**The Result**: The massive $N \times N$ matrix is **never materialized in HBM**!
Memory complexity drops from $O(N^2)$ to $O(N)$!

---

## 3. FlashAttention-2: Faster, Simpler, More Parallel

What did FlashAttention-2 improve over FlashAttention-1?
1. **Parallelize Over Sequence Length**: Instead of launching blocks over Batch and Heads, FA-2 splits the outer loop over sequence length blocks $B_r$, utilizing all 132 SMs even with small batch sizes!
2. **Postpone Rescaling**: In FA-1, $O_i$ was rescaled on every inner iteration. FA-2 maintains unnormalized accumulators and performs a single division by $l_i$ at the end of the block loop, saving thousands of FLOPs!
