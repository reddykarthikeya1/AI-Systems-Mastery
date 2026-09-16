# Lesson 02.03 — Implication and Its Traps

> **Module 02:** Logic for Precise Reasoning · Lesson 3 of 19

---

## What you will be able to do after this lesson

- [ ] State when `p → q` is false, and explain vacuous truth with an example.
- [ ] Rewrite an implication using `¬p ∨ q` and use it to negate one correctly.

## Prerequisites

- [Lesson 02.02](02_Conjunction_Disjunction_and_Negation.md) - the basic connectives.

---

## 1. The idea

`p → q` - *if p then q* - is **false in exactly one case**: p true and q false.

| p | q | `p → q` |
| :-: | :-: | :-: |
| T | T | T |
| T | F | **F** |
| F | T | T |
| F | F | T |

The bottom two rows are where intuition rebels. When p is false the implication
is **vacuously true**, because a promise whose condition never arose has not
been broken. "If it rains, I bring an umbrella" is not falsified by a dry day on
which I left the umbrella at home.

The equivalence that makes everything else easy:

    p → q  ≡  ¬p ∨ q

Read it as: *either the condition fails, or the consequence holds*. From it the
negation follows immediately:

    ¬(p → q) ≡ p ∧ ¬q

To refute an implication you need a case where the condition holds and the
conclusion does not - **a single counterexample**, and nothing else will do.
Showing that q sometimes fails is not enough; it must fail while p holds.

## 2. Worked example

Claim: "if the model is calibrated, then its Brier score is below 0.2".

To **refute** it you need `p ∧ ¬q`: a calibrated model whose Brier score is
0.25. One such model settles it.

These do *not* refute it:

- an uncalibrated model with a Brier score of 0.25 - that is `¬p ∧ ¬q`, row 4,
  and the implication is true there
- a calibrated model scoring 0.1 - that is `p ∧ q`, which supports it

Now the vacuous case in code. "Every element of this empty list is negative" is
`∀x ∈ [] : x < 0`, which unfolds to an implication over membership and is true.
Python agrees: `all(x < 0 for x in [])` is `True`.

Where that matters: a validator that reports "all rows passed" when zero rows
arrived is stating a true proposition and telling you nothing useful. The
correct response is not to change the logic - it is to check for emptiness
separately, because "no data" and "good data" are different situations.

## 3. Verify it in code

```python
from itertools import product

def implies(p, q):
    return (not p) or q

table = [implies(p, q) for p, q in product([True, False], repeat=2)]
assert table == [True, False, True, True]
assert sum(1 for v in table if not v) == 1, "false in exactly one case"

# Vacuous truth: the condition never arose.
assert implies(False, False) is True
assert implies(False, True) is True

# The two equivalences.
assert all(implies(p, q) == ((not p) or q) for p, q in product([True, False], repeat=2))
assert all((not implies(p, q)) == (p and not q)
           for p, q in product([True, False], repeat=2))

# Refuting an implication needs p true AND q false.
calibrated, brier = True, 0.25
assert implies(calibrated, brier < 0.2) is False, "this is a counterexample"

uncalibrated_bad = implies(False, 0.25 < 0.2)
assert uncalibrated_bad is True, "a bad uncalibrated model refutes nothing"

# all() over an empty collection is vacuously true.
assert all(x < 0 for x in []) is True
assert all([]) is True
```

## 4. The mistake people actually make

**Trying to refute an implication with a case where the condition does not hold.**

"You claimed calibrated models score below 0.2, but here is a model scoring
0.3." The immediate question is whether that model is calibrated. If it is not,
it lies in row 4 of the table, where the implication is true, and it is not
evidence against anything.

This is the single most common error in reading a paper's claims. A theorem
almost always reads "under conditions C, result R holds", and a counterexample
must satisfy C. A system that violates C and fails to achieve R is consistent
with the theorem.

The mirror-image error is treating a vacuous success as a real one. "The check
passed on all zero rows" is true and worthless. If your pipeline can produce an
empty batch, assert non-emptiness explicitly - the quantifier will not, and it
is not wrong to refuse.

---

## Check yourself

1. When is `p → q` false?
2. What is needed to refute 'if a model is deep, it generalises better'?
3. Rewrite `¬(p → q)` without an implication, and say why that form is useful.

<details>
<summary>Answers</summary>

1. Only when p is true and q is false. In the other three rows it is true, including both rows where p is false.
2. A model that *is* deep and does *not* generalise better - the pattern `p ∧ ¬q`. A shallow model that generalises poorly is irrelevant to the claim.
3. `p ∧ ¬q`. It is useful because it states exactly what a counterexample must look like: the hypothesis holds and the conclusion fails.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](02_Conjunction_Disjunction_and_Negation.md) · [Module README](../README.md) · [Next →](04_Converse_Inverse_and_Contrapositive.md)
