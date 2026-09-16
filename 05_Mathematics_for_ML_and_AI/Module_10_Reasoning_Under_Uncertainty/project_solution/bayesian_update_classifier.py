"""Production solution for Bayesian reasoning and Naive Bayes."""
from __future__ import annotations

import numpy as np


class BayesianUpdater:
    """Bayesian posterior calculator and discrete belief filter."""

    @staticmethod
    def posterior_probability(
        prior: float, sensitivity: float, false_positive_rate: float
    ) -> float:
        p_disease = float(prior)
        p_healthy = 1.0 - p_disease
        p_pos_given_disease = float(sensitivity)
        p_pos_given_healthy = float(false_positive_rate)

        # Total probability of testing positive
        p_positive = (p_pos_given_disease * p_disease) + (p_pos_given_healthy * p_healthy)
        if p_positive == 0:
            return 0.0
        return (p_pos_given_disease * p_disease) / p_positive

    @staticmethod
    def bayes_filter_update(prior_beliefs: np.ndarray, likelihoods: np.ndarray) -> np.ndarray:
        priors = np.asarray(prior_beliefs, dtype=float)
        likes = np.asarray(likelihoods, dtype=float)
        unnormalized = priors * likes
        total = np.sum(unnormalized)
        if total == 0:
            return np.ones_like(priors) / len(priors)
        return unnormalized / total


class GaussianNaiveBayes:
    """Gaussian Naive Bayes classifier from scratch."""

    def __init__(self, eps: float = 1e-9):
        self.eps = eps
        self.classes_: np.ndarray | None = None
        self.class_priors_: np.ndarray | None = None
        self.means_: np.ndarray | None = None
        self.variances_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> GaussianNaiveBayes:
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        _, n_features = X.shape

        self.class_priors_ = np.zeros(n_classes, dtype=float)
        self.means_ = np.zeros((n_classes, n_features), dtype=float)
        self.variances_ = np.zeros((n_classes, n_features), dtype=float)

        for idx, c in enumerate(self.classes_):
            X_c = X[y == c]
            self.class_priors_[idx] = len(X_c) / len(X)
            self.means_[idx] = np.mean(X_c, axis=0)
            self.variances_[idx] = np.var(X_c, axis=0) + self.eps

        return self

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        if self.classes_ is None or self.means_ is None or self.variances_ is None:
            raise RuntimeError("Model is not fitted.")
        X = np.asarray(X, dtype=float)
        n_samples = len(X)
        n_classes = len(self.classes_)
        log_posteriors = np.zeros((n_samples, n_classes), dtype=float)

        for idx in range(n_classes):
            mean = self.means_[idx]
            var = self.variances_[idx]
            log_prior = np.log(self.class_priors_[idx])
            # Gaussian log-likelihood sum across independent features
            log_lik = -0.5 * np.sum(np.log(2.0 * np.pi * var) + ((X - mean) ** 2) / var, axis=1)
            log_posteriors[:, idx] = log_prior + log_lik

        return log_posteriors

    def predict(self, X: np.ndarray) -> np.ndarray:
        log_prob = self.predict_log_proba(X)
        best_indices = np.argmax(log_prob, axis=1)
        return self.classes_[best_indices]
