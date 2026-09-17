# Lesson 09.28: Jensen's Inequality

## Learning Objectives
- State Jensen's inequality: f(E[X]) <= E[f(X)] for convex f.
- Apply Jensen's inequality to derive the Evidence Lower Bound (ELBO) in variational autoencoders.

## Prerequisites
- 09.25 Convex Functions Definition.

---

## 1. The Core Idea
For any random variable $X$ and convex function $g$:
$$g(\mathbb{E}[X]) \le \mathbb{E}[g(X)]$$
For strictly concave functions (like $\ln$), the inequality reverses: $\mathbb{E}[\ln(X)] \le \ln(\mathbb{E}[X])$.
This provides the mathematical cornerstone for Expectation-Maximization (EM) and VAE ELBO objectives.

---

## 2. Mathematical Exposition & Worked Example
Let $g(x) = x^2$ (convex). Let $X \in \{1, 3\}$ with equal probability $1/2$.
$\mathbb{E}[X] = 2 \implies g(\mathbb{E}[X]) = 2^2 = 4$.
$\mathbb{E}[g(X)] = \frac{1}{2}(1^2) + \frac{1}{2}(3^2) = \frac{1 + 9}{2} = 5$.
Indeed $4 \le 5$, with difference equal to $\text{Var}(X) = 1$.

---

## 3. Verify it in code

```python
import numpy as np
X = np.array([1.0, 3.0])
mean_x = np.mean(X)
g_mean = mean_x**2
mean_g = np.mean(X**2)

assert g_mean <= mean_g
assert np.isclose(g_mean, 4.0)
assert np.isclose(mean_g, 5.0)
assert np.isclose(mean_g - g_mean, np.var(X))
```

---

## 4. The mistake people actually make
Flipping the direction of the inequality for concave functions like log(x).

---

## Check yourself
1. What is Jensen's inequality for a convex function g and random variable X?
2. Why is Jensen's inequality fundamental to Variational Inference?

<details>
<summary>Answers</summary>

1. g(E[X]) <= E[g(X)].
2. It allows lower-bounding intractable log-marginal likelihoods log p(x) with tractable expected joint likelihoods (ELBO).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [29_Gradient_Descent_The_Update_Rule.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\29_Gradient_Descent_The_Update_Rule.md)
