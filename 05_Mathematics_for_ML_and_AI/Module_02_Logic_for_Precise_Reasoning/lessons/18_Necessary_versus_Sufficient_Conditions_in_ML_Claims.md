# Lesson 02.18 — Necessary versus Sufficient Conditions in ML Claims

> **Module 02:** Logic for Precise Reasoning · Lesson 18 of 19

---

## What you will be able to do after this lesson

- [ ] Distinguish necessary from sufficient conditions and place a claim correctly.
- [ ] Rewrite a vague ML claim as a precise implication and identify what evidence would settle it.

## Prerequisites

- [Lesson 02.05](05_Biconditionals_and_Logical_Equivalence.md) - biconditionals.

---

## 1. The idea

For `p → q`:

- **p is sufficient for q.** p being true is enough to guarantee q.
- **q is necessary for p.** p cannot hold without q.

Same implication, read from either end. If both `p → q` and `q → p`, then each
is necessary and sufficient for the other, which is `p ↔ q`.

The English that signals each:

| Phrase | Means |
| :--- | :--- |
| "p is enough for q", "p guarantees q" | `p → q` |
| "q is required for p", "only if q, then p" | `p → q` |
| "p only if q" | `p → q` — note the direction |
| "p if q" | `q → p` |
| "p if and only if q" | both |

"Only if" reverses what most people expect, and it is the phrase that appears in
theorem statements.

Why this matters for reading ML claims: "large models generalise better" is not
a proposition. Turned into "increasing parameters *is sufficient for* lower test
error", it is testable and false in general - past a point, without more data,
test error rises. Turned into "sufficient capacity is *necessary for* fitting
this function class", it is a different and defensible claim. The vague sentence
was standing in for both.

## 2. Worked example

**Claim.** "Being differentiable is sufficient for being continuous."

As an implication: `differentiable → continuous`. True.

The converse - `continuous → differentiable` - is false: `f(x) = |x|` is
continuous everywhere and not differentiable at 0. So differentiability is
sufficient but not necessary for continuity, and continuity is necessary but
not sufficient for differentiability.

**Claim.** "A convex objective is necessary for gradient descent to find the
global minimum."

As an implication this reads `finds global min → convex`. It is **false**:
gradient descent finds global minima of many non-convex functions, including
every neural network that trains successfully. Convexity is *sufficient* for the
guarantee, not necessary for the outcome.

That distinction is exactly the confusion that makes people believe non-convex
optimisation cannot work. Convexity guarantees success; its absence guarantees
nothing either way.

**A claim needing decomposition.** "Batch norm helps training."

Precisely: for which architectures, which optimisers, which learning rates, and
"helps" measured how? Until those are fixed, it is not a proposition and cannot
be confirmed or refuted - which is why the literature contains papers on both
sides.

## 3. Verify it in code

```python
# Differentiable implies continuous; the converse fails at |x|.
def continuous_at_zero(f, eps=1e-9):
    return abs(f(eps) - f(0)) < 1e-6 and abs(f(-eps) - f(0)) < 1e-6

def differentiable_at_zero(f, h=1e-6):
    left = (f(0) - f(-h)) / h
    right = (f(h) - f(0)) / h
    return abs(left - right) < 1e-3

abs_f = abs
assert continuous_at_zero(abs_f), "|x| is continuous at 0"
assert not differentiable_at_zero(abs_f), "and not differentiable there"

square = lambda x: x * x
assert continuous_at_zero(square) and differentiable_at_zero(square)

# So: differentiable -> continuous holds, continuous -> differentiable does not.
implies = lambda p, q: (not p) or q
assert implies(differentiable_at_zero(square), continuous_at_zero(square))
assert not implies(continuous_at_zero(abs_f), differentiable_at_zero(abs_f))

# Convexity is sufficient for "gradient descent finds the global min",
# not necessary: descent on a non-convex function can still succeed.
def descend(grad, x, lr=0.1, steps=500):
    for _ in range(steps):
        x -= lr * grad(x)
    return x

# f(x) = x^4 - is convex... and f(x) = x^2 * (x^2 - 1) + 0.25 is not.
convex_min = descend(lambda x: 4 * x ** 3, x=1.0)
assert abs(convex_min) < 0.1

non_convex_grad = lambda x: 4 * x ** 3 - 2 * x
found = descend(non_convex_grad, x=0.9)
assert abs(abs(found) - (0.5 ** 0.5)) < 0.01, "found a global minimiser anyway"
```

## 4. The mistake people actually make

**Treating a sufficient condition as necessary.**

"Convexity guarantees gradient descent reaches the global minimum" is true.
Concluding "so non-convex problems cannot be solved by gradient descent" is the
converse error from Lesson 02.04, and it is contradicted by every trained
network.

The general shape: a theorem gives conditions under which something is
*guaranteed*. Outside those conditions the outcome is *not guaranteed* - which is
a statement about the guarantee, not about the outcome. Things can still work;
you just have no theorem promising it.

This matters for how you read negative-sounding results. "No algorithm can do X
in general" leaves open that your instances are not general. "The bound does not
apply" is not "the method will fail".

The corrective habit is to write the implication down and check which direction
the evidence supports. Most disagreements about ML claims dissolve once both
parties write the arrow.

---

## Check yourself

1. 'A model is identifiable only if the design matrix has full rank.' Which is necessary and which is sufficient?
2. Is convexity necessary or sufficient for gradient descent to reach a global minimum?
3. Rewrite 'more data helps' as a precise implication and say what would refute it.

<details>
<summary>Answers</summary>

1. 'Only if' means `identifiable → full rank`. So full rank is necessary for identifiability; the statement does not claim it is sufficient.
2. Sufficient. Its absence removes the guarantee but does not prevent success - gradient descent finds global minima of many non-convex objectives.
3. For example: 'for this model class and fixed hyperparameters, increasing training set size never increases expected test error.' It is refuted by a case where adding data raises test error - which happens with label noise or distribution shift in the added data.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](17_Reading_a_Theorem_Statement_in_a_Paper.md) · [Module README](../README.md) · [Next →](19_Module_Project_Verify_or_Refute_Five_Published_Claims.md)
