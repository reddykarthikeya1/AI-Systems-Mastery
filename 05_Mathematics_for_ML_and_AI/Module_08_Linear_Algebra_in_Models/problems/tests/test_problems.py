"""Tests for Ridge Regression Closed Form."""
from __future__ import annotations

import pytest
from p01_ridge_regression_closed_form import ridge_regression_closed_form


def test_ridge_regression_closed_form():
    X = [1.0, 2.0, 3.0]
    y = [2.0, 4.0, 6.0]
    w = ridge_regression_closed_form(X, y, lmbda=0.0)
    assert abs(w - 2.0) < 1e-3
    w_reg = ridge_regression_closed_form(X, y, lmbda=5.0)
    assert w_reg < 2.0  # shrunk by regularization
