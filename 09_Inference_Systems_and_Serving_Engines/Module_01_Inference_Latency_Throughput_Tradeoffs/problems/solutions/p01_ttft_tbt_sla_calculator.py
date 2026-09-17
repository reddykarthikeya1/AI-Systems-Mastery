"""Reference Solution — Problem 01: Ttft Tbt Sla Calculator

Topic: 01 Inference Latency Throughput Tradeoffs
"""

from __future__ import annotations


def ttft_tbt_sla_calculator(ttft_ms: list[float], tbt_ms: list[float]) -> dict[str, float]:
    def pctl(arr: list[float], q: float) -> float:
        if not arr:
            return 0.0
        s = sorted(arr)
        idx = max(0, min(len(s) - 1, int(q * len(s))))
        return s[idx]
    return {
        'p50_ttft': round(pctl(ttft_ms, 0.5), 2),
        'p99_ttft': round(pctl(ttft_ms, 0.99), 2),
        'p50_tbt': round(pctl(tbt_ms, 0.5), 2),
        'p99_tbt': round(pctl(tbt_ms, 0.99), 2)
    }
