"""Tests for Judge Position Bias Debias."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_judge_position_bias_debias import judge_position_bias_debias
except ImportError:
    from p01_judge_position_bias_debias import judge_position_bias_debias


def test_judge_position_bias_debias():
    # Model A gets 9 when first, but 7 when second (position bias favoring first)
    # Model B gets 6 when second, but 8 when first
    deb_a, deb_b = judge_position_bias_debias((9.0, 6.0), (8.0, 7.0))
    assert deb_a == 8.0
    assert deb_b == 7.0
