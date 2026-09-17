# Lesson 05.13 — Module Project: Spectral Clustering From Scratch

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 13 of 13

---

## What you will be able to do after this lesson

- [ ] Construct graph Laplacian L = D - W and compute its Fiedler vector.
- [ ] Perform spectral graph bi-partitioning in NumPy.

## Prerequisites

- All previous Module 05 lessons.

---

## 1. The idea

Spectral clustering uses the eigenvalues of the **graph Laplacian** $L = D - W$ to partition data points. The smallest eigenvalue $\lambda_1 = 0$ corresponds to the all-ones vector. The second smallest eigenvalue $\lambda_2$ (the Fiedler value) and its eigenvector (the **Fiedler vector**) bisect the graph along the bottleneck with minimal cut cost.

---

## 2. Worked example

Consider a graph of two connected cliques: vertices {0, 1} and {2, 3} with an edge between 1 and 2. The Fiedler vector assigns positive values to {0, 1} and negative values to {2, 3}, perfectly separating the clusters.

---

## 3. Verify it in code

```python
import numpy as np

# Adjacency matrix for two clusters connected by one bridge
W = np.array([
    [0.0, 1.0, 0.0, 0.0],
    [1.0, 0.0, 1.0, 0.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 0.0]
])

# Degree matrix D and Laplacian L = D - W
D = np.diag(np.sum(W, axis=1))
L = D - W

vals, vecs = np.linalg.eigh(L)
# Smallest eigenvalue is 0
assert np.isclose(vals[0], 0.0)

# Fiedler vector is the second eigenvector
fiedler = vecs[:, 1]
clusters = fiedler > 0
# Nodes 0 and 1 have one sign, nodes 2 and 3 have the opposite sign
assert clusters[0] == clusters[1]
assert clusters[2] == clusters[3]
assert clusters[0] != clusters[2]
```

---

## 4. The mistake people actually make

Clustering using the first eigenvector instead of the second. The first eigenvector is trivial (constant all ones vector) and contains no cluster separation info.

---

## Check yourself

1. What is the multiplicity of eigenvalue 0 for a graph with k connected components?
2. Why is the Fiedler vector used for clustering?

<details>
<summary>Answers</summary>

1. Exactly k.
2. Because it minimizes the continuous relaxation of the normalized cut problem, dividing nodes along the weakest connections.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md)
