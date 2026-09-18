"""Problem 01 — Model Artifact Drift Detector

Topic: 11 Machine Learning Operations MLOps
Target: Production-grade implementation

Calculate Population Stability Index (PSI) between baseline and production feature bins.

Example:
    >>> model_artifact_drift_detector([80, 20], [20, 80])
    1.6636

Hints:
    Hint 1: PSI compares two histograms bin by bin, not their raw counts —
        each bin's baseline and current counts must first be turned into
        proportions of their own total before any comparison makes sense.
    Hint 2: For each bin, convert `baseline_counts[i]` and
        `current_counts[i]` to percentages of their respective totals
        (`count / total`), then accumulate `(cur_pct - base_pct) *
        ln(cur_pct / base_pct)` across all bins.
    Hint 3: A bin with zero count (or an all-zero totals list) makes
        `cur_pct` or `base_pct` exactly 0, which sends `ln(...)` to
        negative infinity — floor every percentage at `eps = 1e-6` with
        `max(pct, eps)` before taking the log or forming the ratio. Round
        the final summed PSI to 4 decimal places.
"""

from __future__ import annotations


def model_artifact_drift_detector(baseline_counts: list[int], current_counts: list[int]) -> float:
    """Compute PSI: sum((cur_pct - base_pct) * ln(cur_pct / base_pct)).
    Add epsilon 1e-6 to percentages to prevent division by zero.
    Returns PSI score rounded to 4 decimals.
    """
    raise NotImplementedError("Implement model_artifact_drift_detector")
