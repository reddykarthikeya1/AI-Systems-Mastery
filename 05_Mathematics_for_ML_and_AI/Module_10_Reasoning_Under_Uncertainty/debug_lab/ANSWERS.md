# Debug Lab 10 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - the denominator is wrong, so the evidence cancels out

**Where:** `posterior`.

```python
numerator = prior * likelihood
return numerator / likelihood        # the likelihood cancels
```

This returns `prior * likelihood / likelihood`, which is just the prior. The
`likelihood_given_not` argument is never used at all - a strong hint, and one
a linter would have flagged.

Bayes' rule is:

    P(H|E) = P(E|H) P(H) / P(E)

and the denominator is the **total probability of the evidence**:

    P(E) = P(E|H) P(H) + P(E|not H) P(not H)

**The fix.**

```python
def posterior(prior, likelihood, likelihood_given_not):
    evidence = likelihood * prior + likelihood_given_not * (1 - prior)
    return likelihood * prior / evidence
```

Which gives 0.99 * 0.001 / (0.99 * 0.001 + 0.05 * 0.999) = 0.0194.

**The general lesson.** That 1.9% is the base-rate fallacy made concrete: a
99%-accurate test for a rare disease still leaves you far more likely healthy
than ill, because the false positives are drawn from a vastly larger pool. If
your posterior never moves, check that the denominator involves both branches.

---

## Defect 2 - underflow from multiplying hundreds of probabilities

**Where:** `naive_bayes_score`, the line `product *= p`.

0.02^400 is about 1e-680. The smallest positive double is around 5e-324, so the
product reaches exactly 0.0 long before the loop ends - for both classes. The
comparison is then between two zeros and the "classification" is whichever key
`max` encounters first.

Nothing raises. Underflow returns zero silently, which is worse than overflow's
`inf` because zero looks like a legitimate value.

**The fix.** Work in log space:

```python
import math

def naive_bayes_score(priors, likelihoods):
    return {label: math.log(prior) + sum(math.log(p) for p in likelihoods[label])
            for label, prior in priors.items()}
```

Products become sums, underflow disappears, and `max` still picks the right
class because `log` is monotonic. To recover actual probabilities, use the
log-sum-exp trick rather than exponentiating directly.

**The general lesson.** Any time you multiply many numbers smaller than 1, you
will underflow. Every real implementation of naive Bayes, every HMM, and every
language model works in logs for exactly this reason - it is not an
optimisation, it is what makes the computation possible.

---

## Defect 3 - scores presented as probabilities without normalising

**Where:** `main`, which prints the raw scores and calls them probabilities.

Unnormalised scores are fine for *deciding* - `argmax` is unaffected by a
common factor. They are not probabilities, and they must not be displayed as
confidences or fed to anything expecting a distribution.

**The fix.**

```python
total = sum(scores.values())
probabilities = {k: v / total for k, v in scores.items()}
```

**The general lesson.** Know which of the two you are holding. A number between
0 and 1 is not automatically a probability, and a "92% confident" shown to a
user from an unnormalised score is a number with no meaning at all.
