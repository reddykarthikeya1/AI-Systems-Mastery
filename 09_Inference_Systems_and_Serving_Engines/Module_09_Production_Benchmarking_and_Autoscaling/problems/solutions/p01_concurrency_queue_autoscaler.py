"""Reference Solution — Problem 01: Concurrency Queue Autoscaler

Topic: 09 Production Benchmarking and Autoscaling
"""

from __future__ import annotations


def concurrency_queue_autoscaler(queued_requests: int, in_flight_requests: int, target_concurrency_per_pod: int, min_pods: int = 1, max_pods: int = 10) -> int:
    import math
    if target_concurrency_per_pod <= 0:
        return min_pods
    total = queued_requests + in_flight_requests
    desired = math.ceil(total / float(target_concurrency_per_pod))
    return max(min_pods, min(max_pods, desired))
