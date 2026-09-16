# Debug Lab 03 - Symptoms

> A linear system solver. It returns an answer for every system it is given, and some of those answers are wrong.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_linear_solver.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The well-conditioned system is solved correctly

```
    solution: [2.0, 3.0, -1.0]
    expected: [2.0, 3.0, -1.0]
    residual: 0.00e+00
```

The residual is at machine precision and the answer matches. This section is working - note it and move on.

**Ask yourself:** what does a residual of this size tell you, and what does it *not* tell you?

---

## Section 2 - A tiny pivot destroys the answer

```
    solution: [0.0, 1.0]
    exact answer is approximately [1.0, 1.0]
    residual: 1.00e+00
```

The exact solution is very close to `[1, 1]`. The solver returns something else entirely, and the residual is enormous.

The only thing that changed is the size of the top-left entry. The system is not ill-conditioned - it has a perfectly good solution.

**Ask yourself:** look at how the pivot row is chosen. It takes the first row with a non-zero entry. What does dividing by 1e-18 do to every other number in that row?

---

## Section 3 - Singularity detection depends on exact zeros

```
    rows [1,2] and [2,4]              -> singular? True
    rows [1,2] and [1,2.0000000001]   -> singular? False
    solving it with b=[3, 3]           -> [3.0, 0.0]
    nudging b by 1e-9                  -> [-17.0, 10.0]
```

A genuinely singular matrix is detected. A matrix that is singular to within one part in 10^10 is reported as fine.

The solve on that matrix returns a correct answer, so it looks harmless. Then read the last line: nudging the right-hand side by 0.000000001 moves the solution from `[3, 0]` to a completely different point. The answer is exact and useless - any measurement error in `b` produces a wildly different `x`.

**Ask yourself:** `== 0` is a question about floating-point bit patterns. What question did you actually want to ask - and would it have warned you about this matrix?

---
