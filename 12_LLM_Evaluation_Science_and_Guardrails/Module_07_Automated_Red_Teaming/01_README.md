# Module 07: Automated Red Teaming

## 1. Algorithmic Red Teaming Paradigms

Automated Red Teaming (ART) systematically probes AI safety boundaries using algorithmic mutation:

| Algorithm | Mechanism | Compute Cost | Attack Success Rate (ASR) |
| :--- | :--- | :--- | :--- |
| **PAIR** (Chao et al., 2023) | LLM-vs-LLM iterative refinement | Moderate (API calls) | High (~60-80%) |
| **GCG** (Zou et al., 2023) | Token gradient descent on suffix | Massive (White-box GPU) | Very High (>90%) |
| **TAP** (Mehrotra et al., 2023) | Tree of Attacks with pruning | High (Tree search) | High (~75%) |
| **Evolutionary Mutation** | Genetic crossover + mutation | Low | Moderate (~50%) |

---

## 2. Attack Success Rate (ASR) Formulation

For a test dataset of $N$ safety-sensitive concepts $\mathcal{C} = \{c_1, \dots, c_N\}$:

$$\text{ASR} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(\text{SafetyViolation}(\text{LLM}(\text{Mutate}(c_i))) = \text{TRUE})$$

A model is considered safety-certified only when $\text{ASR} < \tau$ (typically $\tau \le 1.0\%$ across all MLCommons hazard benchmarks).
