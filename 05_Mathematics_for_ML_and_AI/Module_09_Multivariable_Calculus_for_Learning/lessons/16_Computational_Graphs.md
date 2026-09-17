# Lesson 09.16: Computational Graphs

## Learning Objectives
- Represent mathematical expressions as Directed Acyclic Graphs (DAGs).
- Identify nodes as operations/tensors and edges as intermediate dependencies.

## Prerequisites
- 09.15 The Multivariable Chain Rule.

---

## 1. The Core Idea
A **computational graph** is a DAG where nodes represent input variables or primitive operations ($+, \times, \exp, \dots$), and directed edges represent data flow. Evaluating values along edges is the **forward pass**; propagating derivatives backwards is the **reverse pass**.

---

## 2. Mathematical Exposition & Worked Example
Expression $e = (a + b) \cdot (b + 1)$.
Let $c = a + b$, $d = b + 1$, $e = c \cdot d$.
At $a = 2, b = 3$: $c = 5, d = 4, e = 20$.
$\frac{\partial e}{\partial c} = d = 4$, $\frac{\partial e}{\partial d} = c = 5$.
$\frac{\partial e}{\partial a} = \frac{\partial e}{\partial c} \frac{\partial c}{\partial a} = 4(1) = 4$.
$\frac{\partial e}{\partial b} = \frac{\partial e}{\partial c} \frac{\partial c}{\partial b} + \frac{\partial e}{\partial d} \frac{\partial d}{\partial b} = 4(1) + 5(1) = 9$.

---

## 3. Verify it in code

```python
import numpy as np
a, b = 2.0, 3.0
c = a + b
d = b + 1.0
e = c * d

de_dc = d
de_dd = c
de_da = de_dc * 1.0
de_db = de_dc * 1.0 + de_dd * 1.0

assert np.isclose(e, 20.0)
assert np.isclose(de_da, 4.0)
assert np.isclose(de_db, 9.0)
```

---

## 4. The mistake people actually make
Forgetting that a shared node (like b appearing in both c and d) accumulates gradient contributions from all outgoing edges.

---

## Check yourself
1. What graph structure is used to represent neural network computation?
2. Why must gradients sum at branches during reverse accumulation?

<details>
<summary>Answers</summary>

1. A directed acyclic graph (DAG).
2. By the multivariable chain rule, each outgoing path contributes additively to total sensitivity.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [17_ForwardMode_Differentiation.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\17_ForwardMode_Differentiation.md)
