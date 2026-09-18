"""Problem 01 — Concurrency Queue Autoscaler

Topic: 09 Production Benchmarking and Autoscaling
Target: Production-grade implementation

Compute desired replica count from queue length and target concurrency per replica.

Example:
    >>> concurrency_queue_autoscaler(20, 10, target_concurrency_per_pod=10, min_pods=1, max_pods=5)
    3

Hints:
    Hint 1: The raw signal is total outstanding work — queued plus in-flight
        requests together — measured against how much one pod is meant to
        carry; everything else is just turning that ratio into a whole
        number of pods within bounds.
    Hint 2: Divide total requests by `target_concurrency_per_pod` and round
        UP with `math.ceil` (partial load still needs a whole extra pod),
        then clamp the result between `min_pods` and `max_pods`.
    Hint 3: A `target_concurrency_per_pod` of zero or negative would divide
        by zero — guard it and fall back to `min_pods` in that case — and
        the clamp must apply after computing the ceiling, since heavy load
        (e.g. 500+500 requests at target 10) should saturate at `max_pods`
        rather than scale past it.
"""

from __future__ import annotations


def concurrency_queue_autoscaler(queued_requests: int, in_flight_requests: int, target_concurrency_per_pod: int, min_pods: int = 1, max_pods: int = 10) -> int:
    """Desired pods = ceil((queued_requests + in_flight_requests) / target_concurrency_per_pod).
    Clamp between min_pods and max_pods.
    """
    raise NotImplementedError("Implement concurrency_queue_autoscaler")
