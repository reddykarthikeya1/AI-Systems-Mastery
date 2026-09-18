"""Tests for Tma Asynchronous Transfer Schedule."""
from __future__ import annotations

import pytest
from p01_tma_asynchronous_transfer_schedule import tma_asynchronous_transfer_schedule


def test_tma_asynchronous_transfer_schedule():
    sched = tma_asynchronous_transfer_schedule(2)
    assert sched == [
        ('LOAD', 0, 0),
        ('LOAD', 1, 1),
        ('COMPUTE', 0, 0),
        ('COMPUTE', 1, 1)
    ]
