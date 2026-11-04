"""Little's Law and Adaptive Concurrency Limiters.

Core Mathematical Principles:
-----------------------------
1. Little's Law:
   L = lambda * W
   where:
     L      = Average number of items/requests in the system (concurrency)
     lambda = Average arrival rate of requests (requests / unit time)
     W      = Average time a request spends in the system (latency / residence time)

2. TCP Vegas Adaptive Limiter:
   Estimates queuing delay by tracking base round-trip time (min_rtt):
     expected_throughput = limit / min_rtt
     actual_throughput   = limit / smoothed_rtt
     queue_size          = limit * (1 - min_rtt / smoothed_rtt)

   Adjustment Rules:
     - If queue_size < alpha: underutilized; limit += 1
     - If queue_size > beta:  queue building; limit = max(min_limit, limit - 1)
     - If latency > slo_latency: emergency throttle; limit = max(min_limit, limit * backoff)

3. AIMD (Additive Increase / Multiplicative Decrease):
   Directly regulates concurrency against an SLO latency target:
     - Under SLO: limit += additive_increase (probe capacity)
     - Over SLO:  limit = max(min_limit, limit * backoff_factor) (shed load)
"""

from __future__ import annotations
import math
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional


class ConcurrencyLimitExceeded(Exception):
    """Raised when in-flight requests reach or exceed the current adaptive limit."""


@dataclass(frozen=True)
class LimiterMetrics:
    """Snapshot of limiter metrics at an instant."""
    in_flight: int
    current_limit: float
    min_rtt_ms: float
    smoothed_rtt_ms: float
    arrival_rate: float
    rejections: int
    completions: int


class LittlesLawEstimator:
    """Estimates system capacity and validates operational equilibrium using Little's Law.

    Formula: L = lambda * W
    """

    def __init__(self, window_seconds: float = 10.0) -> None:
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._completions: Deque[tuple[float, float]] = deque()  # (timestamp, duration_seconds)

    def record_completion(self, duration_seconds: float, now: Optional[float] = None) -> None:
        """Record the completion of a request with its total residence duration."""
        if now is None:
            now = time.monotonic()
        with self._lock:
            self._completions.append((now, duration_seconds))
            self._prune(now)

    def _prune(self, now: float) -> None:
        cutoff = now - self.window_seconds
        while self._completions and self._completions[0][0] < cutoff:
            self._completions.popleft()

    def get_arrival_rate(self, now: Optional[float] = None) -> float:
        """Arrival/throughput rate (lambda) in requests/second."""
        if now is None:
            now = time.monotonic()
        with self._lock:
            self._prune(now)
            count = len(self._completions)
            if count < 2:
                return float(count)
            span = max(self._completions[-1][0] - self._completions[0][0], 0.001)
            return count / span

    def get_average_latency(self, now: Optional[float] = None) -> float:
        """Average latency (W) in seconds."""
        if now is None:
            now = time.monotonic()
        with self._lock:
            self._prune(now)
            if not self._completions:
                return 0.0
            return sum(d for _, d in self._completions) / len(self._completions)

    def estimate_concurrency(self, now: Optional[float] = None) -> float:
        """Compute estimated concurrency L = lambda * W."""
        lam = self.get_arrival_rate(now)
        w = self.get_average_latency(now)
        return lam * w


class ConcurrencyContext:
    """Context manager for acquiring and releasing a concurrency slot."""

    def __init__(self, limiter: ConcurrencyLimiterBase) -> None:
        self.limiter = limiter
        self.start_time: float = 0.0

    def __enter__(self) -> ConcurrencyContext:
        self.start_time = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        duration = time.monotonic() - self.start_time
        success = exc_type is None
        self.limiter.release(duration, success=success)


class ConcurrencyLimiterBase:
    """Base class for adaptive concurrency limiters."""

    def __init__(
        self,
        initial_limit: float = 10.0,
        min_limit: float = 1.0,
        max_limit: float = 1000.0,
        slo_latency_ms: float = 200.0,
    ) -> None:
        self.limit = float(initial_limit)
        self.min_limit = float(min_limit)
        self.max_limit = float(max_limit)
        self.slo_latency_ms = slo_latency_ms
        self.in_flight: int = 0
        self.rejections: int = 0
        self.completions: int = 0
        self._lock = threading.Lock()
        self.estimator = LittlesLawEstimator()

    def acquire(self) -> ConcurrencyContext:
        """Attempt to acquire an execution slot.

        Raises:
            ConcurrencyLimitExceeded: if in-flight count meets or exceeds the current limit.
        """
        with self._lock:
            if self.in_flight >= int(math.floor(self.limit)):
                self.rejections += 1
                raise ConcurrencyLimitExceeded(
                    f"Concurrency limit reached ({self.in_flight}/{int(self.limit)})"
                )
            self.in_flight += 1
            return ConcurrencyContext(self)

    def try_acquire(self) -> Optional[ConcurrencyContext]:
        """Try to acquire a slot; returns None on rejection."""
        try:
            return self.acquire()
        except ConcurrencyLimitExceeded:
            return None

    def release(self, duration_seconds: float, success: bool = True) -> None:
        """Release a slot and feed back execution metrics to adapt the limit."""
        with self._lock:
            self.in_flight = max(0, self.in_flight - 1)
            self.completions += 1
        self.estimator.record_completion(duration_seconds)
        self._adjust_limit(duration_seconds * 1000.0, success)

    def _adjust_limit(self, rtt_ms: float, success: bool) -> None:
        raise NotImplementedError


