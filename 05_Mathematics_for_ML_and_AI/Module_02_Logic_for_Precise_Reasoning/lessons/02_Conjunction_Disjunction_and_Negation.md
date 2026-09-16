# Lesson 02.02 — Conjunction, Disjunction and Negation

> **Module 02:** Logic for Precise Reasoning · Lesson 2 of 19

---

## What you will be able to do after this lesson

- [ ] Build the truth table for `∧`, `∨` and `¬` from memory.
- [ ] Simplify a compound condition using the standard equivalences and verify the simplification exhaustively.

## Prerequisites

- [Lesson 02.01](01_Propositions_Truth_Values_and_Notation.md) - propositions and notation.

---

## 1. The idea

The three basic connectives, defined by what they do to truth values:

| p | q | `¬p` | `p ∧ q` | `p ∨ q` |
| :-: | :-: | :-: | :-: | :-: |
| T | T | F | T | T |
| T | F | F | F | T |
| F | T | T | F | T |
| F | F | T | F | F |

Conjunction is true on exactly one row; disjunction is false on exactly one.
That asymmetry is worth holding: **`∧` is hard to satisfy, `∨` is hard to
falsify.**

The equivalences you will actually use:

    ¬¬p ≡ p                              double negation
    p ∧ T ≡ p,      p ∨ F ≡ p            identity
    p ∧ F ≡ F,      p ∨ T ≡ T            domination
    p ∧ p ≡ p,      p ∨ p ≡ p            idempotence
    p ∧ q ≡ q ∧ p                        commutativity
    p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)      distributivity
    ¬(p ∧ q) ≡ ¬p ∨ ¬q                   De Morgan

Two equivalences are the same statement checked on every row of the truth table.
That is the only verification method that exists here, and it is complete - with
n variables there are 2ⁿ rows and checking them all is a proof.

## 2. Worked example

Simplify `(p ∧ q) ∨ (p ∧ ¬q)`.

By distributivity, `p ∧ (q ∨ ¬q)`. And `q ∨ ¬q` is always true, so the whole
expression is `p ∧ T`, which is `p`.

Check it on all four rows:

| p | q | `p ∧ q` | `p ∧ ¬q` | `(p∧q) ∨ (p∧¬q)` | `p` |
| :-: | :-: | :-: | :-: | :-: | :-: |
| T | T | T | F | T | T |
| T | F | F | T | T | T |
| F | T | F | F | F | F |
| F | F | F | F | F | F |

The last two columns agree on every row, so the equivalence holds. Four rows is
the entire space of possibilities for two variables, so this is a proof and not
evidence.

In practice this is the simplification that removes a redundant branch: a filter
written as "(active and premium) or (active and not premium)" is just "active",
and the second condition was never doing anything.

## 3. Verify it in code

```python
from itertools import product

def table(fn, arity=2):
    return [fn(*vals) for vals in product([True, False], repeat=arity)]

# The defining tables.
assert table(lambda p, q: p and q) == [True, False, False, False]
assert table(lambda p, q: p or q) == [True, True, True, False]
assert table(lambda p: not p, arity=1) == [False, True]

# Conjunction true on one row, disjunction false on one row.
assert sum(table(lambda p, q: p and q)) == 1
assert sum(table(lambda p, q: p or q)) == 3

# The simplification, checked exhaustively.
left = lambda p, q: (p and q) or (p and not q)
right = lambda p, q: p
assert table(left) == table(right)

# Distributivity, over all 8 assignments of three variables.
d_left = lambda p, q, r: p and (q or r)
d_right = lambda p, q, r: (p and q) or (p and r)
assert table(d_left, 3) == table(d_right, 3)

# De Morgan, and the wrong version that people write instead.
assert table(lambda p, q: not (p and q)) == table(lambda p, q: (not p) or (not q))
wrong = lambda p, q: (not p) and (not q)
assert table(lambda p, q: not (p and q)) != table(wrong)
assert table(wrong) == table(lambda p, q: not (p or q)), "it computes the OTHER law"
```

## 4. The mistake people actually make

**Simplifying a condition by intuition and not checking the table.**

`(a and b) or (a and not b)` reducing to `a` is easy to see. `not (a or (b and
c))` is not, and a wrong simplification changes which rows a filter keeps while
still looking sensible.

The check is mechanical and cheap: with n variables enumerate all 2ⁿ
assignments and compare outputs. Three variables is eight rows. If the two
expressions agree on all of them they are equivalent, full stop - there is
nothing else to verify, because the table *is* the semantics.

The related trap is short-circuit evaluation. In Python `a and f(x)` does not
call `f` when `a` is false, so rewriting it as `f(x) and a` is logically
equivalent and operationally different - it can raise, or be slow, or have side
effects. Logical equivalence says nothing about evaluation order.

---

## Check yourself

1. Simplify `p ∨ (p ∧ q)`.
2. How many rows does a truth table with 4 variables have, and why is checking them all a proof?
3. Are `a and f(x)` and `f(x) and a` logically equivalent? Operationally identical?

<details>
<summary>Answers</summary>

1. `p`. This is absorption: if p is true the whole thing is true, and if p is false both disjuncts are false.
2. 2⁴ = 16. The rows enumerate every possible assignment of truth values, so agreement on all of them leaves no case in which the two expressions could differ.
3. Logically equivalent - `∧` is commutative. Not operationally identical: Python short-circuits, so the first does not call `f` when `a` is false. If `f` raises or has side effects, the two behave differently.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](01_Propositions_Truth_Values_and_Notation.md) · [Module README](../README.md) · [Next →](03_Implication_and_Its_Traps.md)
