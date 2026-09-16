# Lesson 01.11 — Functions as Special Relations

> **Module 01:** Set Language for Machine Learning · Lesson 11 of 25

---

## What you will be able to do after this lesson

- [ ] State the two conditions that make a relation a function, and test them.
- [ ] Identify the domain, codomain and range of a function, and say why codomain and range differ.

## Prerequisites

- [Lesson 01.09](09_Relations_as_Subsets_of_a_Product.md) - relations.

---

## 1. The idea

A **function** `f : A → B` is a relation from A to B in which

1. **every** element of A appears as a first component - it is *total*, and
2. **no** element of A appears twice - it is *single-valued*.

Together: each input has exactly one output. That is all a function is - a
relation with those two restrictions.

Three sets, and the third is the one people conflate:

- the **domain** A: everything the function accepts
- the **codomain** B: the declared type of the output
- the **range** `f(A) = { f(a) : a ∈ A }`: the values actually produced

The range is a subset of the codomain and is often a proper subset. `f(x) = x²`
from ℝ to ℝ has codomain ℝ, but its range is only `[0, ∞)`. Declaring the
codomain as ℝ is not wrong - it is a statement about the type, not a promise
that every real is hit.

In ML this distinction is load-bearing: a softmax has codomain `[0,1]ⁿ`, but its
range is the *simplex* - vectors that also sum to 1. Code that treats any vector
in `[0,1]ⁿ` as a valid softmax output is assuming the codomain when it needs the
range.

## 2. Worked example

`A = {1, 2, 3}`, `B = {a, b}`.

`F = {(1,a), (2,a), (3,b)}` - is it a function?

- Total: 1, 2, 3 all appear as first components ✓
- Single-valued: each appears once ✓

So yes. Domain `{1,2,3}`, codomain `{a,b}`, range `{a, b}` - here the range
happens to be all of B.

`G = {(1,a), (1,b), (2,a)}` - not a function. 1 maps to two things, and 3 is
missing. Both conditions fail.

`H = {(1,a), (2,a), (3,a)}` - a function. Domain `{1,2,3}`, codomain `{a,b}`,
range `{a}`. Here the range is a *proper* subset of the codomain: nothing maps
to b. That is entirely legal.

## 3. Verify it in code

```python
A, B = {1, 2, 3}, {"a", "b"}

def is_function(rel, domain):
    firsts = [x for x, _ in rel]
    return set(firsts) == domain and len(firsts) == len(set(firsts))

F = {(1, "a"), (2, "a"), (3, "b")}
G = {(1, "a"), (1, "b"), (2, "a")}
H = {(1, "a"), (2, "a"), (3, "a")}

assert is_function(F, A)
assert not is_function(G, A), "1 has two outputs and 3 has none"
assert is_function(H, A)

# domain, codomain, range
rng = {y for _, y in H}
assert rng == {"a"}
assert rng < B, "the range can be a proper subset of the codomain"

rng_F = {y for _, y in F}
assert rng_F == B, "and sometimes it is all of it"

# A Python dict is exactly a finite function: keys are the domain.
f = {1: "a", 2: "a", 3: "b"}
assert set(f) == A
assert set(f.values()) == B
assert len(f) == len(A), "one output per input, enforced by the dict itself"
```

## 4. The mistake people actually make

**Confusing the codomain with the range when validating model output.**

A classifier's scores are declared to live in `[0,1]ⁿ` - that is the codomain.
Their actual range is the probability simplex: non-negative *and summing to 1*.

Code that validates only `0 <= p <= 1` accepts a vector like `[0.9, 0.9]`, which
is in the codomain and is not a probability distribution. It typically arises
from applying a sigmoid per class where a softmax was intended - a real and
common bug, and one that produces confident-looking, entirely meaningless
confidences.

The check that catches it is the range condition, not the codomain condition:
assert the sum is 1 (to a tolerance), not merely that each entry is in `[0,1]`.

The same pattern recurs whenever a type is weaker than the invariant: declaring
a value `float` does not make it a probability, and declaring a matrix
`ndarray` does not make it a valid covariance.

---

## Check yourself

1. Is `{(1,a), (2,b)}` a function from `{1,2,3}` to `{a,b}`?
2. Give a function whose range is a proper subset of its codomain.
3. Why is checking `0 <= p[i] <= 1` for every i insufficient to validate a softmax output?

<details>
<summary>Answers</summary>

1. No. It is single-valued but not total - 3 has no output. It is a function from `{1,2}`, but not from `{1,2,3}`.
2. `f : ℝ → ℝ`, `f(x) = x²`. The codomain is ℝ but the range is `[0, ∞)`; no negative number is ever produced.
3. Because that only checks membership of the codomain. A softmax output must additionally sum to 1, which is the range condition. `[0.9, 0.9]` passes the first check and is not a distribution.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](10_Equivalence_Relations_and_Partitions.md) · [Module README](../README.md) · [Next →](12_Injective_Surjective_and_Bijective_Maps.md)
