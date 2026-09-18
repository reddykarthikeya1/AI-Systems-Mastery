"""Tests for Probabilistic Early Expiration."""
from __future__ import annotations

import pytest
from p01_probabilistic_early_expiration import probabilistic_early_expiration


def test_probabilistic_early_expiration():
    # Far from expiry -> should not recompute
    assert probabilistic_early_expiration(100.0, 200.0, 5.0, 1.0, 0.5) is False
    # At or past expiry -> must recompute
    assert probabilistic_early_expiration(200.0, 200.0, 5.0, 1.0, 0.5) is True
