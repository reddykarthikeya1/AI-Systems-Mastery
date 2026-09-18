"""Tests for Strict Two Phase Locking."""
from __future__ import annotations

import pytest
from p01_strict_two_phase_locking import strict_two_phase_locking


def test_strict_two_phase_locking():
    # tx1 holds R1, tx2 holds R2. tx1 requests R2 (waits for tx2). tx2 requests R1 (cycle!).
    reqs = [
        ('tx1', 'R1', 'X'),
        ('tx2', 'R2', 'X'),
        ('tx1', 'R2', 'X'),
        ('tx2', 'R1', 'X'),
    ]
    acquired, aborted = strict_two_phase_locking(reqs)
    assert 'tx2' in aborted
