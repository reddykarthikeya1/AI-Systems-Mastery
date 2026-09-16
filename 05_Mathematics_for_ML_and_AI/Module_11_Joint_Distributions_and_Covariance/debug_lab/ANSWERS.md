# Debug Lab 11 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - none

The input and its means are correct, and the perfectly linear relationship is
deliberate: it gives you an answer you already know, which is the cheapest way
to catch a wrong implementation.

---

## Defect 2 - population variance where the sample estimator was needed

**Where:** `variance`, which divides by `len(values)`.

When the mean is estimated from the same sample, the deviations are measured
from a point chosen to minimise them - so the sum of squared deviations is
systematically too small, and dividing by n gives a **biased** estimate of the
population variance.

Dividing by `n - 1` corrects it exactly. That is **Bessel's correction**, and
`n - 1` is the number of degrees of freedom left after spending one on the
mean.

The inconsistency is the immediate bug: a covariance matrix whose diagonal is
divided by n and whose off-diagonal is divided by n - 1 is not a covariance
matrix of anything. It can even fail to be positive semi-definite, which will
make a Gaussian fit or a Cholesky factorisation fail later, a long way from
here.

**The fix.**

```python
def variance(values):
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)
```

Whichever convention you choose, use it everywhere. NumPy makes this explicit
with `ddof`: `np.var(x, ddof=1)` for the sample estimator, `ddof=0` by default.

**The general lesson.** With n = 8 the two differ by 14%; at n = 1000 the
difference is invisible. It is a bug that shows up on small samples, which is
where variance estimates matter most.

---

## Defect 3 - dividing by the variances instead of the standard deviations

**Where:** `correlation`.

```python
return covariance(xs, ys) / (variance(xs) * variance(ys))
```

The definition is:

    corr(x, y) = cov(x, y) / (sd(x) * sd(y))

where `sd` is the square root of the variance. Dividing by the variances
divides by an extra factor of `sd(x) * sd(y)`, so the result is not
dimensionless and is not bounded by 1.

The extra factor is `sd(x) * sd(y)`, so the reported value is the true
correlation divided by the two standard deviations. That is why the second
dataset is so much worse: its spread is smaller than 1, so dividing by it makes
the result *larger*, and it sails past 1.

Note what this means for checking your work. On the first dataset the answer is
wrong and still inside [-1, 1] - a range check passes. Only the narrow-spread
case pushes it outside. A sanity check that happens to pass is not evidence;
it only ever catches the cases it catches.

**The fix.**

```python
return covariance(xs, ys) / math.sqrt(variance(xs) * variance(ys))
```

**The general lesson.** Correlation is covariance with the units divided out -
that is the entire point of it, and it is why correlation is comparable across
datasets while covariance is not. Any quantity with a guaranteed range gives
you a free assertion: check it, and the check will catch this class of error
immediately.
