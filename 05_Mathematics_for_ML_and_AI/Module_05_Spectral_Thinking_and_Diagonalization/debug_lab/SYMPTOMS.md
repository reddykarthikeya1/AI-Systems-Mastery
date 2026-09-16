# Debug Lab 05 - Symptoms

> A power-iteration eigenvalue finder, of the kind PageRank uses. It converges, and not always to the right thing.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_power_iteration.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The eigenvalue is right but look at the raw vector

```
    raw vector after 60 iterations: ['4.239e+28', '4.239e+28']
    normalised: [0.707107, 0.707107]
    eigenvalue estimate: 3.000000   (true value 3.0)
```

The normalised vector and the eigenvalue are both correct. Now read the first line: the raw components are astronomically large.

**Ask yourself:** the loop multiplies by the matrix 60 times and never does anything else. What is the magnitude of the result after n steps, and what is it for a matrix with a dominant eigenvalue of 3?

---

## Section 2 - More iterations make it worse, not better

```
    after 200 iterations, first component = 2.656140e+95
    after 400 iterations, first component = 7.055079e+190
    after 700 iterations, first component = inf
```

Normally more iterations means more accuracy. Here the numbers grow until they stop being numbers.

**Ask yourself:** what does Python print when a float exceeds about 1.8e308, and what happens to every subsequent arithmetic operation on it? Would you notice, given that nothing raises?

---

## Section 3 - A vector that is converging is reported as not converged

```
    v        = [1.0, -1.0]
    A @ v    = [-1.0, 1.0]   (same direction, opposite sign)
    converged(v, A@v) reports: False
```

`A @ v` is exactly `-v` here: the same direction, flipped. As an *eigenvector* that is the same answer - eigenvectors are only defined up to a scalar - but the convergence test compares component by component and sees a huge difference.

**Ask yourself:** what is the right way to ask 'are these two vectors the same direction'?

---
