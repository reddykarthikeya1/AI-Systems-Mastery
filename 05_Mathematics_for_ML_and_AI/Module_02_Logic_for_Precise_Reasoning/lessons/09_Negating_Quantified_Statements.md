# Lesson 02.09 — Negating Quantified Statements

> **Module 02:** Logic for Precise Reasoning · Lesson 9 of 19

---

## What you will be able to do after this lesson

- [ ] Negate a quantified statement mechanically, including nested quantifiers.
- [ ] Use the negation rule to state precisely what a counterexample must look like.

## Prerequisites

- [Lesson 02.08](08_Nested_Quantifiers_and_Why_Order_Matters.md) - nested quantifiers.

---

## 1. The idea

Negation swaps the quantifiers and negates the body:

    ¬(∀x : P(x))  ≡  ∃x : ¬P(x)
    ¬(∃x : P(x))  ≡  ∀x : ¬P(x)

In words: *not everything has the property* means *something lacks it*; *nothing
has it* means *everything lacks it*.

For nested quantifiers, apply the rule from the outside in, flipping each in
turn:

    ¬(∀x ∃y : P(x,y))  ≡  ∃x ∀y : ¬P(x,y)
    ¬(∀ε ∃δ ∀x : P)    ≡  ∃ε ∀δ ∃x : ¬P

This is mechanical, and that is the point: it turns "what would disprove this?"
from a puzzle into a procedure.

Combined with the implication rule `¬(p → q) ≡ p ∧ ¬q`, it gives the exact shape
of a counterexample. Negating

    ∀x : (P(x) → Q(x))

gives

    ∃x : P(x) ∧ ¬Q(x)

- one object satisfying the hypothesis and failing the conclusion. Nothing less
will do, and nothing more is needed.

## 2. Worked example

Claim: "every calibrated model has Brier score below 0.2", i.e.

    ∀m : (C(m) → B(m) < 0.2)

Negate it:

    ¬∀m : (...)        ≡  ∃m : ¬(C(m) → B(m) < 0.2)
                       ≡  ∃m : C(m) ∧ ¬(B(m) < 0.2)
                       ≡  ∃m : C(m) ∧ B(m) ≥ 0.2

So: exhibit one calibrated model with Brier score at least 0.2. The procedure
told us the model must be calibrated - which is the step people skip.

Now a nested one. Uniform convergence of `fₙ` to `f`:

    ∀ε > 0 ∃N ∀n ≥ N ∀x : |fₙ(x) - f(x)| < ε

Negated:

    ∃ε > 0 ∀N ∃n ≥ N ∃x : |fₙ(x) - f(x)| ≥ ε

Read it back: there is a tolerance ε such that, no matter how far out you go,
you can still find an index beyond it and a point where the gap is at least ε.
That is precisely what "converges pointwise but not uniformly" looks like, and
the negation produced it mechanically.

## 3. Verify it in code

```python
models = [(True, 0.15), (True, 0.25), (False, 0.30)]   # (calibrated, brier)

claim = all((not c) or (b < 0.2) for c, b in models)
assert claim is False

# The negation says what a counterexample must be: calibrated AND brier >= 0.2.
counterexamples = [(c, b) for c, b in models if c and b >= 0.2]
assert counterexamples == [(True, 0.25)]

# The uncalibrated bad model is NOT a counterexample.
assert (False, 0.30) not in counterexamples

# Mechanical negation over a finite domain.
domain = range(1, 6)
P = lambda x: x % 2 == 0

assert (not all(P(x) for x in domain)) == any(not P(x) for x in domain)
assert (not any(P(x) for x in domain)) == all(not P(x) for x in domain)

# Nested: not (for all x, exists y) == exists x, for all y not.
Q = lambda x, y: x + y > 8
left = not all(any(Q(x, y) for y in domain) for x in domain)
right = any(all(not Q(x, y) for y in domain) for x in domain)
assert left == right is True

# And the witness the negation promises.
bad_x = next(x for x in domain if all(not Q(x, y) for y in domain))
assert bad_x == 1, "x = 1 has no y in 1..5 with 1 + y > 8"
```

## 4. The mistake people actually make

**Negating an implication by negating both sides.**

`¬(P → Q)` is **not** `¬P → ¬Q`. It is `P ∧ ¬Q`.

The consequence in practice: asked to disprove "if the data is IID then the
bound holds", people look for non-IID data where the bound fails. That satisfies
`¬P ∧ ¬Q` and refutes nothing - the claim says nothing about non-IID data.

The mechanical procedure prevents it. Write the statement in symbols, apply
`¬∀ → ∃¬`, then `¬(P → Q) ≡ P ∧ ¬Q`, and read off what to look for. Every step
is forced.

The same discipline turns a vague objection into a testable one. "I do not think
that holds in general" becomes "then there is an x with P(x) and not Q(x) - what
is it?", and either the example appears or the objection does not.

---

## Check yourself

1. Negate: 'every batch contains at least one positive example.'
2. Negate `∀x : (P(x) → Q(x))` and say what a counterexample looks like.
3. Why is `¬P → ¬Q` the wrong negation of `P → Q`?

<details>
<summary>Answers</summary>

1. 'Some batch contains no positive example' - `∃b ∀x ∈ b : ¬positive(x)`.
2. `∃x : P(x) ∧ ¬Q(x)`. A single object that satisfies the hypothesis and fails the conclusion.
3. `¬P → ¬Q` is the inverse, which is not even equivalent to the original, let alone its negation. The negation is `P ∧ ¬Q`, a conjunction rather than an implication.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](08_Nested_Quantifiers_and_Why_Order_Matters.md) · [Module README](../README.md) · [Next →](10_Direct_Proof.md)
