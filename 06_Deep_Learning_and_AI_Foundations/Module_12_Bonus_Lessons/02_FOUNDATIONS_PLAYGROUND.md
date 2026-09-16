# 🐣 Interactive Foundations Playground: Modern Frontiers (MoE, Diffusion, Mamba)

> *"Dense models are a company where every employee must vote on every email. Mixture of Experts (MoE) is routing each email to the two engineers who actually know how to answer it."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. Sparse Mixture of Experts (MoE)

In a traditional Dense LLM (like LLaMA-2), every token activates 100% of the model's weights.
In a Sparse MoE (like Mixtral 8x7B or GPT-4):
- The Feedforward Network (FFN) is replaced by $E$ independent Expert networks (e.g. 8 experts).
- A lightweight **Router (Gating Network)** computes:
$$G(x) = \text{Softmax}(\text{Top2}(x \cdot W_g))$$
- For each token, only the **top-2 experts** execute! The other 6 experts consume **0 FLOPs**.
- **The Load Balancing Danger**: If expert #1 gets lucky early in training, the router might send all tokens to expert #1 forever (Winner-Takes-All collapse). We add an **Auxiliary Load Balancing Loss** to enforce equal distribution of tokens across all experts!

---

## 2. Diffusion Models: Carving Statues from Static

How does Midjourney or Stable Diffusion create photorealistic art?
1. **Forward Process (T=1,000 steps)**: Add tiny Gaussian noise to an image step-by-step until it becomes pure TV static.
2. **Reverse Process (Neural Network)**: Train a U-Net to predict: *"Given noisy image $x_t$ and timestep $t$, what was the noise $\epsilon$ added on this step?"*
3. By subtracting the predicted noise iteratively, the model turns pure white noise into high-resolution masterpieces!

---

## 3. State Space Models (Mamba)

Transformers suffer from $O(N^2)$ quadratic complexity in context length.
**Mamba (Gu & Dao, 2023)** adapts classical control theory State Space Models ($h'(t) = A h(t) + B x(t)$) with **Selective State Spaces**:
- It can remember relevant tokens and forget irrelevant tokens with an $O(1)$ constant-time recurrent state!
- During training, it uses a hardware-aware parallel prefix scan on GPU SRAM to train as fast as Attention!
