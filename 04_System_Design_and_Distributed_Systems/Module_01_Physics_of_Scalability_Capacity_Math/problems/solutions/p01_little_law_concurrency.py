"""Reference Solution — Problem 01: Little Law Concurrency

Topic: 01 Physics of Scalability Capacity Math
"""

from __future__ import annotations


def little_law_concurrency(arrival_rate_rps: float, avg_latency_seconds: float) -> float:
    return arrival_rate_rps * avg_latency_seconds
