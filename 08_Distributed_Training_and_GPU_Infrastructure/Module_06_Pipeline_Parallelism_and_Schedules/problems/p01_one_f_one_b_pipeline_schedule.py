"""Problem 01 — One F One B Pipeline Schedule

Topic: 06 Pipeline Parallelism and Schedules
Target: Production-grade implementation

Generate 1F1B micro-batch schedule for pipeline stages.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def one_f_one_b_pipeline_schedule(num_stages: int, num_microbatches: int) -> dict[str, int]:
    """Compute pipeline bubble fraction:
    bubble_fraction = (num_stages - 1) / (num_microbatches + num_stages - 1).
    Returns dict with 'warmup_steps', 'bubble_fraction_pct'.
    """
    raise NotImplementedError("Implement one_f_one_b_pipeline_schedule")
