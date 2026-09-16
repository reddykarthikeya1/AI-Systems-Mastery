# Module 07: Fused Activations & Normalization

> **Architectural Scope**: Overcoming the Memory Wall, Kernel Fusion Mechanics, Fused RMSNorm, Fused SwiGLU, and Single-Pass Online Safe Softmax.

---

## 1. The Memory Wall in Modern Transformer Architectures

In a 70B parameter LLM inference pass, matrix multiplications (GEMMs) are typically compute-bound.
However, **Activations (SwiGLU, GeLU)** and **Normalizations (RMSNorm, LayerNorm)** are deeply **Memory-Bound**:
- Every layer performs LayerNorm before and after Multi-Head Attention and MLP.
- In standard PyTorch, LayerNorm executes 4 sequential CUDA kernels:
  $$X \xrightarrow{\text{Kernel 1}} \mu \xrightarrow{\text{Kernel 2}} \sigma^2 \xrightarrow{\text{Kernel 3}} \hat{X} \xrightarrow{\text{Kernel 4}} Y$$
- Memory traffic = $4 \times$ tensor size in DRAM read/writes!

---

## 2. Kernel Fusion Architecture

Kernel fusion collapses multiple sequential operations into a **single GPU kernel launch**:
- Load row from DRAM into registers/SRAM **once**.
- Compute mean, variance, scale, shift, and activation in registers.
- Write output to DRAM **once**.
- Eliminates 75% of memory bus traffic!

---

## 3. Fused RMSNorm Formulation

Modern LLMs (LLaMA 3, Mistral, Gemma) replace standard LayerNorm with **RMSNorm** (Root Mean Square Normalization):
$$y_i = \frac{x_i}{\text{RMS}(x)} \times \gamma_i, \quad \text{where } \text{RMS}(x) = \sqrt{\frac{1}{d} \sum_{j=1}^d x_j^2 + \epsilon}$$
RMSNorm eliminates mean calculation $\mu$, saving 30% compute cycles and register pressure.

---

## 4. Online Safe Softmax Mathematical Proof

Standard Softmax:
$$S_i = \frac{e^{x_i - m}}{\sum_j e^{x_j - m}}, \quad m = \max_j(x_j)$$
Normally requires 2 passes over data: (Pass 1) find max $m$, (Pass 2) sum exponentials.

**Online Softmax (Milakov & Gimelshein 2018 / FlashAttention)**:
When combining existing running statistics $(m_A, l_A)$ from block $A$ with new block $B$:
$$m_{\text{new}} = \max(m_A,\; \max(x_B))$$
$$l_{\text{new}} = l_A \times e^{m_A - m_{\text{new}}} + \sum_{k \in B} e^{x_k - m_{\text{new}}}$$
For output accumulator $O = P V$:
$$O_{\text{new}} = O_A \times e^{m_A - m_{\text{new}}} + P_B V_B$$
This recurrence allows computing attention over infinite sequence lengths in a single pass without storing the attention matrix!

---

## 5. Module Study Progression
1. **Beginner Playground**: Read [00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).
