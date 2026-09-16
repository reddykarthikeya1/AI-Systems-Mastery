# Debug Lab 06 - Symptoms

> A Gram-Schmidt orthogonalizer used to build an orthonormal basis. The vectors it returns are not quite orthogonal.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_orthogonalization.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The easy case is clean

```
    vectors in: 3, basis out: 3
    worst |dot| between distinct basis vectors: 0.00e+00
    norms: [1.0, 1.0, 1.0]
```

Three well-separated vectors give a basis whose vectors are orthogonal to machine precision and have unit norm. Nothing to fix here.

**Ask yourself:** this is the case every textbook example uses. What does it fail to exercise?

---

## Section 2 - Nearly parallel vectors produce a basis that is not orthogonal

```
    vectors in: 3, basis out: 3
    worst |dot| between distinct basis vectors: 7.07e-01
```

Three vectors that are almost the same direction go in; what comes out has a dot product between distinct basis vectors many orders of magnitude larger than the previous section.

In exact arithmetic the result would be perfectly orthogonal. This is rounding, and the *order of the operations* is what decides how much of it accumulates.

**Ask yourself:** look at what `project` is given. Each subtraction projects the ORIGINAL vector onto a basis vector. By the time you reach the third basis vector, is the original still the right thing to project?

---

## Section 3 - A dependent vector is silently dropped

```
    vectors in: 3 (rank is 2)
    basis out: 2
    worst |dot|: 0.00e+00
```

Three vectors go in, the rank is 2, and two come out - which is arguably correct. But look at how it happened: the guard is `if length > 0`.

**Ask yourself:** after subtracting the projections of a dependent vector, is the remainder exactly zero in floating point? What does this code do if the remainder is 1e-17 instead - and what is the norm of the vector it then appends?

---
