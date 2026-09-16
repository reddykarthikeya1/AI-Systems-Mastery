# Debug Lab 08 - Symptoms

> A PCA and least-squares pipeline. Both fit without complaint and both are subtly wrong.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_pca_regression.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The data is as described

```
    rows: 5
    column means: [10.0, 20.08]
    the two columns are near-perfectly correlated (col2 ~ 2 x col1)
```

Two columns, means around 10 and 20, strongly correlated. Nothing to diagnose here - it is the input.

**Ask yourself:** note those means. They are far from zero. Does anything downstream assume otherwise?

---

## Section 2 - The covariance matrix entries are enormous

```
    [125.025, 251.055]
    [251.055, 504.13]
    off-diagonal (should be a small covariance): 251.0550
```

A covariance measures how two variables vary *around their means*. These values are spread over a range of less than one unit, so the covariance should be a small fraction. The reported off-diagonal is around 250.

That number is not a covariance - it is close to the product of the two means.

**Ask yourself:** read the `covariance` function and find the step that is missing. What must be subtracted before multiplying?

---

## Section 3 - The regression fits perfectly and the coefficients are absurd

```
    fitted coefficients: [1.0, 0.0]
    predictions: [1.0, 2.0, 3.0, 4.0]
    targets    : [1.0, 2.0, 3.0, 4.0]
```

The predictions match the targets to four decimal places, so by any fit metric this model is excellent. Now look at the coefficients.

Column 2 is almost exactly twice column 1, so the two features carry the same information and the split between them is nearly arbitrary. A tiny change in the data moves these numbers a long way.

**Ask yourself:** what is the determinant of `X^T X` for near-collinear columns, and what does dividing by it do? What would you add to the diagonal to stop it?

---
