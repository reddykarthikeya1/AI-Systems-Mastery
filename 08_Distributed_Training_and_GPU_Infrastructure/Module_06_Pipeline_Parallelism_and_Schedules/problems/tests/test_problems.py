"""Tests for One F One B Pipeline Schedule."""
from __future__ import annotations

import pytest
from p01_one_f_one_b_pipeline_schedule import one_f_one_b_pipeline_schedule


def test_one_f_one_b_pipeline_schedule():
    sched = one_f_one_b_pipeline_schedule(4, 32)
    assert sched['warmup_steps'] == 3
    assert sched['bubble_fraction_pct'] < 10
