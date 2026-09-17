"""Tests for Ttft Tbt Sla Calculator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_ttft_tbt_sla_calculator import ttft_tbt_sla_calculator
except ImportError:
    from p01_ttft_tbt_sla_calculator import ttft_tbt_sla_calculator


def test_ttft_tbt_sla_calculator():
    res = ttft_tbt_sla_calculator(list(range(100)), list(range(100)))
    assert res['p50_ttft'] == 50.0
    assert res['p99_ttft'] == 99.0
