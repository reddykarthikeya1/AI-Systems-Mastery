"""Starter template for Bayesian reasoning and Naive Bayes."""
from __future__ import annotations

import numpy as np


class BayesianUpdater:
    """Bayesian posterior calculator and discrete belief filter."""

    @staticmethod
    def posterior_probability(
        prior: float, sensitivity: float, false_positive_rate: float
    ) -> float:
        """Compute P(Disease | Positive) using Bayes' Theorem."""
        raise NotImplementedError

    @staticmethod
    def bayes_filter_update(prior_beliefs: np.ndarray, likelihoods: np.ndarray) -> np.ndarray:
        """Update discrete prior probabilities with likelihoods and normalize."""
        raise NotImplementedError


class GaussianNaiveBayes:
    """Gaussian Naive Bayes classifier from scratch."""

    def __init__(self, eps: float = 1e-9):
        self.eps = eps
        self.classes_: np.ndarray | None = None
        self.class_priors_: np.ndarray | None = None
        self.means_: np.ndarray | None = None
        self.variances_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> GaussianNaiveBayes:
        """Estimate prior, mean, and variance for each class."""
        raise NotImplementedError

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        """Compute unnormalized log posterior for each class."""
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class with highest log posterior probability."""
        raise NotImplementedError
