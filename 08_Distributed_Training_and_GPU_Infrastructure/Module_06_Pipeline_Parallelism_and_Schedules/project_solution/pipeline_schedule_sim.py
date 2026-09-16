from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class PipelineMetrics:
    stages: int
    microbatches: int
    bubble_fraction_gpipe: float
    bubble_fraction_1f1b: float
    peak_act_memory_gpipe_mb: int
    peak_act_memory_1f1b_mb: int


class PipelineScheduleSimulator:
    """Simulates and analyzes GPipe and 1F1B pipeline schedules."""

    def __init__(self, stages: int, microbatches: int):
        if stages < 1:
            raise ValueError("stages must be >= 1")
        if microbatches < stages:
            raise ValueError(f"microbatches ({microbatches}) must be >= stages ({stages}) for valid pipeline")
        self.p = stages
        self.m = microbatches

    def calculate_metrics(self) -> PipelineMetrics:
        # GPipe bubble: (p - 1) / (m + p - 1)
        bubble_gpipe = (self.p - 1) / (self.m + self.p - 1)
        # 1F1B bubble: (p - 1) / m
        bubble_1f1b = (self.p - 1) / self.m

        # GPipe stores all m microbatch activations
        peak_gpipe = self.m
        # 1F1B caps peak activation memory at p microbatches
        peak_1f1b = self.p

        return PipelineMetrics(
            stages=self.p,
            microbatches=self.m,
            bubble_fraction_gpipe=round(bubble_gpipe, 4),
            bubble_fraction_1f1b=round(bubble_1f1b, 4),
            peak_act_memory_gpipe_mb=peak_gpipe,
            peak_act_memory_1f1b_mb=peak_1f1b,
        )

    def generate_1f1b_schedule_timeline(self) -> list[str]:
        """Generates human-readable schedule trace for Stage 0."""
        timeline = []
        # Warmup: p - 1 forwards
        for mb in range(self.p - 1):
            timeline.append(f"F{mb}")
        # Steady state 1F1B
        for mb in range(self.p - 1, self.m):
            timeline.append(f"F{mb}")
            b_mb = mb - (self.p - 1)
            timeline.append(f"B{b_mb}")
        # Cooldown: remaining backwards
        for b_mb in range(self.m - (self.p - 1), self.m):
            timeline.append(f"B{b_mb}")
        return timeline
