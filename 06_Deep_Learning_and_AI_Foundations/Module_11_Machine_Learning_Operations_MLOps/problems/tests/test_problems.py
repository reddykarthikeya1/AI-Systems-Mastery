"""Tests for Model Artifact Drift Detector."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_model_artifact_drift_detector import model_artifact_drift_detector
except ImportError:
    from p01_model_artifact_drift_detector import model_artifact_drift_detector


def test_model_artifact_drift_detector():
    # Identical distributions -> PSI near 0
    assert model_artifact_drift_detector([50, 50], [50, 50]) == 0.0
    drift = model_artifact_drift_detector([80, 20], [20, 80])
    assert drift > 0.25  # substantial drift
