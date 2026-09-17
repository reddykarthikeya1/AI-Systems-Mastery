# Lesson 06.03 — Angles, Cosine Similarity and Correlation

> **Module 06:** Orthogonality and Projections · Lesson 3 of 18

---

## What you will be able to do after this lesson

- [ ] Compute cosine similarity between embedding vectors.
- [ ] Prove that Pearson correlation is cosine similarity between centered vectors.

## Prerequisites

- 06.01 The Dot Product.

---

## 1. The idea

Cosine similarity $\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$ measures angular alignment independent of magnitude. Pearson correlation coefficient $r_{xy}$ is exactly the cosine similarity of mean-centered variables.

---

## 2. Worked example

Let $\mathbf{u} = [1, 2], \mathbf{v} = [2, 4]$. $\mathbf{u} \cdot \mathbf{v} = 10, \|\mathbf{u}\| = \sqrt{5}, \|\mathbf{v}\| = \sqrt{20} = 2\sqrt{5}$. $\cos(\theta) = 10 / 10 = 1.0$.

---

## 3. Verify it in code

```python
import numpy as np
u = np.array([1.0, 2.0, 3.0])
v = np.array([2.0, 4.0, 6.0])
cos_sim = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
assert np.isclose(cos_sim, 1.0)
# Pearson correlation is cosine similarity of centered vectors
uc = u - np.mean(u)
vc = v - np.mean(v)
assert np.isclose(np.dot(uc, vc) / (np.linalg.norm(uc) * np.linalg.norm(vc)), 1.0)
```

---

## 4. The mistake people actually make

Using Euclidean distance instead of cosine similarity for text embeddings where document length scales embedding norm.

---

## Check yourself

1. What is the range of cosine similarity for non-zero vectors?
2. How does Pearson correlation relate to cosine similarity?

<details>
<summary>Answers</summary>

1. Between -1.0 and +1.0.
2. Pearson correlation is identical to cosine similarity evaluated on centered vectors.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Orthogonal_and_Orthonormal_Vectors.md)
