# 🐣 Interactive Foundations Playground: LLM From Scratch & KV-Cache

> *"Without KV-Cache, generating a 1,000-word essay requires recalculating the entire essay from word 1 on every single keystroke. With KV-Cache, you only calculate the new word!"*

---

## 1. What is an Autoregressive Language Model?

An LLM is a machine that plays one game:
$$P(w_{t} \mid w_1, w_2, \dots, w_{t-1})$$
Given the previous words, predict the probability distribution of the very next word!
When generating text:
1. Sample token $w_t$.
2. Append $w_t$ to the context.
3. Feed the new sequence back into the model to predict $w_{t+1}$.

---

## 2. The KV-Cache: The Engine of Fast Generation

In a standard transformer layer:
- $Q = X W_Q$
- $K = X W_K$
- $V = X W_V$

Notice something crucial:
When you generate token 100, **tokens 1 through 99 do not change**! Their Keys ($K$) and Values ($V$) are identical to what they were on the previous step!
- **Naive Generation ($O(N^2)$)**: Recomputes $K$ and $V$ for all 99 tokens again $\to$ massive waste of GPU FLOPs.
- **KV-Cache Generation ($O(N)$)**: Store $K_{1..99}$ and $V_{1..99}$ in GPU memory. Only compute $Q_{100}$, $K_{100}$, $V_{100}$. Append $K_{100}$ to cache, compute attention with the cached keys, and generate token 101!

---

## 3. Sampling Strategies: Temperature, Top-K, Top-P

Raw logits are converted to probabilities via $\text{Softmax}(z / T)$:
- **Temperature ($T$)**:
  - $T = 0.1$: Extremely sharp peaks $\implies$ focused, factual, greedy.
  - $T = 1.0$: True learned distribution.
  - $T = 2.0$: Uniform, chaotic, hallucinations.
- **Top-K**: Truncate logits to only the top $K$ highest-scoring tokens (e.g. $K=50$).
- **Top-P (Nucleus Sampling)**: Dynamically include only the smallest set of tokens whose cumulative probability reaches $P$ (e.g. $P=0.9$).
