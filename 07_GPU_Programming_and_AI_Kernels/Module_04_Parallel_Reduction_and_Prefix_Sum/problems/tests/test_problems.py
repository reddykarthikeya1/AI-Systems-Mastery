"""Tests for Blelloch Prefix Scan."""
from __future__ import annotations

import pytest
from p01_blelloch_prefix_scan import blelloch_prefix_scan


def test_blelloch_prefix_scan():
    assert blelloch_prefix_scan([3, 1, 7, 0, 4, 1, 6, 3]) == [0, 3, 4, 11, 11, 15, 16, 22]
    assert blelloch_prefix_scan([]) == []
