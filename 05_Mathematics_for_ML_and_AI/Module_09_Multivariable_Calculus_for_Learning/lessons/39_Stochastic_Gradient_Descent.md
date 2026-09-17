# Lesson 09.39: Stochastic Gradient Descent

## Learning Objectives
- Formulate mini-batch SGD: g_B = (1/|B|) sum_{i in B} nabla L_i(theta).
- Prove that mini-batch gradients are unbiased estimators of the true population gradient: E[g_B] = nabla L(theta).

## Prerequisites
- 09.29 Gradient Descent: The Update Rule.

---

## 1. The Core Idea
Evaluating full gradients over billions of training samples is computationally impossible. **Stochastic Gradient Descent (SGD)** samples a mini-batch $B \subset \{1, \dots, N\}$ and estimates:
$$\mathbf{g}_B(\theta) = \frac{1}{|B|} \sum_{i \in B} \nabla \ell_i(\theta)$$
By linearity of expectation, $\mathbb{E}_{B}[\mathbf{g}_B(\theta)] = \nabla L(\theta)$. Mini-batch SGD is strictly **unbiased**.

---

## 2. Mathematical Exposition & Worked Example
Dataset of $N = 4$ samples with gradients $g \in \{2, 4, 6, 8\}$. Full batch gradient: $\frac{2+4+6+8}{4} = 5.0$.
Sample batch $B = \{1, 3\}$ (gradients 2 and 6): batch gradient $= \frac{2 + 6}{2} = 4.0$.
Expected value over all $\binom{4}{2} = 6$ pairs: $\frac{3 + 4 + 5 + 5 + 6 + 7}{6} = \frac{30}{6} = 5.0$.

---

## 3. Verify it in code

```python
import numpy as np
grads = np.array([2.0, 4.0, 6.0, 8.0])
full_grad = np.mean(grads)

# All pairs
from itertools import combinations
pair_means = [np.mean(pair) for pair in combinations(grads, 2)]
expected_sample_grad = np.mean(pair_means)

assert full_grad == 5.0
assert np.isclose(expected_sample_grad, full_grad)
```

---

## 4. The mistake people actually make
Confusing unbiasedness with zero variance; an individual mini-batch gradient can point far away from the true descent direction.

---

## Check yourself
1. Is the mini-batch gradient an unbiased estimator of the true dataset gradient?
2. Why is full-batch gradient descent impractical for modern LLMs?

<details>
<summary>Answers</summary>

1. Yes, E[g_B] = nabla L.
2. Because computing gradients over trillions of tokens per step is computationally and memory impossible.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [40_Variance_of_the_Stochastic_Gradient.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\40_Variance_of_the_Stochastic_Gradient.md)
