#!/usr/bin/env python3
"""Module 17: Prometheus Metrics Exposition Demonstration.

This script demonstrates formatting runtime telemetry into Prometheus metrics.
"""

from __future__ import annotations

from collections import defaultdict


class PrometheusCollector:
    def __init__(self) -> None:
        self.counters: dict[str, float] = defaultdict(float)
        self.latencies: dict[str, list[float]] = defaultdict(list)

    def inc_counter(self, metric: str, value: float = 1.0) -> None:
        self.counters[metric] += value

    def observe_latency(self, metric: str, duration_sec: float) -> None:
        self.latencies[metric].append(duration_sec)

    def generate_metrics_text(self) -> str:
        lines = []
        for metric, val in self.counters.items():
            lines.append(f"# TYPE {metric} counter\n{metric} {val}")
        for metric, vals in self.latencies.items():
            count = len(vals)
            total = sum(vals)
            lines.append(f"# TYPE {metric} summary\n{metric}_count {count}\n{metric}_sum {total:.4f}")
        return "\n".join(lines) + "\n"


def main() -> None:
    print("=" * 60)
    print("  Prometheus Metrics Collector Demonstration")
    print("=" * 60)

    collector = PrometheusCollector()
    collector.inc_counter('http_requests_total{handler="catalog",status="200"}', 10)
    collector.inc_counter('http_requests_total{handler="checkout",status="500"}', 2)
    collector.observe_latency('http_request_duration_seconds{handler="catalog"}', 0.024)
    collector.observe_latency('http_request_duration_seconds{handler="catalog"}', 0.031)

    print(collector.generate_metrics_text())


if __name__ == "__main__":
    main()
