"""Tests for Readiness & Liveness Consensus."""
from __future__ import annotations

import pytest
from p01_health_probe_evaluator import evaluate_cluster_health


def test_health_probe_evaluator():
    probes = [{'liveness': True, 'readiness': True}, {'liveness': True, 'readiness': False}]
    assert evaluate_cluster_health(probes, 0.5) is True
    assert evaluate_cluster_health(probes, 0.6) is False
    assert evaluate_cluster_health([], 0.5) is False
