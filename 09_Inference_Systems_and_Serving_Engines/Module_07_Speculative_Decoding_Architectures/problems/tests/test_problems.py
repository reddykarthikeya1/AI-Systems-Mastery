"""Tests for Speculative Rejection Sampler."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_speculative_rejection_sampler import speculative_rejection_sampler
except ImportError:
    from p01_speculative_rejection_sampler import speculative_rejection_sampler


def test_speculative_rejection_sampler():
    # draft=0.8, target=0.9 -> ratio 1.0 (draw 0.5 <= 1.0 -> accept)
    # draft=0.8, target=0.4 -> ratio 0.5 (draw 0.6 > 0.5 -> reject)
    dp = [0.8, 0.8]
    tp = [0.9, 0.4]
    r = [0.5, 0.6]
    assert speculative_rejection_sampler(dp, tp, r) == 1
