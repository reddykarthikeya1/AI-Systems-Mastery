# Module 08: LLM From Scratch

> **AI Research Archive** · 4 lessons
> **Status:** 🔴 Scaffold — structure is in place, lesson content is not written.

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[README.md](README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[02_FOUNDATIONS_PLAYGROUND.md](02_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[03_try_it_yourself.py](03_try_it_yourself.py)** | Run in terminal (`python 03_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[01_Tokenization_BytePair_Encoding_From_Scratch.md](lessons/01_Tokenization_BytePair_Encoding_From_Scratch.md)** | Complete deep-dive curriculum lesson on 01 Tokenization Bytepair Encoding From Scratch. |
| **5** | **[02_Pretraining_a_Small_GPT.md](lessons/02_Pretraining_a_Small_GPT.md)** | Complete deep-dive curriculum lesson on 02 Pretraining A Small Gpt. |
| **6** | **[03_Sampling_Temperature_Topk_Topp_and_Beam_Search.md](lessons/03_Sampling_Temperature_Topk_Topp_and_Beam_Search.md)** | Complete deep-dive curriculum lesson on 03 Sampling Temperature Topk Topp And Beam Search. |
| **7** | **[04_Checkpoint_Train_Sample_and_Evaluate_Your_Own_LLM.md](lessons/04_Checkpoint_Train_Sample_and_Evaluate_Your_Own_LLM.md)** | Complete deep-dive curriculum lesson on 04 Checkpoint Train Sample And Evaluate Your Own Llm. |
| **8** | **[TROUBLESHOOTING_AND_EDGE_CASES.md](TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **9** | **[SELF_ASSESSMENT_AND_CHALLENGES.md](SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **10** | **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **11** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **12** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---


---


## Scaled Dot-Product Attention Pipeline

```mermaid
flowchart TD
    Q["Query Matrix Q<br/>(B, H, S_q, D)"] --> MatMul1["Batch MatMul: Q × K^T"]
    K["Key Matrix K<br/>(B, H, S_k, D)"] --> MatMul1
    MatMul1 --> Scale["Scale by 1 / sqrt(D)"]
    Scale --> Mask["Apply Causal Mask (Lower Triangular)"]
    Mask --> Softmax["Softmax along last dimension"]
    Softmax --> AttnWeights["Attention Probabilities P<br/>(B, H, S_q, S_k)"]
    AttnWeights --> MatMul2["Batch MatMul: P × V"]
    V["Value Matrix V<br/>(B, H, S_k, D)"] --> MatMul2
    MatMul2 --> Out["Context Output O<br/>(B, H, S_q, D)"]
```

## Why this module exists

<!-- The one question this module answers that no other module does. Two or
     three sentences, written before any lesson is drafted, because a module
     that cannot state its purpose in three sentences has the wrong scope. -->

TODO

## What you will be able to do

<!-- Module-level capabilities. These become the mastery checklist below. -->

- [ ] TODO
- [ ] TODO
- [ ] TODO

---

## Lessons

| # | Lesson | Status |
| :--- | :--- | :---: |
| 01 | [Tokenization: Byte-Pair Encoding From Scratch](lessons/01_Tokenization_BytePair_Encoding_From_Scratch.md) | 🔴 |
| 02 | [Pretraining a Small GPT](lessons/02_Pretraining_a_Small_GPT.md) | 🔴 |
| 03 | [Sampling: Temperature, Top-k, Top-p and Beam Search](lessons/03_Sampling_Temperature_Topk_Topp_and_Beam_Search.md) | 🔴 |
| 04 | [Checkpoint: Train, Sample and Evaluate Your Own LLM](lessons/04_Checkpoint_Train_Sample_and_Evaluate_Your_Own_LLM.md) | 🔴 |

---

## Module project

See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for the 3-tier build path.

- **Tier 1 — Foundational:** TODO
- **Tier 2 — Practitioner:** TODO
- **Tier 3 — Architect:** TODO

## Assessment

- [SELF_ASSESSMENT_AND_CHALLENGES.md](SELF_ASSESSMENT_AND_CHALLENGES.md) — quiz, challenges and diagnostics
- [TROUBLESHOOTING_AND_EDGE_CASES.md](TROUBLESHOOTING_AND_EDGE_CASES.md) — documented failure modes
- `debug_lab/` — planted defects that produce plausible wrong answers

## You have mastered this module when you can…

<!-- Ten items, each one a thing the learner DOES, not a thing they know. -->

1. TODO

---

## Directory tour

```
Module_08_LLM_From_Scratch/
├── README.md                            ← this file
├── PROJECT_GUIDE.md
├── SELF_ASSESSMENT_AND_CHALLENGES.md
├── TROUBLESHOOTING_AND_EDGE_CASES.md
├── lessons/                             ← 4 lessons
├── starter/                             ← stubs; the tests are the spec
├── project_solution/                    ← reference implementation + tests
└── debug_lab/                           ← defects to diagnose
```

## Navigation

- [Module 07 — Reinforcement Learning](../Module_07_Reinforcement_Learning/README.md)
- [Module 09 — Write Research Paper](../Module_09_Write_Research_Paper/README.md)
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md) · [Roadmap](../ROADMAP_AI_RESEARCH.md)