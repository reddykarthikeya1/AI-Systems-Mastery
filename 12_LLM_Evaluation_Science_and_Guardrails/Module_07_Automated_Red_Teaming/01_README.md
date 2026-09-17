# Module 07: Automated Red Teaming

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
