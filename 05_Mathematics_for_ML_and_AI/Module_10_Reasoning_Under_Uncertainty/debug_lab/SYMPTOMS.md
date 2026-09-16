# Debug Lab 10 - Symptoms

> A Bayesian classifier that updates beliefs as evidence arrives. Every posterior it reports is a plausible probability.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_bayesian_update.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The medical test posterior equals the prior exactly

```
    disease prevalence      : 0.001
    test sensitivity P(+|D) : 0.99
    false positive P(+|not D): 0.05
    reported P(disease | positive test) = 0.0010
    (for reference, the textbook answer is about 0.0194)
```

The reported answer is 0.001 - exactly the prevalence we started with. A positive test from a 99%-sensitive instrument should move the belief a long way; the textbook answer is about 1.9%.

The evidence has had no effect at all.

**Ask yourself:** read `posterior` and simplify the arithmetic by hand. What does it actually compute, and which argument is never used?

---

## Section 2 - Every class score is exactly zero

```
    spam score: 0.0
    ham  score: 0.0
    classified as: spam
    (spam likelihoods are 2x ham's on every one of 400 features)
```

Both scores print as 0.0, so `max` picks whichever key it happens to see first, and the classification is meaningless. The spam likelihoods are twice ham's on every one of 400 features, so spam should win overwhelmingly.

**Ask yourself:** what is 0.02 multiplied by itself 400 times, and what is the smallest positive number a float can hold?

---

## Section 3 - The 'probabilities' do not sum to 1

```
    raw scores: {'a': 0.3, 'b': 0.1}
    sum of scores: 0.4
    reported as probabilities: {'a': 0.3, 'b': 0.1}
```

Two scores are reported as probabilities and they add up to 0.4.

**Ask yourself:** Bayes' rule has a denominator. What is it for, and what step is missing before these numbers may be called probabilities?

---
