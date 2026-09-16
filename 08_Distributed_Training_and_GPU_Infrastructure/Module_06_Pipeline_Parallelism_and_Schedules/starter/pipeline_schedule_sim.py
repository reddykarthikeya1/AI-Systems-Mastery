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
    def __init__(self, stages: int, microbatches: int):
        raise NotImplementedError("Implement PipelineScheduleSimulator")

    def calculate_metrics(self) -> PipelineMetrics:
        raise NotImplementedError("Implement calculate_metrics")

    def generate_1f1b_schedule_timeline(self) -> list[str]:
        raise NotImplementedError("Implement generate_1f1b_schedule_timeline")
