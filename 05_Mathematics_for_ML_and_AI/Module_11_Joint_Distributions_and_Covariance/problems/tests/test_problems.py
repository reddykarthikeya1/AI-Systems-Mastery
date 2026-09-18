"""Tests for Sample Covariance Matrix."""
from __future__ import annotations

import pytest
from p01_sample_covariance_matrix import sample_covariance_matrix


def test_sample_covariance_matrix():
    cov = sample_covariance_matrix([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
    assert cov[0][0] == 1.0
    assert cov[0][1] == 2.0
    assert cov[1][1] == 4.0
