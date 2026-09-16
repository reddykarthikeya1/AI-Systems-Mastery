from __future__ import annotations

import dataclasses
import numpy as np


@dataclasses.dataclass
class SLAReport:
    p50_ms: float
    p90_ms: float
    p99_ms: float
    mean_ms: float
    sla_passed: bool
    recommended_replicas: int


class ServingBenchmarkAnalyzer:
    """Analyzes latency distributions, SLA compliance, and capacity planning."""

    @staticmethod
    def evaluate_latencies(
        latencies_ms: list[float],
        sla_p99_threshold_ms: float = 500.0,
        arrival_rate_qps: float = 50.0,
        node_concurrency_capacity: int = 64,
    ) -> SLAReport:
        if not latencies_ms:
            raise ValueError("latencies_ms cannot be empty")

        sorted_lats = sorted(latencies_ms)

        p50 = float(np.percentile(sorted_lats, 50, method="nearest"))
        p90 = float(np.percentile(sorted_lats, 90, method="nearest"))
        p99 = float(np.percentile(sorted_lats, 99, method="nearest"))
        mean = float(np.mean(sorted_lats))

        sla_pass = p99 <= sla_p99_threshold_ms

        # Little's Law: L = lambda * W
        mean_residence_sec = mean / 1000.0
        total_concurrent_load = arrival_rate_qps * mean_residence_sec
        needed_replicas = max(1, int(np.ceil(total_concurrent_load / node_concurrency_capacity)))

        return SLAReport(
            p50_ms=round(p50, 2),
            p90_ms=round(p90, 2),
            p99_ms=round(p99, 2),
            mean_ms=round(mean, 2),
            sla_passed=sla_pass,
            recommended_replicas=needed_replicas,
        )
