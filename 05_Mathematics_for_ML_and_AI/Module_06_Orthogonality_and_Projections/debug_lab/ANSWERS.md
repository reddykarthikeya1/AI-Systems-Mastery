# Debug Lab 06 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - there is none here

Well-separated vectors orthogonalize cleanly. Worth confirming: it tells you
the algebra is right and isolates the remaining faults to the numerics.

What this case does not exercise is *cancellation*. Every vector here is far
from the span of the others, so the subtractions never remove most of the
vector's magnitude. The next section is the one that does.

---

## Defect 2 - classical Gram-Schmidt instead of modified

**Where:** `classical_gram_schmidt`, the inner loop.

```python
for b in basis:
    w = subtract(w, project(v, b))      # projects v, the ORIGINAL vector
```

Each subtraction projects the original `v`. In exact arithmetic that is fine -
the projections are independent. In floating point it is not: `w` has already
been corrected for earlier basis vectors, and those corrections carried
rounding error. Projecting `v` again re-introduces components that were
supposed to have been removed, and the errors compound.

**The fix** is one character - project the running remainder instead:

```python
for b in basis:
    w = subtract(w, project(w, b))      # project w, the running remainder
```

That is **modified Gram-Schmidt**. Same operations, same cost, same answer in
exact arithmetic - and dramatically better orthogonality in floating point,
because each projection is computed from a vector that already reflects every
earlier correction.

**The general lesson.** Two algebraically identical expressions can have
completely different numerical behaviour. Rearranging arithmetic to keep
intermediate quantities small is not micro-optimisation; it is the difference
between a basis you can use and one you cannot. For serious work, use a
Householder QR (`numpy.linalg.qr`), which is stabler than either.

---

## Defect 3 - a zero-length remainder tested with `> 0`

**Where:** the guard `if length > 0`.

When an input vector lies in the span of the ones before it, the remainder
after subtracting the projections should be the zero vector. In floating point
it is a vector of magnitude around 1e-16 - pointing in an essentially random
direction, made entirely of rounding error.

`length > 0` is true for 1e-16. The code then divides by it, producing a unit
vector out of pure noise and appending it to the basis. Here the dependent
vector happened to cancel to exactly zero, so the count came out right - which
is luck, not correctness. Change `[2.0, 0.0]` to `[2.0, 1e-17]` and a third
"basis vector" appears.

**The fix.** Compare against a tolerance relative to the input:

```python
if length > 1e-10 * norm(v):
    basis.append(scale(w, 1.0 / length))
```

**The general lesson.** Rank decisions are tolerance decisions. "Is this vector
in the span of those?" has no exact answer in floating point, only an answer
relative to a threshold - which is exactly what SVD-based rank (counting
singular values above a tolerance) makes explicit, and why it is the reliable
way to ask the question.
