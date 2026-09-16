# Lesson 02.17 — Reading a Theorem Statement in a Paper

> **Module 02:** Logic for Precise Reasoning · Lesson 17 of 19

---

## What you will be able to do after this lesson

- [ ] Decompose a theorem statement into hypotheses, conclusion and quantifier structure.
- [ ] Identify which hypothesis a result depends on most, and what fails when it is dropped.

## Prerequisites

- [Lesson 02.08](08_Nested_Quantifiers_and_Why_Order_Matters.md) - quantifier order.
- [Lesson 02.09](09_Negating_Quantified_Statements.md) - negation.

---

## 1. The idea

A theorem in a paper is an implication with quantifiers, written in prose. The
reading procedure:

1. **Find the conclusion.** Usually after "then", or the displayed inequality.
2. **List every hypothesis.** Including the ones stated far away - in a
   "Setting" section, an earlier assumption, or a footnote.
3. **Write the quantifier structure.** Which variables are universally
   quantified, which existentially, and in what order.
4. **Ask what is uniform.** A constant that does not depend on n or on the
   function class is a much stronger claim than one that does.
5. **Negate it.** What would a counterexample have to look like? That tells you
   whether your situation is even covered.

Step 4 is where most of the content hides. "There exists a constant C such that
for all n..." is a genuine bound. "For all n there exists a constant C..." is
almost vacuous, because C may grow with n without limit.

And step 2 is where most misapplications begin: the hypothesis that matters is
usually the one stated once, early, and never repeated.

## 2. Worked example

A typical generalisation bound:

> **Theorem.** Let `F` be a hypothesis class with VC dimension d. For any
> distribution D and any `δ > 0`, with probability at least `1 - δ` over a
> sample of size n drawn i.i.d. from D, for all `f ∈ F`:
>
>     R(f) ≤ R̂(f) + √((d log(n/d) + log(1/δ)) / n)

Decompose it.

- **Conclusion:** the displayed inequality bounding true risk by empirical risk
  plus a term.
- **Hypotheses:** `F` has finite VC dimension d; the sample is i.i.d. from D;
  `δ > 0`.
- **Quantifiers:** `∀D ∀δ ∀F` and, crucially, **`∀f ∈ F`** *inside* the
  probability. The bound holds for every f simultaneously, not for a
  pre-chosen f.
- **What is uniform:** the bound is over the whole class at once. That is what
  makes it applicable to the f your algorithm selected *after* seeing the data.
- **Negation:** a distribution, a δ, and a sample of size n on which some
  `f ∈ F` violates the inequality, with probability more than δ.

Drop "i.i.d." and the theorem says nothing - which matters, because time series
and grouped data are not i.i.d., and the bound is routinely quoted for them.

Note also what is *not* claimed: nothing about the bound being tight, and
nothing about which f the algorithm will find.

## 3. Verify it in code

```python
import math

def bound(d, n, delta):
    return math.sqrt((d * math.log(n / d) + math.log(1 / delta)) / n)

# The bound shrinks as n grows - the shape of the claim.
values = [bound(d=10, n=n, delta=0.05) for n in (100, 1_000, 10_000, 100_000)]
assert all(a > b for a, b in zip(values, values[1:])), "decreasing in n"
assert values[-1] < values[0] / 5

# It grows with the capacity d: a richer class needs more data.
assert bound(d=100, n=10_000, delta=0.05) > bound(d=10, n=10_000, delta=0.05)

# The confidence term enters logarithmically - tightening delta is cheap.
tight = bound(d=10, n=10_000, delta=0.001)
loose = bound(d=10, n=10_000, delta=0.05)
assert tight > loose
assert tight / loose < 1.5, "a 50x smaller delta costs under 50% in the bound"

# "Uniform over the class" is the load-bearing quantifier: it must hold for the
# f chosen AFTER seeing the data, which is why the bound is over all f at once.
class_size = 5
empirical = [0.10, 0.12, 0.09, 0.15, 0.11]
gap = bound(d=10, n=10_000, delta=0.05)
assert all(r + gap >= r for r in empirical)
selected = min(empirical)                       # chosen using the data
assert selected + gap >= selected, "still covered, because the bound is uniform"
```

## 4. The mistake people actually make

**Quoting a bound whose hypotheses your setting violates.**

Generalisation bounds assume i.i.d. sampling. Time series, grouped records and
data with distribution shift all violate it, and the bound then guarantees
nothing - it is not merely loose, it is inapplicable.

This is the implication trap from Lesson 02.03 at full scale: the theorem is
`hypotheses → conclusion`, and a setting that fails the hypotheses is row 3 or 4
of the truth table, where the implication is true and uninformative.

Two more reading errors worth naming:

- **Missing the uniformity.** A bound holding for each fixed f separately does
  not cover an f selected using the data. Only the uniform version does, and
  that is the difference between a usable theorem and a useless one.
- **Reading a bound as an estimate.** `R(f) ≤ R̂(f) + ε` says the true risk is no
  worse than that. It does not say it is close to it. Most VC bounds are
  numerically enormous at realistic n and are still true.

---

## Check yourself

1. What are the five steps for reading a theorem statement?
2. Why is `∀f ∈ F` inside the probability the important part of a generalisation bound?
3. A bound assumes i.i.d. data and you have a time series. What does the bound tell you?

<details>
<summary>Answers</summary>

1. Find the conclusion; list every hypothesis including distant ones; write the quantifier structure; ask what is uniform; negate it to see what a counterexample would be.
2. Because the algorithm selects f after seeing the data. A bound holding for each fixed f separately does not apply to a data-dependent choice; only a bound uniform over the whole class does.
3. Nothing. The hypothesis fails, so the implication is vacuously true and carries no information about your case. It is not a loose bound - it is an inapplicable one.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](16_Counterexamples_and_Disproof.md) · [Module README](../README.md) · [Next →](18_Necessary_versus_Sufficient_Conditions_in_ML_Claims.md)
