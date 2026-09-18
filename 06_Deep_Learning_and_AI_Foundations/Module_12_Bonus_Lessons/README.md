# Module 12: Bonus Lessons

> **AI Research Archive** · 3 lessons
> **Status:** 🔴 Scaffold — structure is in place, lesson content is not written.

---


## Chinchilla Compute-Optimal Scaling Frontier

```mermaid
flowchart TD
    Compute["Fixed FLOP Compute Budget C ≈ 6 N D"]
    Compute --> Opt["Compute-Optimal Allocation (Hoffmann et al.)"]
    Opt --> N["Scale Parameters N ∝ C^0.5"]
    Opt --> D["Scale Training Tokens D ∝ C^0.5"]
    Opt --> Ratio["Golden Ratio: ~20 Tokens per Model Parameter"]

    subgraph PreChinchilla["Legacy Oversized Models (Under-trained)"]
        GPT3["GPT-3: 175B parameters on 300B tokens (1.7 tokens/param - sub-optimal)"]
    end

    subgraph Modern["Modern Compute-Optimal Models"]
        LLaMA["LLaMA 3: 8B parameters on 15T tokens (Over-trained for serving inference efficiency)"]
    end
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
| 01 | [Reading a Paper Efficiently](lessons/01_Reading_a_Paper_Efficiently.md) | 🔴 |
| 02 | [Reproducing a Paper: A Worked Case](lessons/02_Reproducing_a_Paper_A_Worked_Case.md) | 🔴 |
| 03 | [Building a Research Portfolio](lessons/03_Building_a_Research_Portfolio.md) | 🔴 |

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
Module_12_Bonus_Lessons/
├── README.md                            ← this file
├── PROJECT_GUIDE.md
├── SELF_ASSESSMENT_AND_CHALLENGES.md
├── TROUBLESHOOTING_AND_EDGE_CASES.md
├── lessons/                             ← 3 lessons
├── starter/                             ← stubs; the tests are the spec
├── project_solution/                    ← reference implementation + tests
└── debug_lab/                           ← defects to diagnose
```

## Navigation

- [Module 11 — Machine Learning Operations (MLOps)](../Module_11_Machine_Learning_Operations_MLOps/README.md)
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md) · [Roadmap](../ROADMAP_AI_RESEARCH.md)