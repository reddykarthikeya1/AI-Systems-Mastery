# Module 08: Model Quantization for Serving (FP8, INT4, AWQ & Marlin)

## 1. Mathematical Principles of Uniform Quantization

Uniform quantization maps a continuous real-valued tensor $X \in \mathbb{R}$ to a discrete grid of $b$-bit integers $\mathbb{Z}$:

### 1.1 Symmetric Quantization
$$q = \text{clamp}\left(\left\lfloor \frac{x}{s} \right\rceil, -2^{b-1}, 2^{b-1} - 1\right)$$
$$\hat{x} = q \times s$$
where scale factor $s$ is:
$$s = \frac{\max(|X|)}{2^{b-1} - 1}$$

### 1.2 SmoothQuant Mathematical Invariance
SmoothQuant (Xiao et al., ICML 2023) observes that activation quantization is hard because of persistent activation outliers, whereas weight quantization is easy.
Because linear operations satisfy associativity:
$$Y = X W = (X \cdot \text{diag}(s)^{-1}) \cdot (\text{diag}(s) \cdot W) = \hat{X} \hat{W}$$
By choosing per-channel smoothing scale $s_j$:
$$s_j = \frac{\max(|X_j|)^\alpha}{\max(|W_j|)^{1-\alpha}}, \quad \alpha \in [0.5, 0.85]$$
The dynamic range of activations is smoothed down, enabling seamless 8-bit matrix multiplication without outlier degradation.
