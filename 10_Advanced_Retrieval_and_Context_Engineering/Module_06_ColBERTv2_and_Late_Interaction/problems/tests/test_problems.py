"""Tests for Maxsim Late Interaction."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_maxsim_late_interaction import maxsim_late_interaction
except ImportError:
    from p01_maxsim_late_interaction import maxsim_late_interaction


def test_maxsim_late_interaction():
    q = [[1.0, 0.0], [0.0, 1.0]]
    d = [[1.0, 0.0], [0.5, 0.5]]
    # q0 matches d0: dot=1.0. q1 matches d1: dot=0.5. Total = 1.5
    assert maxsim_late_interaction(q, d) == 1.5
