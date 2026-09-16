# Debug Lab 12 - Symptoms

> A maximum-likelihood estimator and a confidence-interval routine used to report a parameter with error bars.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_mle_estimator.py
echo "exit=$?"
```

There are **4** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The sample mean looks reasonable

```
    n = 8
    sample mean: 5.1477   (true mu = 5.0)
```

Eight draws from N(5, 4) give a mean near 5. Nothing wrong.

**Ask yourself:** the mean is an unbiased estimator. Is every maximum-likelihood estimator unbiased?

---

## Section 2 - The variance estimate is consistently too small

```
    true variance                   : 4.0000
    average of 4000 MLE estimates   : 3.5125
    ratio estimate/true             : 0.8781
```

Averaged over 4,000 independent samples, the estimate should sit on the true value if it is unbiased. The ratio is clearly below 1, and it is not noise - 4,000 repetitions have averaged the noise away.

Look at the ratio and compare it to (n-1)/n for n = 8.

**Ask yourself:** this is the maximum-likelihood estimator, and it is biased. Is that a bug in the code or a property of MLE - and what do you do about it?

---

## Section 3 - The log likelihood becomes -inf on larger samples

```
    n=  50  log likelihood = -101.14237966531772
    n= 200  log likelihood = -441.5912743284266
    n= 800  log likelihood = -inf
```

It is a finite number for the smallest sample and `-inf` for the larger ones. The data is perfectly ordinary in every case.

**Ask yourself:** the function multiplies n densities together and takes the log at the very end. Each density is less than 1. What is the product for n = 800, and what does `math.log` return for it?

---

## Section 4 - The confidence interval is far too narrow

```
    sample mean: 5.1477
    reported 95% interval: (1.5680, 8.7274)
    interval width: 7.1594
```

The interval uses the standard deviation of the data. For a 95% interval on the *mean* of 8 observations, that is not the right quantity, and the reported width is much too small.

**Ask yourself:** how much does the sample *mean* vary from sample to sample, compared with how much a single observation varies? What is the relationship, and what else changes when n is only 8?

---
