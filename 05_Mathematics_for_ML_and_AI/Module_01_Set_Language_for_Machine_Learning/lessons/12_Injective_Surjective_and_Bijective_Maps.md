# Lesson 01.12 — Injective, Surjective and Bijective Maps

> **Module 01:** Set Language for Machine Learning · Lesson 12 of 25

---

## What you will be able to do after this lesson

- [ ] Classify a function as injective, surjective, bijective, or none, and justify with a witness.
- [ ] Connect invertibility to bijectivity and explain what fails when a map is not injective.

## Prerequisites

- [Lesson 01.11](11_Functions_as_Special_Relations.md) - functions, domain, codomain, range.

---

## 1. The idea

Three properties of a function `f : A → B`.

**Injective** (one-to-one): distinct inputs give distinct outputs.

    f(x) = f(y) ⟹ x = y

**Surjective** (onto): every element of the codomain is hit. Equivalently, the
range equals the codomain.

**Bijective**: both. Each element of B is hit exactly once.

The reason to care is invertibility:

> `f` has a two-sided inverse exactly when `f` is a bijection.

If f is not injective, two inputs collapse to the same output and the inverse
cannot decide which to return - information has been destroyed. If f is not
surjective, some element of B has no preimage and the inverse is undefined
there.

This is the precise statement of a fact you rely on constantly: hashing is not
injective, so it is not invertible; a lossy encoder is not injective, so the
original cannot be recovered; and a dimensionality reduction from ℝ¹⁰⁰ to ℝ²
cannot be injective, because there is not enough room in the target.

## 2. Worked example

`A = {1,2,3}`, `B = {a,b,c}` unless stated otherwise.

`f = {(1,a), (2,b), (3,c)}` - injective (three distinct outputs), surjective
(range is `{a,b,c}` = B), so bijective. Its inverse is
`{(a,1), (b,2), (c,3)}`.

`g = {(1,a), (2,a), (3,b)}` - not injective: `g(1) = g(2) = a`, and 1 ≠ 2. That
pair is the witness. Not surjective either, since c is never produced.

`h : {1,2,3} → {a,b}`, `h = {(1,a), (2,b), (3,a)}` - surjective (both a and b
are hit) but not injective (1 and 3 both give a).

A counting argument settles many cases immediately: if `|A| > |B|` no function
`A → B` can be injective, because there are more inputs than available outputs.
That is the **pigeonhole principle**, and with `|A| = 3`, `|B| = 2` it tells you
`h` cannot be injective before you look at it.

## 3. Verify it in code

```python
A, B = {1, 2, 3}, {"a", "b", "c"}

def injective(f):
    return len(set(f.values())) == len(f)

def surjective(f, codomain):
    return set(f.values()) == codomain

f = {1: "a", 2: "b", 3: "c"}
g = {1: "a", 2: "a", 3: "b"}
h = {1: "a", 2: "b", 3: "a"}

assert injective(f) and surjective(f, B)          # bijective
assert not injective(g)                           # 1 and 2 both give "a"
assert not surjective(g, B)                       # "c" is never produced
assert surjective(h, {"a", "b"}) and not injective(h)

# A bijection has a two-sided inverse.
inverse = {v: k for k, v in f.items()}
assert len(inverse) == len(f), "no outputs collided, so nothing was lost"
assert all(inverse[f[x]] == x for x in f)
assert all(f[inverse[y]] == y for y in inverse)

# Inverting a non-injective map loses inputs: two keys collapse to one.
lossy = {v: k for k, v in g.items()}
assert len(lossy) < len(g), "1 and 2 cannot both be recovered from 'a'"

# Pigeonhole: more inputs than outputs forces a collision.
assert len(A) > len({"a", "b"})
assert not injective(h)
```

## 4. The mistake people actually make

**Inverting a dict to "undo" a mapping that was never injective.**

`{v: k for k, v in mapping.items()}` is a one-line inverse, and it silently
drops entries whenever two keys share a value - the later key wins, and which
one that is depends on iteration order.

It appears constantly in label encoding. If two category names were normalised
to the same string, `name -> id` is not injective, and the `id -> name` map
built this way returns one of them arbitrarily. Predictions then decode to the
wrong label for a subset of classes, consistently, with no error.

The cost is one line: assert the inverse is the same size as the original.
`len(inverse) == len(mapping)` is exactly the injectivity check, and it fails
loudly at build time instead of quietly at inference time.

---

## Check yourself

1. `f : ℝ → ℝ`, `f(x) = x²`. Injective? Surjective? Give witnesses.
2. Can a function from a 5-element set to a 3-element set be injective? Why?
3. Why can a map from ℝ¹⁰⁰ to ℝ² never be injective, and what does that mean for dimensionality reduction?

<details>
<summary>Answers</summary>

1. Neither. Not injective: `f(2) = f(-2) = 4` with 2 ≠ -2. Not surjective: no real x gives `f(x) = -1`.
2. No. By the pigeonhole principle, five inputs must share three outputs, so at least two inputs collide.
3. There is not enough room in the target to keep all inputs distinct, so distinct high-dimensional points must collapse to the same low-dimensional point. Reduction is necessarily lossy: the original point cannot be recovered.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](11_Functions_as_Special_Relations.md) · [Module README](../README.md) · [Next →](13_Composition_and_Inverse_Functions.md)
