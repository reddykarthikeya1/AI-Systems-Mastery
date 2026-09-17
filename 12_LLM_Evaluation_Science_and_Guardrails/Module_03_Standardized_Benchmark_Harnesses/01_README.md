# Module 03: Standardized Benchmark Harnesses


## LLM-as-a-Judge Pairwise Arena & Position Bias Calibration

```mermaid
flowchart TD
    Prompt["Benchmark Prompt"] --> M1["Model A Response"]
    Prompt --> M2["Model B Response"]

    subgraph Round1["Evaluation Round 1: [Model A, Model B]"]
        Judge1["Judge LLM: Select Winner (Round 1)"]
    end

    subgraph Round2["Evaluation Round 2: [Model B, Model A] (Position Swap!)"]
        Judge2["Judge LLM: Select Winner (Round 2)"]
    end

    M1 & M2 --> Round1
    M1 & M2 --> Round2

    Round1 & Round2 --> Calibrate["Bias Filter: Only award win if choice is consistent across both positions!"]
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

## 1. Landmark AI Benchmarks & Evaluation Paradigms

Standardized benchmarks form the bedrock of AI capabilities evaluation:

| Benchmark | Target Capability | Format | Metric |
| :--- | :--- | :--- | :--- |
| **MMLU** (Hendrycks et al.) | General Knowledge across 57 subjects | 4-choice Multiple Choice | Macro-averaged Accuracy |
| **GSM8K** (Cobbe et al.) | Multi-step Grade School Math | CoT Free-form generation | Exact numeric match |
| **HumanEval** (Chen et al.) | Python Code Generation | Functional execution | Pass@k on hidden unit tests |
| **TruthfulQA** (Lin et al.) | Hallucination & Common Misconceptions | Adversarial QA | Truthfulness % + Informative % |

---

## 2. Pass@k Unbiased Estimator Formulation

Evaluating Pass@k by drawing $k$ samples directly requires generating millions of tokens. Chen et al. derived an unbiased minimum-variance estimator from $n \ge k$ total generations:

$$\widehat{\text{Pass}@k} = \mathbb{E}\left[ 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}} \right]$$

where $n$ is total candidate samples per task, and $c$ is the number of correct solutions ($0 \le c \le n$).

---

## 3. Data Contamination & Decontamination Auditing

Pre-training corpora (Common Crawl, The Pile, GitHub) frequently ingest benchmark test splits.
Decontamination techniques:
1. **$N$-gram Overlap Filtering**: Any training document sharing an 8-gram or 13-gram with a benchmark test question is flagged as contaminated.
2. **Perplexity Probing**: Comparing cross-entropy loss on benchmark test questions versus syntactically perturbed controls. If loss drops sharply on the original, memorization is confirmed.