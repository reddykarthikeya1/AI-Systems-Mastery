from __future__ import annotations

from serving_benchmarker import ServingBenchmarkAnalyzer


def test_sla_percentile_analysis():
    # 100 sample latencies (top 2% are 600ms)
    latencies = [100.0] * 90 + [200.0] * 8 + [600.0] * 2
    res = ServingBenchmarkAnalyzer.evaluate_latencies(
        latencies_ms=latencies,
        sla_p99_threshold_ms=500.0,
        arrival_rate_qps=20.0,
        node_concurrency_capacity=32,
    )

    assert res.p50_ms == 100.0
    assert res.p99_ms == 600.0
    # Fails SLA since 600 > 500
    assert res.sla_passed is False


def test_littles_law_replica_sizing():
    # Mean latency 2000ms (2s), 100 QPS -> 200 concurrent requests
    latencies = [2000.0] * 50
    res = ServingBenchmarkAnalyzer.evaluate_latencies(
        latencies_ms=latencies,
        arrival_rate_qps=100.0,
        node_concurrency_capacity=50,
    )
    # 200 / 50 = 4 replicas
    assert res.recommended_replicas == 4
