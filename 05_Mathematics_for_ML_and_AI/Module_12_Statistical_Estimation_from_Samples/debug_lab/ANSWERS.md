# Debug Lab 12 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - none

The sample mean is the MLE for mu and it is unbiased. It is here as a contrast:
the next section shows that being a maximum-likelihood estimator does not imply
being unbiased.

---

## Defect 2 - the MLE of variance is biased, and it is used anyway

**Where:** `mle_variance`, which divides by `n`.

This is not a coding error. The maximum-likelihood estimator of a normal
variance genuinely is

    sigma^2_MLE = sum((x - xbar)^2) / n

and it genuinely is biased low, by exactly a factor of `(n-1)/n`. For n = 8
that is 0.875, which is what the measured ratio shows.

The reason: `xbar` was estimated from the same data, so the deviations are
measured from the point that minimises them. One degree of freedom has been
spent.

**The fix**, when you want an unbiased estimate:

```python
def sample_variance(values):
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)
```

**The general lesson.** MLE is consistent - the bias vanishes as n grows - but
it is not unbiased, and "maximum likelihood" is not a synonym for "correct".
Know which property you are relying on. At n = 8 the estimate is 12.5% low;
at n = 1000 nobody would notice.

---

## Defect 3 - multiplying densities before taking the log

**Where:** `log_likelihood_normal`.

```python
total = 1.0
for v in values:
    total *= density         # underflows to 0.0
return math.log(total)
```

Each density is well below 1, so the product underflows to exactly 0.0 for a
few hundred points, and `log(0)` is `-inf`. The guard returns `-inf` rather
than raising, so the caller gets a number and no explanation.

**The fix.** Sum the log densities instead of logging the product:

```python
def log_likelihood_normal(values, mu, sigma):
    n = len(values)
    return (-n * math.log(sigma * math.sqrt(2 * math.pi))
            - sum((v - mu) ** 2 for v in values) / (2 * sigma ** 2))
```

This never underflows, and it is cheaper - the exponentials cancel analytically
against the logarithm.

**The general lesson.** It is called *log* likelihood because it is computed in
logs throughout, not because you take a log at the end. The same applies to
every product of probabilities in this course: naive Bayes, HMMs, and the
cross-entropy loss of every neural network.

---

## Defect 4 - the standard deviation used where the standard error was needed

**Where:** `confidence_interval`.

```python
sd = math.sqrt(mle_variance(values))
margin = z * sd
```

`sd` measures the spread of **individual observations**. An interval for the
**mean** needs the spread of the mean, which is the **standard error**:

    se = sd / sqrt(n)

With n = 8 that is a factor of 2.83 too wide a margin - the interval is nearly
three times larger than it should be.

Two further corrections belong here:

- the variance should be the unbiased `n - 1` version (defect 2), and
- with n = 8 and the variance estimated from the data, the multiplier is not
  1.96 but a t-distribution value: about 2.36 for 7 degrees of freedom.

**The fix.**

```python
se = math.sqrt(sample_variance(values) / len(values))
margin = t_critical * se
```

**The general lesson.** "Standard deviation" and "standard error" answer
different questions - how much does one observation vary, versus how much does
this estimate vary - and the `sqrt(n)` between them is the reason more data
narrows a conclusion. Getting it wrong produces an interval that is confidently
the wrong width, in a direction nobody checks.
