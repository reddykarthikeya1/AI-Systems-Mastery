"""Problem 01 — One F One B Pipeline Schedule

Topic: 06 Pipeline Parallelism and Schedules
Target: Production-grade implementation

Generate 1F1B micro-batch schedule for pipeline stages.

Example:
    >>> one_f_one_b_pipeline_schedule(4, 32)
    {'warmup_steps': 3, 'bubble_fraction_pct': 9}

Hints:
    Hint 1: Every stage but the first has to wait for the stage before it
        to finish its first forward pass — that fixed startup latency is
        the source of both the warmup steps and the pipeline bubble.
    Hint 2: `warmup_steps` is simply `num_stages - 1`. The bubble fraction
        is that same `num_stages - 1` "wasted" time divided by the total
        schedule length `num_microbatches + num_stages - 1`, then expressed
        as a percentage.
    Hint 3: Guard the case where `total <= 0` (falls back to a `0.0`
        bubble fraction), and round the percentage with `round(bubble *
        100)` cast to `int` — more microbatches relative to stages shrinks
        the bubble fraction, which is why deep pipelines need large batch
        counts to stay efficient.
"""

from __future__ import annotations


def one_f_one_b_pipeline_schedule(num_stages: int, num_microbatches: int) -> dict[str, int]:
    """Compute pipeline bubble fraction:
    bubble_fraction = (num_stages - 1) / (num_microbatches + num_stages - 1).
    Returns dict with 'warmup_steps', 'bubble_fraction_pct'.
    """
    raise NotImplementedError("Implement one_f_one_b_pipeline_schedule")
