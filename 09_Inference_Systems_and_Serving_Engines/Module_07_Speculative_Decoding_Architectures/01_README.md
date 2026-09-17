# Module 07: Speculative Decoding & Medusa Architectures


## LLM Weight & Activation Quantization Formats

```mermaid
flowchart LR
    FP16["FP16 / BF16<br/>(16 bits, Baseline)"] --> FP8["FP8 (E4M3 / E5M2)<br/>(8 bits, 2x Memory & Speed)"]
    FP8 --> INT4["INT4 / AWQ / GPTQ<br/>(4 bits, 3.5x Memory Reduction)"]

    subgraph Tradeoff["Accuracy vs Performance Frontier"]
        Desc["AWQ preserves top 1% salient weight channels to maintain perplexity!"]
    end

    INT4 --> Tradeoff
```

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[00_try_it_yourself.py](00_try_it_yourself.py)** | Run in terminal (`python 00_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **5** | **[03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **6** | **[02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **7** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **8** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---

## 1. Mathematical Formulation of Speculative Decoding

Speculative Decoding (Leviathan et al., ICML 2023; Chen et al., 2023) breaks the sequential autoregressive dependency by decoupling candidate token proposal from candidate token verification.

### 1.1 Rejection Sampling with Exact Distribution Preservation
Let $M_p$ denote the large target model with probability distribution $p(x | x_{<t})$ and $M_q$ denote the small draft model with distribution $q(x | x_{<t})$.
Given $\gamma$ speculative draft tokens $(x_1, x_2, \dots, x_\gamma)$:
1. Concurrently evaluate target model logits $p(x_i | x_{<i})$ for all $i \in \{1, \dots, \gamma+1\}$ in a single forward pass.
2. For each draft token $x_i$, accept $x_i$ with probability:
   $$\alpha_i = \min\left(1, \frac{p(x_i)}{q(x_i)}\right)$$
3. If token $x_k$ is rejected, discard tokens $x_{k+1} \dots x_\gamma$.
4. Sample replacement token $x_k$ from the normalized residual distribution:
   $$p'(x) = \frac{\max(0, p(x) - q(x))}{\sum_y \max(0, p(y) - q(y))}$$

**Theorem**: The sampled token sequence follows distribution $p(x)$ exactly. Speculative decoding guarantees zero degradation in perplexity or task accuracy.

---

## 2. Medusa: Multi-Head Speculation Without Draft Models

Medusa (Cai et al., 2024) eliminates the secondary draft model:
- Multiple lightweight feed-forward heads are attached on top of the target model's final hidden state.
- Head $k$ predicts the token at step $t + k$.
- Candidate sequences are verified using a **Tree Attention** mask in the next forward pass.