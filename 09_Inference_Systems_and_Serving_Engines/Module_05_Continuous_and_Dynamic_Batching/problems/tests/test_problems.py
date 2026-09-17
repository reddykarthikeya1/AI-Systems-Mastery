"""Tests for Iteration Level Scheduler."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_iteration_level_scheduler import iteration_level_scheduler
except ImportError:
    from p01_iteration_level_scheduler import iteration_level_scheduler


def test_iteration_level_scheduler():
    running = ['r1', 'r2']  # uses 2 tokens
    waiting = [('w1', 5), ('w2', 10)]
    new_run, rem = iteration_level_scheduler(running, waiting, max_batch_tokens=8)
    assert new_run == ['r1', 'r2', 'w1']
    assert rem == [('w2', 10)]
