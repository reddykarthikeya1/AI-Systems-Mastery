# Lesson 02.06 — Truth Tables and Tautologies

> **Module 02:** Logic for Precise Reasoning · Lesson 6 of 19

---

## What you will be able to do after this lesson

- [ ] Build a truth table for a compound expression and classify it as a tautology, contradiction or contingency.
- [ ] Use exhaustive enumeration to verify a claimed logical equivalence.

## Prerequisites

- [Lesson 02.05](05_Biconditionals_and_Logical_Equivalence.md) - equivalence.

---

## 1. The idea

A **truth table** lists every assignment of truth values to the variables and
the resulting value of the expression. With n variables there are 2ⁿ rows, and
enumerating them is a **decision procedure**: it settles any question about
propositional logic with certainty.

Three classifications:

| Kind | Meaning |
| :--- | :--- |
| **Tautology** | true on every row - e.g. `p ∨ ¬p` |
| **Contradiction** | false on every row - e.g. `p ∧ ¬p` |
| **Contingency** | true on some rows and false on others |

The connection to equivalence: `A ≡ B` exactly when `A ↔ B` is a tautology.
That turns "are these two conditions the same" into a mechanical check.

This completeness is unusual and worth appreciating. Propositional logic is
**decidable** - a finite procedure answers every question - which stops being
true the moment quantifiers over infinite domains appear in the next lesson.
The price of the guarantee is the 2ⁿ growth: 20 variables is a million rows,
30 is a billion, which is why SAT solvers exist and why SAT is NP-complete.

## 2. Worked example

Classify `(p → q) ∨ (q → p)`.

| p | q | `p → q` | `q → p` | `∨` |
| :-: | :-: | :-: | :-: | :-: |
| T | T | T | T | T |
| T | F | F | T | T |
| F | T | T | F | T |
| F | F | T | T | T |

True on every row, so it is a **tautology**. It says: for any two propositions,
at least one implies the other. That is startling in English and obvious from
the table - whenever `p → q` fails, p is true and q is false, which makes
`q → p` true.

Now `p ∧ ¬p`: false on both rows, a **contradiction**.

And `p → q`: true on three rows, false on one - a **contingency**. Its truth
depends on which case you are in, which is why it carries information; a
tautology carries none.

## 3. Verify it in code

```python
from itertools import product

def truth_table(fn, variables):
    return {vals: fn(*vals) for vals in product([True, False], repeat=variables)}

def classify(fn, variables):
    values = list(truth_table(fn, variables).values())
    if all(values):
        return "tautology"
    if not any(values):
        return "contradiction"
    return "contingency"

implies = lambda p, q: (not p) or q

assert classify(lambda p, q: implies(p, q) or implies(q, p), 2) == "tautology"
assert classify(lambda p: p and not p, 1) == "contradiction"
assert classify(lambda p: p or not p, 1) == "tautology"
assert classify(implies, 2) == "contingency"

# Equivalence is exactly "the biconditional is a tautology".
def equivalent(f, g, variables):
    return all(f(*v) == g(*v) for v in product([True, False], repeat=variables))

assert equivalent(lambda p, q: not (p and q),
                  lambda p, q: (not p) or (not q), 2)
assert classify(lambda p, q: (not (p and q)) == ((not p) or (not q)), 2) == "tautology"

# Contraposition, verified exhaustively.
assert equivalent(lambda p, q: implies(p, q),
                  lambda p, q: implies(not q, not p), 2)

# The cost of completeness: 2^n rows.
assert len(truth_table(lambda a, b, c: a and b and c, 3)) == 8
assert 2 ** 20 == 1_048_576
```

## 4. The mistake people actually make

**Testing a logical claim on a few cases and calling it verified.**

Checking three of eight rows is not a proof, and the rows you skip are usually
the asymmetric ones - the mixed assignments where two similar-looking
expressions diverge. Every equivalence error in this module differs only on
mixed rows.

Enumerating all 2ⁿ is cheap up to about 20 variables and is a genuine proof for
propositional logic. Do it.

The complementary error is assuming the method scales. At 40 variables the table
has 10¹² rows and is not enumerable, which is precisely the situation SAT
solvers were built for - and their existence is not a contradiction of
decidability but a response to its cost. When you find yourself wanting a truth
table over dozens of variables, the question has left the territory where brute
force is the answer.

---

## Check yourself

1. Classify `(p ∧ q) → p`.
2. How does a truth table settle whether two conditions are equivalent?
3. Why is propositional logic decidable while first-order logic is not?

<details>
<summary>Answers</summary>

1. A tautology. If both conjuncts hold then p holds, so the implication is true on every row.
2. Build both columns. They are equivalent exactly when the columns agree on every row, which is the same as the biconditional between them being a tautology.
3. Propositional logic has finitely many assignments - 2ⁿ - so exhaustive checking terminates. Quantifiers over infinite domains give infinitely many cases, so no finite enumeration settles them.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](05_Biconditionals_and_Logical_Equivalence.md) · [Module README](../README.md) · [Next →](07_Universal_and_Existential_Quantifiers.md)
