# Debug Lab 08 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - none

This section only prints the input. It is here so you notice the column means
are around 10 and 20 rather than 0, which is the fact the next defect turns on.

---

## Defect 2 - covariance computed without centring

**Where:** `covariance`.

```python
out[i][j] = sum(row[i] * row[j] for row in x) / (n - 1)
```

This is the second moment about the **origin**, not about the mean. The
definition is:

    cov(i, j) = sum((x_i - mean_i) * (x_j - mean_j)) / (n - 1)

Without subtracting the means you get roughly `mean_i * mean_j * n / (n-1)`,
which is why the off-diagonal came out near 200 - it is measuring where the
data *is*, not how it *varies*.

For PCA this is fatal and silent. The leading eigenvector of the uncentred
matrix points at the data's centre of mass rather than its direction of
greatest variance, so "the first principal component" is just the mean
direction. On data far from the origin it looks like a strong, clean result.

**The fix.**

```python
means = column_means(x)
out[i][j] = sum((row[i] - means[i]) * (row[j] - means[j]) for row in x) / (n - 1)
```

Note the divisor is already correct: `n - 1`, not `n`. That is Bessel's
correction, and it is there because the means were estimated from the same
data.

**The general lesson.** PCA is defined on centred data. Every library centres
for you, which is exactly why hand-rolling it is where this bug appears. If
your first principal component always points roughly at the mean, this is why.

---

## Defect 3 - the normal equation on collinear features

**Where:** `fit_normal_equation` together with `solve_2x2`.

Nothing here is misimplemented. The normal equation is correct and the fit is
genuinely excellent. The problem is that it should not be used this way.

When two columns are nearly proportional, `X^T X` is nearly singular: its
determinant is close to zero, and solving divides by it. The coefficients blow
up, they split the shared signal between the two features almost arbitrarily,
and a perturbation of 0.001 in one entry moves them substantially. The fit
stays perfect throughout, so no fit metric will warn you.

`solve_2x2` also returns `[0.0, 0.0]` when the determinant is *exactly* zero -
silently reporting a fitted model of all zeros rather than refusing.

**The fix.** Add ridge regularisation:

```python
lam = 1e-6
for i in range(len(xtx)):
    xtx[i][i] += lam
```

That makes the matrix invertible, bounds the coefficients, and costs a tiny
amount of bias. In practice, solve least squares with `numpy.linalg.lstsq`,
which uses an SVD and handles rank deficiency properly, rather than forming
`X^T X` at all - squaring the matrix squares its condition number.

**The general lesson.** "The model fits well" and "the coefficients mean
something" are different claims. Collinear features make the first true and
the second false, and only the second is what anyone wanted when they asked
which feature matters.