class AIMDConcurrencyLimiter(ConcurrencyLimiterBase):
    """Additive Increase Multiplicative Decrease Concurrency Controller.

    Increases limit linearly while latency satisfies SLO; decreases multiplicatively
    when latency exceeds SLO or an error occurs.
    """

    def __init__(
        self,
        initial_limit: float = 10.0,
        min_limit: float = 1.0,
        max_limit: float = 500.0,
        slo_latency_ms: float = 100.0,
        additive_increase: float = 1.0,
        backoff_factor: float = 0.5,
    ) -> None:
        super().__init__(
            initial_limit=initial_limit,
            min_limit=min_limit,
            max_limit=max_limit,
            slo_latency_ms=slo_latency_ms,
        )
        self.additive_increase = additive_increase
        self.backoff_factor = backoff_factor

    def _adjust_limit(self, rtt_ms: float, success: bool) -> None:
        with self._lock:
            if not success or rtt_ms > self.slo_latency_ms:
                # Multiplicative decrease
                self.limit = max(self.min_limit, self.limit * self.backoff_factor)
            else:
                # Additive increase
                self.limit = min(self.max_limit, self.limit + self.additive_increase)

    def get_metrics(self) -> LimiterMetrics:
        with self._lock:
            return LimiterMetrics(
                in_flight=self.in_flight,
                current_limit=self.limit,
                min_rtt_ms=0.0,
                smoothed_rtt_ms=0.0,
                arrival_rate=self.estimator.get_arrival_rate(),
                rejections=self.rejections,
                completions=self.completions,
            )


class VegasAdaptiveLimiter(ConcurrencyLimiterBase):
    """TCP Vegas-style adaptive concurrency controller.

    Measures minimum RTT (base latency without queuing delay) and smoothed RTT.
    Computes virtual queue size:
        queue_size = limit * (1 - min_rtt / smoothed_rtt)
    Throttles if queue_size exceeds beta, expands if queue_size drops below alpha.
    """

    def __init__(
        self,
        initial_limit: float = 10.0,
        min_limit: float = 2.0,
        max_limit: float = 1000.0,
        slo_latency_ms: float = 250.0,
        alpha: float = 3.0,
        beta: float = 6.0,
        smoothing: float = 0.2,
        rtt_reset_period_seconds: float = 60.0,
    ) -> None:
        super().__init__(
            initial_limit=initial_limit,
            min_limit=min_limit,
            max_limit=max_limit,
            slo_latency_ms=slo_latency_ms,
        )
        self.alpha = alpha
        self.beta = beta
        self.smoothing = smoothing
        self.rtt_reset_period_seconds = rtt_reset_period_seconds

        self.min_rtt_ms: float = float("inf")
        self.smoothed_rtt_ms: float = 0.0
        self._last_min_rtt_reset = time.monotonic()

    def _adjust_limit(self, rtt_ms: float, success: bool) -> None:
        now = time.monotonic()
        with self._lock:
            # Periodic min_rtt reset to accommodate route/infrastructure shifts
            if now - self._last_min_rtt_reset > self.rtt_reset_period_seconds:
                self.min_rtt_ms = rtt_ms
                self._last_min_rtt_reset = now
            else:
                self.min_rtt_ms = min(self.min_rtt_ms, rtt_ms)

            # Exponential Moving Average for RTT
            if self.smoothed_rtt_ms <= 0:
                self.smoothed_rtt_ms = rtt_ms
            else:
                self.smoothed_rtt_ms = (
                    (1 - self.smoothing) * self.smoothed_rtt_ms + self.smoothing * rtt_ms
                )

            # Hard SLO violation overrides queuing calculation
            if not success or self.smoothed_rtt_ms > self.slo_latency_ms:
                self.limit = max(self.min_limit, self.limit * 0.7)
                return

            if self.smoothed_rtt_ms <= 0 or self.min_rtt_ms <= 0:
                return

            # Estimate queued items in the system
            queue_size = self.limit * (1.0 - (self.min_rtt_ms / self.smoothed_rtt_ms))

            if queue_size < self.alpha:
                # Underutilized: probe more concurrency
                self.limit = min(self.max_limit, self.limit + 1.0)
            elif queue_size > self.beta:
                # Congestion: back off gently
                self.limit = max(self.min_limit, self.limit - 1.0)
            # If between alpha and beta, system is in equilibrium; keep limit steady.

    def get_metrics(self) -> LimiterMetrics:
        with self._lock:
            return LimiterMetrics(
                in_flight=self.in_flight,
                current_limit=self.limit,
                min_rtt_ms=self.min_rtt_ms if self.min_rtt_ms != float("inf") else 0.0,
                smoothed_rtt_ms=self.smoothed_rtt_ms,
                arrival_rate=self.estimator.get_arrival_rate(),
                rejections=self.rejections,
                completions=self.completions,
            )
