# Debug Lab 11 - Symptoms

> A covariance and correlation estimator used to summarise a dataset before fitting a Gaussian.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_covariance_estimator.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The data and means are right

```
    xs = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    ys = 2 * xs
    mean(xs) = 5.0   mean(ys) = 10.0
```

`ys` is exactly twice `xs`, and the means confirm it. Nothing to fix.

**Ask yourself:** a perfectly linear relationship gives a known correlation. What is it, and will you be able to recognise a wrong answer when you see one?

---

## Section 2 - Variance and covariance use different divisors

```
    variance() returns        : 4.000000
    dividing by n     gives   : 4.000000
    dividing by n - 1 gives   : 4.571429
    covariance() divides by n - 1: 4.571429
```

`variance()` divides by n and `covariance()` divides by n - 1. Both appear in the same summary, so the diagonal and the off-diagonal of a covariance matrix built from them are on different scales.

Only one of the two is the sample estimator.

**Ask yourself:** the mean was estimated from the same data before the deviations were computed. What does that do to the sum of squared deviations, and which divisor corrects for it?

---

## Section 3 - The correlation of a perfect line is not 1

```
    ys = 2 * xs exactly, so the correlation must be 1.0
    correlation() reports: 0.142857
    is it within [-1, 1]? True
    the same relationship on a narrower spread [0.1, 0.2, 0.3, 0.4]:
    correlation() reports: 53.333333
    is it within [-1, 1]? False
```

`ys` is exactly `2 * xs`, so the correlation is 1 by definition. The first dataset reports about 0.14 - badly wrong, and still inside [-1, 1], so a range check passes and tells you nothing.

Then look at the second dataset. Same perfect relationship, narrower spread, and now the reported 'correlation' is far outside the range a correlation can occupy at all. The error was always there; only the scale of the data decides whether it is visible.

**Ask yourself:** write down the definition of the correlation coefficient. What is in the denominator - the variances, or something derived from them? Check the units, and work out why shrinking the data made the answer bigger.

---
