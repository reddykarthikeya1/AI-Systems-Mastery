# Module 10: How to Fine-Tune Models

> **AI Research Archive** · 5 lessons
> **Status:** 🔴 Scaffold — structure is in place, lesson content is not written.

---


## Rotary Position Embedding (RoPE) 2D Subspace Rotation

```mermaid
flowchart LR
    subgraph Vector["Embedding Vector x (Dimension d)"]
        P1["Pair (x_0, x_1)"]
        P2["Pair (x_2, x_3)"]
        PK["Pair (x_{d-2}, x_{d-1})"]
    end

    subgraph Rotation["Orthogonal 2D Givens Rotations (Token Index m)"]
        R1["Rotate by m * θ₀"]
        R2["Rotate by m * θ₁"]
        RK["Rotate by m * θ_{d/2-1}"]
    end

    P1 --> R1
    P2 --> R2
    PK --> RK

    subgraph Prop["Inner Product Property"]
        IP["<R_m x, R_n y> = <x, R_{n-m} y> -> Pure Relative Distance!"]
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
| 01 | [Full Fine-Tuning versus Parameter-Efficient Methods](lessons/01_Full_FineTuning_versus_ParameterEfficient_Methods.md) | 🔴 |
| 02 | [LoRA and QLoRA](lessons/02_LoRA_and_QLoRA.md) | 🔴 |
| 03 | [Instruction Tuning and Dataset Construction](lessons/03_Instruction_Tuning_and_Dataset_Construction.md) | 🔴 |
| 04 | [Preference Optimization: RLHF and DPO](lessons/04_Preference_Optimization_RLHF_and_DPO.md) | 🔴 |
| 05 | [Checkpoint: Fine-Tune and Beat the Base Model on a Held-Out Set](lessons/05_Checkpoint_FineTune_and_Beat_the_Base_Model_on_a_HeldOut_Set.md) | 🔴 |

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
Module_10_How_to_FineTune_Models/
├── README.md                            ← this file
├── PROJECT_GUIDE.md
├── SELF_ASSESSMENT_AND_CHALLENGES.md
├── TROUBLESHOOTING_AND_EDGE_CASES.md
├── lessons/                             ← 5 lessons
├── starter/                             ← stubs; the tests are the spec
├── project_solution/                    ← reference implementation + tests
└── debug_lab/                           ← defects to diagnose
```

## Navigation

- [Module 09 — Write Research Paper](../Module_09_Write_Research_Paper/README.md)
- [Module 11 — Machine Learning Operations (MLOps)](../Module_11_Machine_Learning_Operations_MLOps/README.md)
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md) · [Roadmap](../ROADMAP_AI_RESEARCH.md)