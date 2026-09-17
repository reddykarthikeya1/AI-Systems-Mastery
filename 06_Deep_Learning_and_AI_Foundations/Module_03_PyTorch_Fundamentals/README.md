# Module 03: PyTorch Fundamentals

> **AI Research Archive** · 9 lessons
> **Status:** 🔴 Scaffold — structure is in place, lesson content is not written.

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[README.md](README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[02_FOUNDATIONS_PLAYGROUND.md](02_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[03_try_it_yourself.py](03_try_it_yourself.py)** | Run in terminal (`python 03_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[01_Tensors_Devices_and_dtypes.md](lessons/01_Tensors_Devices_and_dtypes.md)** | Complete deep-dive curriculum lesson on 01 Tensors Devices And Dtypes. |
| **5** | **[02_Autograd_How_requiresgrad_Actually_Works.md](lessons/02_Autograd_How_requiresgrad_Actually_Works.md)** | Complete deep-dive curriculum lesson on 02 Autograd How Requiresgrad Actually Works. |
| **6** | **[03_nnModule_and_Parameter_Registration.md](lessons/03_nnModule_and_Parameter_Registration.md)** | Complete deep-dive curriculum lesson on 03 Nnmodule And Parameter Registration. |
| **7** | **[04_Datasets_DataLoaders_and_Collate_Functions.md](lessons/04_Datasets_DataLoaders_and_Collate_Functions.md)** | Complete deep-dive curriculum lesson on 04 Datasets Dataloaders And Collate Functions. |
| **8** | **[TROUBLESHOOTING_AND_EDGE_CASES.md](TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **9** | **[SELF_ASSESSMENT_AND_CHALLENGES.md](SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **10** | **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **11** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **12** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---


---


## PyTorch Tensor Memory Layout: Storage vs Strides

```mermaid
flowchart TD
    subgraph Logical["Logical 2D Tensor Shape (3 x 4)"]
        R0["Row 0: [a00, a01, a02, a03]"]
        R1["Row 1: [a10, a11, a12, a13]"]
        R2["Row 2: [a20, a21, a22, a23]"]
    end

    subgraph Physical["Flat 1D Storage Buffer (StorageOffset = 0, Strides = (4, 1))"]
        S["[a00, a01, a02, a03, a10, a11, a12, a13, a20, a21, a22, a23]"]
    end

    subgraph Transposed["Transposed View (4 x 3): Zero Memory Copy! Strides = (1, 4)"]
        T["Index Formula: offset = i * stride[0] + j * stride[1]"]
    end

    Logical --> Physical --> Transposed
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
| 01 | [Tensors, Devices and dtypes](lessons/01_Tensors_Devices_and_dtypes.md) | 🔴 |
| 02 | [Autograd: How requires_grad Actually Works](lessons/02_Autograd_How_requiresgrad_Actually_Works.md) | 🔴 |
| 03 | [nn.Module and Parameter Registration](lessons/03_nnModule_and_Parameter_Registration.md) | 🔴 |
| 04 | [Datasets, DataLoaders and Collate Functions](lessons/04_Datasets_DataLoaders_and_Collate_Functions.md) | 🔴 |
| 05 | [The Training Loop, Written Out Once](lessons/05_The_Training_Loop_Written_Out_Once.md) | 🔴 |
| 06 | [Optimizers, Schedulers and zero_grad](lessons/06_Optimizers_Schedulers_and_zerograd.md) | 🔴 |
| 07 | [Saving, Loading and Reproducibility](lessons/07_Saving_Loading_and_Reproducibility.md) | 🔴 |
| 08 | [Mixed Precision and torch.compile](lessons/08_Mixed_Precision_and_torchcompile.md) | 🔴 |
| 09 | [Checkpoint: Train a Classifier End to End](lessons/09_Checkpoint_Train_a_Classifier_End_to_End.md) | 🔴 |

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
Module_03_PyTorch_Fundamentals/
├── README.md                            ← this file
├── PROJECT_GUIDE.md
├── SELF_ASSESSMENT_AND_CHALLENGES.md
├── TROUBLESHOOTING_AND_EDGE_CASES.md
├── lessons/                             ← 9 lessons
├── starter/                             ← stubs; the tests are the spec
├── project_solution/                    ← reference implementation + tests
└── debug_lab/                           ← defects to diagnose
```

## Navigation

- [Module 02 — Core AI Intuitions](../Module_02_Core_AI_Intuitions/README.md)
- [Module 04 — TensorFlow Fundamentals](../Module_04_TensorFlow_Fundamentals/README.md)
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md) · [Roadmap](../ROADMAP_AI_RESEARCH.md)