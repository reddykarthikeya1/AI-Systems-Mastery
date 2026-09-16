# 🐣 W3Schools-Style Playground: Transformers, Self-Attention & RoPE

> *"Attention is a smart filing cabinet: You present a Query (what you are searching for), compare it to Keys (folder labels), and pull out the weighted sum of Values (the contents)."*

---

## 1. The Attention Formula: Step-by-Step

$$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

1. **$Q K^T$ (Similarity Score)**: Measures how relevant each token is to every other token.
2. **$\frac{1}{\sqrt{d_k}}$ (Scaling Factor)**: If $d_k = 64$, variance of the dot product is 64! Large numbers push Softmax into saturated flat zones where gradients vanish. Dividing by $\sqrt{64} = 8$ keeps gradients healthy!
3. **Causal Mask (For Generative Models)**: In GPT, token 3 cannot look at token 4. We mask future positions with $-\infty$ so their Softmax probability becomes $0.0$.
4. **Weighted Values**: Multiply Softmax weights by $V$ to synthesize the contextual representation.

---

## 2. Rotary Position Embeddings (RoPE)

How do modern LLMs (LLaMA-3, Mistral, Gemma) know word order?
- Older models **added** position vectors: $x + p_i$.
- **RoPE (Su et al., 2021)** rotates query and key vectors in 2D pairs by angle $m \theta_i$:
$$R_{\Theta, m}^d x$$
- When calculating $Q_m \cdot K_n$, the dot product simplifies to an expression that depends **only on relative distance $(m - n)$**!
- This gives models the superpower to extrapolate to longer context lengths!
