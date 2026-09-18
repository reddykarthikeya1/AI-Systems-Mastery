"""Tests for Bayes Posterior Update."""
from __future__ import annotations

import pytest
from p01_bayes_posterior_update import bayes_posterior_update


def test_bayes_posterior_update():
    # Medical test: prior=0.01, sensitivity=0.9, p_pos=0.05
    post = bayes_posterior_update(0.01, 0.9, 0.05)
    assert post == 0.18
