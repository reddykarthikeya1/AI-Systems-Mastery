# Lesson 02.04 — Converse, Inverse and Contrapositive

> **Module 02:** Logic for Precise Reasoning · Lesson 4 of 19

---

## What you will be able to do after this lesson

- [ ] Form the converse, inverse and contrapositive of a statement and say which is equivalent to it.
- [ ] Spot a converse error in an informal argument.

## Prerequisites

- [Lesson 02.03](03_Implication_and_Its_Traps.md) - implication.

---

## 1. The idea

Given `p → q`:

| Name | Form | Equivalent to the original? |
| :--- | :--- | :---: |
| Converse | `q → p` | **no** |
| Inverse | `¬p → ¬q` | **no** |
| Contrapositive | `¬q → ¬p` | **yes** |

Only the contrapositive is equivalent, and it is equivalent *always*. That makes
it a proof technique: to show `p → q`, it suffices to show `¬q → ¬p`, and
sometimes the second is far easier.

The converse and the inverse are equivalent to each other - each is the
contrapositive of the other - and neither follows from the original.

**Converse error** is asserting `q → p` from `p → q`. It is the most common
fallacy in informal reasoning about experiments, and it is easy to see once
named:

- "Overfitting causes a large train-test gap" does **not** give "a large gap
  means overfitting". Distribution shift produces the same gap.
- "A bug causes the test to fail" does not give "the test failed, so there is a
  bug" - the test itself may be wrong.

## 2. Worked example

Original: "if a matrix is invertible, its determinant is non-zero" - true.

- **Converse:** "if the determinant is non-zero, the matrix is invertible."
  Also true here, but that is a *separate fact*, not a consequence. For square
  matrices the two happen to be equivalent.
- **Inverse:** "if a matrix is not invertible, its determinant is zero." True,
  again separately.
- **Contrapositive:** "if the determinant is zero, the matrix is not
  invertible." True, and it *must* be - it is equivalent to the original.

A case where the converse genuinely fails: "if x > 2 then x² > 4" is true. Its
converse, "if x² > 4 then x > 2", is false - take x = -3, where x² = 9 > 4 and
x = -3 < 2.

The contrapositive of the original is "if x² ≤ 4 then x ≤ 2", which is true, as
it has to be.

## 3. Verify it in code

```python
from itertools import product

def implies(p, q):
    return (not p) or q

pairs = list(product([True, False], repeat=2))

original = [implies(p, q) for p, q in pairs]
converse = [implies(q, p) for p, q in pairs]
inverse = [implies(not p, not q) for p, q in pairs]
contrapositive = [implies(not q, not p) for p, q in pairs]

assert original == contrapositive, "the contrapositive is always equivalent"
assert original != converse, "the converse is not"
assert original != inverse
assert converse == inverse, "converse and inverse are equivalent to each other"

# A concrete converse failure.
forward = all(implies(x > 2, x * x > 4) for x in range(-10, 11))
assert forward, "x > 2 implies x^2 > 4"

backward = all(implies(x * x > 4, x > 2) for x in range(-10, 11))
assert not backward, "the converse fails"
assert (-3) ** 2 > 4 and not (-3 > 2), "x = -3 is the counterexample"

# And the contrapositive holds, as it must.
assert all(implies(not (x * x > 4), not (x > 2)) for x in range(-10, 11))
```

## 4. The mistake people actually make

**Reading a diagnostic backwards.**

"Overfitting produces a train-test gap" is a true implication. Observing a gap
and concluding overfitting is its converse, and it is not supported.

The practical cost: you respond with more regularisation and more data
augmentation, and the gap does not move, because the actual cause was that the
test set came from a different distribution. The remedy was chosen by an invalid
inference, and the time is gone.

The habit that prevents it: when a symptom appears, write down *every* condition
that implies it, not just the one you thought of first. A gap is implied by
overfitting, by distribution shift, by a leaky split scoring the training set
too high, and by a test set that is simply harder. Only then is it worth
gathering evidence to discriminate between them.

---

## Check yourself

1. Give the contrapositive of 'if the split leaks, the test score is optimistic'.
2. Why are the converse and the inverse equivalent to each other?
3. 'All effective models are large.' Someone builds a large model, finds it ineffective, and says the claim is refuted. Are they right?

<details>
<summary>Answers</summary>

1. 'If the test score is not optimistic, the split does not leak.' It is equivalent to the original.
2. The inverse `¬p → ¬q` is the contrapositive of the converse `q → p`, and a statement is always equivalent to its contrapositive.
3. No. The claim is `effective → large`. A large, ineffective model is `¬effective ∧ large`, which the claim permits. Refuting it requires an effective model that is *not* large.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](03_Implication_and_Its_Traps.md) · [Module README](../README.md) · [Next →](05_Biconditionals_and_Logical_Equivalence.md)
