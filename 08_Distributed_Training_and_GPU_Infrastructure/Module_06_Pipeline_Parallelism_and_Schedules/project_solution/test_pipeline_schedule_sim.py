from __future__ import annotations

import pytest
from pipeline_schedule_sim import PipelineScheduleSimulator


def test_pipeline_schedule_bubble_and_memory():
    sim = PipelineScheduleSimulator(stages=4, microbatches=16)
    metrics = sim.calculate_metrics()

    # In GPipe: (4 - 1) / (16 + 4 - 1) = 3 / 19 = 0.1579
    assert abs(metrics.bubble_fraction_gpipe - 0.1579) < 0.001
    # In 1F1B: (4 - 1) / 16 = 3 / 16 = 0.1875
    assert abs(metrics.bubble_fraction_1f1b - 0.1875) < 0.001

    # GPipe memory scales with microbatches (16), 1F1B caps at stages (4)
    assert metrics.peak_act_memory_gpipe_mb == 16
    assert metrics.peak_act_memory_1f1b_mb == 4


def test_1f1b_schedule_timeline_generation():
    sim = PipelineScheduleSimulator(stages=3, microbatches=6)
    timeline = sim.generate_1f1b_schedule_timeline()

    # Must execute exactly 6 Forwards and 6 Backwards
    forwards = [t for t in timeline if t.startswith("F")]
    backwards = [t for t in timeline if t.startswith("B")]
    assert len(forwards) == 6
    assert len(backwards) == 6


def test_pipeline_invalid_microbatches():
    with pytest.raises(ValueError, match="must be >= stages"):
        PipelineScheduleSimulator(stages=8, microbatches=4)
