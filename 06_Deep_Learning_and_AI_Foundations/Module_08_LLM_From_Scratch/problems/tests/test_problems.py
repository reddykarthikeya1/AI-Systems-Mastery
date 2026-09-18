"""Tests for Rotary Position Embedding."""
from __future__ import annotations

import pytest
from p01_rotary_position_embedding import rotary_position_embedding


def test_rotary_position_embedding():
    # At position 0, cos(0)=1, sin(0)=0 -> unchanged
    r0, r1 = rotary_position_embedding(1.0, 2.0, 0)
    assert r0 == 1.0 and r1 == 2.0
