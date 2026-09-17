"""Pytest suite for Vector Spaces Bases and Rank problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if str(SOL_DIR) not in sys.path:
    sys.path.insert(0, str(SOL_DIR))

from p01_compute_matrix_metric import compute_matrix_metric


def test_compute_matrix_metric():
    res = compute_matrix_metric([[1.0, 2.0], [3.0, 4.0]])
    assert res["trace"] == 5.0
    assert abs(res["frobenius_norm"] - 5.4772) < 1e-3
    assert compute_matrix_metric([]) == {"trace": 0.0, "frobenius_norm": 0.0}

