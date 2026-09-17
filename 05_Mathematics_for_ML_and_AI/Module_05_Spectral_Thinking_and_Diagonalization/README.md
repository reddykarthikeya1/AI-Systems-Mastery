# Module 05: Spectral Thinking and Diagonalization

> **ML Math** · 13 lessons
> **Status:** 🔴 Scaffold — structure is in place, lesson content is not written.

---


## Spectral Thinking: Eigenvector Invariance (Av = λv)

```mermaid
flowchart TD
    subgraph Arbitrary["Arbitrary Vector x"]
        x["x (Rotates and Scales under A)"]
    end

    subgraph Eigen["Eigenvector v"]
        v["Eigenvector v (Direction is Invariant!)"] --> Scale["Scaled purely by Scalar λ:<br/>A v = λ v"]
    end

    subgraph Eigendecomp["Matrix Diagonalization"]
        Diag["A = Q Λ Q⁻¹ = Σ λᵢ qᵢ qᵢᵀ"]
    end

    Scale --> Diag
```

## Why this module exists

<!-- GENERATED_ALGORITHM_DIAGRAM: EIGENVECTOR_SVG START -->

![Eigenvector Invariance and Linear Transformation](../assets/eigenvector_transformation.svg)

<!-- GENERATED_ALGORITHM_DIAGRAM: EIGENVECTOR_SVG END -->

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
| 01 | [Eigenvectors: Directions a Map Does Not Turn](lessons/01_Eigenvectors_Directions_a_Map_Does_Not_Turn.md) | 🔴 |
| 02 | [Eigenvalues and the Characteristic Polynomial](lessons/02_Eigenvalues_and_the_Characteristic_Polynomial.md) | 🔴 |
| 03 | [Computing Eigenvalues by Hand](lessons/03_Computing_Eigenvalues_by_Hand.md) | 🔴 |
| 04 | [Eigenspaces and Geometric Multiplicity](lessons/04_Eigenspaces_and_Geometric_Multiplicity.md) | 🔴 |
| 05 | [Algebraic versus Geometric Multiplicity](lessons/05_Algebraic_versus_Geometric_Multiplicity.md) | 🔴 |
| 06 | [Diagonalization: When and Why](lessons/06_Diagonalization_When_and_Why.md) | 🔴 |
| 07 | [Similar Matrices and Their Invariants](lessons/07_Similar_Matrices_and_Their_Invariants.md) | 🔴 |
| 08 | [Matrix Powers via Diagonalization](lessons/08_Matrix_Powers_via_Diagonalization.md) | 🔴 |
| 09 | [Defective Matrices and Jordan Form](lessons/09_Defective_Matrices_and_Jordan_Form.md) | 🔴 |
| 10 | [Complex Eigenvalues and Rotation](lessons/10_Complex_Eigenvalues_and_Rotation.md) | 🔴 |
| 11 | [The Spectral Theorem for Symmetric Matrices](lessons/11_The_Spectral_Theorem_for_Symmetric_Matrices.md) | 🔴 |
| 12 | [Power Iteration and How PageRank Works](lessons/12_Power_Iteration_and_How_PageRank_Works.md) | 🔴 |
| 13 | [Module Project: Spectral Clustering From Scratch](lessons/13_Module_Project_Spectral_Clustering_From_Scratch.md) | 🔴 |

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
Module_05_Spectral_Thinking_and_Diagonalization/
├── README.md                            ← this file
├── PROJECT_GUIDE.md
├── SELF_ASSESSMENT_AND_CHALLENGES.md
├── TROUBLESHOOTING_AND_EDGE_CASES.md
├── lessons/                             ← 13 lessons
├── starter/                             ← stubs; the tests are the spec
├── project_solution/                    ← reference implementation + tests
└── debug_lab/                           ← defects to diagnose
```

## Navigation

- [Module 04 — Vector Spaces, Bases and Rank](../Module_04_Vector_Spaces_Bases_and_Rank/README.md)
- [Module 06 — Orthogonality and Projections](../Module_06_Orthogonality_and_Projections/README.md)
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md) · [Roadmap](../ROADMAP_ML_MATH.md)