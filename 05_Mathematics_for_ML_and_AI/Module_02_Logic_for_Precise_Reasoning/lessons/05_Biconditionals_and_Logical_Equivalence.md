# Lesson 02.05 — Biconditionals and Logical Equivalence

> **Module 02:** Logic for Precise Reasoning · Lesson 5 of 19

---

## What you will be able to do after this lesson

- [ ] Use `↔` correctly and prove a biconditional by proving two implications.
- [ ] Distinguish logical equivalence from material equivalence on a particular input.

## Prerequisites

- [Lesson 02.04](04_Converse_Inverse_and_Contrapositive.md) - converse and contrapositive.

---

## 1. The idea

`p ↔ q` - *p if and only if q* - is true when p and q have the **same** truth
value.

| p | q | `p ↔ q` |
| :-: | :-: | :-: |
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | T |

The decomposition that matters for proofs:

    p ↔ q  ≡  (p → q) ∧ (q → p)

So proving "if and only if" is **two** proofs, and they are usually different in
character. "Only if" gives the forward direction `p → q`; "if" gives the
backward `q → p`. Papers routinely prove one and state both, and reading
carefully means noticing which was actually shown.

**Logical equivalence** (`≡`) is a stronger relation than `↔` being true on one
assignment. `p ≡ q` means they agree on *every* row of the truth table - it is a
statement about the expressions, not about a particular case. Two expressions
can both be true today and not be equivalent.

The same distinction appears in code as "these two functions returned the same
value on this input" versus "these two functions are the same function". Only
the second justifies replacing one with the other.

## 2. Worked example

Claim: "a square matrix is invertible **iff** its determinant is non-zero".

Two directions to prove:

1. invertible → det ≠ 0
2. det ≠ 0 → invertible

Both are true here, so the biconditional holds. Proving only direction 1 would
leave open the possibility of a singular matrix with non-zero determinant.

Now a case where a biconditional is *claimed* and only one direction is true:
"a set is convex iff it is connected". Every convex set is connected ✓. Not
every connected set is convex - an annulus is connected and has a hole ✗. So the
biconditional is false, and only "convex → connected" survives.

Equivalence versus agreement: the expressions `p ∧ q` and `p` agree when q is
true, so on that row `((p ∧ q) ↔ p)` is true. They are not equivalent, because
on `p=T, q=F` they differ. Checking one row is not checking the claim.

## 3. Verify it in code

```python
from itertools import product

pairs = list(product([True, False], repeat=2))

def iff(p, q):
    return p == q

assert [iff(p, q) for p, q in pairs] == [True, False, False, True]

# The decomposition into two implications.
implies = lambda p, q: (not p) or q
assert all(iff(p, q) == (implies(p, q) and implies(q, p)) for p, q in pairs)

# Logical equivalence is agreement on EVERY row.
left = [p and q for p, q in pairs]
right = [p for p, _ in pairs]
assert left != right, "p AND q is not equivalent to p"

# ...yet they agree on the rows where q is true.
agreeing = [(p, q) for p, q in pairs if q]
assert all((p and q) == p for p, q in agreeing)
assert all(iff(p and q, p) for p, q in agreeing), "true here, not equivalent"

# A genuine equivalence agrees everywhere.
assert [not (p and q) for p, q in pairs] == [(not p) or (not q) for p, q in pairs]

# Only one direction of a claimed biconditional may hold.
convex_implies_connected = True
connected_implies_convex = False    # an annulus is a counterexample
assert not (convex_implies_connected and connected_implies_convex)
```

## 4. The mistake people actually make

**Accepting "iff" when only one direction was demonstrated.**

A paper shows that its method attains low loss whenever a condition holds, and
then describes the condition as characterising low loss. That is one direction.
Unless the converse is also shown, a different mechanism could produce low loss
without the condition, and every claim built on the "characterisation" is
unsupported.

The reading habit: whenever you see "if and only if", "exactly when", or
"characterises", find both proofs. If only one appears, the other is an
assumption, and it may be the one your use case depends on.

In code the same error is replacing a function with a cheaper one because they
agreed on the test inputs. Agreement on a sample is not equivalence, and the
inputs where they differ are exactly the ones your tests did not contain.

---

## Check yourself

1. What two things must be proved to establish `p ↔ q`?
2. `p ∧ q` and `p` are both true when p and q are true. Are they logically equivalent?
3. A paper proves 'if the data satisfies C, the algorithm converges', then says C characterises convergence. What is missing?

<details>
<summary>Answers</summary>

1. `p → q` and `q → p`. The biconditional is the conjunction of the two implications, and they usually require different arguments.
2. No. Logical equivalence requires agreement on every assignment, and they differ when p is true and q is false.
3. The converse: that convergence implies C. Without it, the algorithm could converge for data violating C, so C is sufficient but not shown to be necessary.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](04_Converse_Inverse_and_Contrapositive.md) · [Module README](../README.md) · [Next →](06_Truth_Tables_and_Tautologies.md)
