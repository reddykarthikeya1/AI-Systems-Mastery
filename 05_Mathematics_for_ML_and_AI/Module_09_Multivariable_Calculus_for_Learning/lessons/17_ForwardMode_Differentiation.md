# Lesson 09.17: Forward-Mode Differentiation

## Learning Objectives
- Implement forward-mode automatic differentiation using dual numbers a + b eps with eps^2 = 0.
- Understand when forward mode is optimal (f: R -> R^m).

## Prerequisites
- 09.16 Computational Graphs.

---

## 1. The Core Idea
**Forward-mode AD** propagates directional derivatives forward alongside primal values using **dual numbers** $x + \dot{x}\epsilon$ where $\epsilon^2 = 0$. One forward pass computes the directional derivative $\mathbf{J} \mathbf{v}$.
Cost: $O(n)$ forward passes for $n$ inputs. Ideal when input dimension $n \ll$ output dimension $m$.

---

## 2. Mathematical Exposition & Worked Example
Function $f(x) = x^2 + 3x$. With dual number $x = 2 + 1\epsilon$:
$f(2 + \epsilon) = (2 + \epsilon)^2 + 3(2 + \epsilon) = 4 + 4\epsilon + 6 + 3\epsilon = 10 + 7\epsilon$.
Value is 10, derivative is 7!

---

## 3. Verify it in code

```python
class Dual:
    def __init__(self, val, der=0.0):
        self.val = float(val)
        self.der = float(der)
    def __add__(self, o):
        o = o if isinstance(o, Dual) else Dual(o, 0.0)
        return Dual(self.val + o.val, self.der + o.der)
    def __mul__(self, o):
        o = o if isinstance(o, Dual) else Dual(o, 0.0)
        return Dual(self.val * o.val, self.val * o.der + self.der * o.val)

x = Dual(2.0, 1.0)
y = x * x + Dual(3.0) * x
assert y.val == 10.0
assert y.der == 7.0
```

---

## 4. The mistake people actually make
Attempting to use forward-mode AD to train deep networks with millions of parameters; requiring 1 pass per parameter makes it computationally intractable.

---

## Check yourself
1. What is a dual number?
2. When is forward-mode AD faster than reverse-mode AD?

<details>
<summary>Answers</summary>

1. A number a + b eps where eps is an infinitesimal element satisfying eps^2 = 0.
2. When the number of inputs n is much smaller than the number of outputs m (n << m).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [18_ReverseMode_Differentiation.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\18_ReverseMode_Differentiation.md)
