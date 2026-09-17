"""Reference Solution — Problem 01: One F One B Pipeline Schedule

Topic: 06 Pipeline Parallelism and Schedules
"""

from __future__ import annotations


def one_f_one_b_pipeline_schedule(num_stages: int, num_microbatches: int) -> dict[str, int]:
    warmup = num_stages - 1
    total = num_microbatches + num_stages - 1
    bubble = (num_stages - 1) / float(total) if total > 0 else 0.0
    return {
        'warmup_steps': warmup,
        'bubble_fraction_pct': int(round(bubble * 100))
    }
