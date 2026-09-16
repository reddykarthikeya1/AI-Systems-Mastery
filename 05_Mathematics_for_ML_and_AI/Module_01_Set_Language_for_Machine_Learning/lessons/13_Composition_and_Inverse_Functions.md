# Lesson 01.13 — Composition and Inverse Functions

> **Module 01:** Set Language for Machine Learning · Lesson 13 of 25

---

## What you will be able to do after this lesson

- [ ] Compose two functions in the correct order and identify when composition is defined.
- [ ] Verify an inverse using both composition identities rather than one.

## Prerequisites

- [Lesson 01.12](12_Injective_Surjective_and_Bijective_Maps.md) - bijections and invertibility.

---

## 1. The idea

Given `f : A → B` and `g : B → C`, the **composition** `g ∘ f : A → C` is
defined by

    (g ∘ f)(x) = g(f(x))

**Read it right to left.** `g ∘ f` applies f first. The notation puts g on the
left because that is where it sits in `g(f(x))`, and it is the single most
common source of order errors.

Composition is defined only when the codomain of f matches the domain of g -
the output of the first must be acceptable input to the second. That is the same
condition as matrix dimensions lining up, and it is not a coincidence: matrix
multiplication *is* composition of linear maps, which Module 03 makes explicit.

Composition is **associative** - `(h ∘ g) ∘ f = h ∘ (g ∘ f)` - and not
**commutative**: `g ∘ f` and `f ∘ g` are usually different functions, and often
only one of them is even defined.

The **identity** `id(x) = x` is the neutral element, and it gives the precise
definition of an inverse:

    f⁻¹ ∘ f = id_A   and   f ∘ f⁻¹ = id_B

Both are required. A function can have a one-sided inverse without being
invertible.

## 2. Worked example

`f(x) = x + 1` and `g(x) = 2x`, both on the integers.

    (g ∘ f)(3) = g(f(3)) = g(4) = 8
    (f ∘ g)(3) = f(g(3)) = f(6) = 7

Different answers, so composition does not commute. Writing them out:

    (g ∘ f)(x) = 2(x + 1) = 2x + 2
    (f ∘ g)(x) = 2x + 1

Now an inverse. `f(x) = x + 1` has `f⁻¹(x) = x - 1`. Check both directions:

    f⁻¹(f(x)) = (x + 1) - 1 = x ✓
    f(f⁻¹(x)) = (x - 1) + 1 = x ✓

Both hold, so `f⁻¹` is a genuine two-sided inverse.

A one-sided case: let `s : ℕ → ℕ` be `s(n) = n + 1` and `p : ℕ → ℕ` be
`p(n) = max(n - 1, 0)`. Then `p(s(n)) = n` for every n ✓, but
`s(p(0)) = s(0) = 1 ≠ 0`. So p is a left inverse of s and not a right inverse -
because s is not surjective onto ℕ, as nothing maps to 0.

## 3. Verify it in code

```python
def compose(g, f):
    return lambda x: g(f(x))

f = lambda x: x + 1
g = lambda x: 2 * x

gf = compose(g, f)      # f first, then g
fg = compose(f, g)      # g first, then f

assert gf(3) == 8
assert fg(3) == 7
assert gf(3) != fg(3), "composition does not commute"
assert all(gf(x) == 2 * x + 2 for x in range(-5, 6))
assert all(fg(x) == 2 * x + 1 for x in range(-5, 6))

# Associativity.
h = lambda x: x * x
left = compose(compose(h, g), f)
right = compose(h, compose(g, f))
assert all(left(x) == right(x) for x in range(-5, 6))

# A two-sided inverse satisfies BOTH identities.
f_inv = lambda x: x - 1
assert all(f_inv(f(x)) == x for x in range(-5, 6))
assert all(f(f_inv(x)) == x for x in range(-5, 6))

# One-sided only: successor and truncated predecessor on the naturals.
s = lambda n: n + 1
p = lambda n: max(n - 1, 0)
assert all(p(s(n)) == n for n in range(10)), "p is a LEFT inverse of s"
assert s(p(0)) == 1 != 0, "but not a right inverse: s never produces 0"
```

## 4. The mistake people actually make

**Applying a preprocessing pipeline's inverse in the same order as the forward pass.**

A pipeline scales, then applies PCA, then predicts. To map a prediction back to
original units you must undo them in **reverse** order: inverse-PCA first, then
inverse-scale. Undoing in the forward order gives numbers that are the right
shape, the right sign and completely wrong.

The rule is

    (g ∘ f)⁻¹ = f⁻¹ ∘ g⁻¹

- note the order reverses. The everyday version: you put on socks then shoes,
and you take off shoes then socks.

Nothing raises, because both inverses accept a vector of the right length. The
symptom is a reconstruction error that is large but not absurd, which gets
attributed to the model rather than to the order.

The check: reconstruct a known input through forward-then-inverse and assert
you get it back. One assertion, and it catches every ordering mistake in the
chain.

---

## Check yourself

1. `f(x) = 3x`, `g(x) = x - 2`. Compute `(g ∘ f)(4)` and `(f ∘ g)(4)`.
2. Why is `f⁻¹ ∘ f = id` alone insufficient to call `f⁻¹` an inverse?
3. A pipeline does scale then PCA. What is the correct order to invert, and what is the general rule?

<details>
<summary>Answers</summary>

1. `(g ∘ f)(4) = g(12) = 10`. `(f ∘ g)(4) = f(2) = 6`.
2. It only shows `f⁻¹` is a left inverse, which requires f to be injective. Being a two-sided inverse also requires `f ∘ f⁻¹ = id`, which needs f to be surjective. The successor/predecessor pair on ℕ satisfies the first and not the second.
3. Inverse-PCA first, then inverse-scale. The rule is `(g ∘ f)⁻¹ = f⁻¹ ∘ g⁻¹`: the inverse of a composition reverses the order.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](12_Injective_Surjective_and_Bijective_Maps.md) · [Module README](../README.md) · [Next →](14_Images_and_Preimages.md)
