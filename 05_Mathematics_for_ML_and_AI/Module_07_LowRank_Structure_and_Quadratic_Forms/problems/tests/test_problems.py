"""Tests for Truncated Svd Reconstruction."""
from __future__ import annotations

import pytest
from p01_truncated_svd_reconstruction import truncated_svd_reconstruction


def test_truncated_svd_reconstruction():
    rec = truncated_svd_reconstruction(10.0, [1.0, 0.5], [1.0, 2.0])
    assert rec == [[10.0, 20.0], [5.0, 10.0]]
