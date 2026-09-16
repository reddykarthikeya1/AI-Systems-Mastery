"""Bayesian updating with three planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations


def posterior(prior, likelihood, likelihood_given_not):
    """P(H | E) from P(H), P(E|H) and P(E|not H)."""
    numerator = prior * likelihood
    return numerator / likelihood


def naive_bayes_score(priors, likelihoods):
    """Unnormalised class scores, multiplying feature likelihoods."""
    scores = {}
    for label, prior in priors.items():
        product = prior
        for p in likelihoods[label]:
            product *= p
        scores[label] = product
    return scores


def classify(scores):
    return max(scores, key=scores.get)


def main():
    print("=" * 66)
    print("BAYESIAN CLASSIFIER - belief update report")
    print("=" * 66)

    print()
    print("[1] The classic medical test")
    prevalence = 0.001
    sensitivity = 0.99
    false_positive = 0.05
    p = posterior(prevalence, sensitivity, false_positive)
    print(f"    disease prevalence      : {prevalence}")
    print(f"    test sensitivity P(+|D) : {sensitivity}")
    print(f"    false positive P(+|not D): {false_positive}")
    print(f"    reported P(disease | positive test) = {p:.4f}")
    print(f"    (for reference, the textbook answer is about 0.0194)")

    print()
    print("[2] Naive Bayes over many features")
    priors = {"spam": 0.5, "ham": 0.5}
    likelihoods = {"spam": [0.02] * 400, "ham": [0.01] * 400}
    scores = naive_bayes_score(priors, likelihoods)
    print(f"    spam score: {scores['spam']}")
    print(f"    ham  score: {scores['ham']}")
    print(f"    classified as: {classify(scores)}")
    print(f"    (spam likelihoods are 2x ham's on every one of 400 features)")

    print()
    print("[3] Do the posteriors form a distribution?")
    two = {"a": 0.3, "b": 0.1}
    print(f"    raw scores: {two}")
    print(f"    sum of scores: {sum(two.values())}")
    print(f"    reported as probabilities: {two}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
