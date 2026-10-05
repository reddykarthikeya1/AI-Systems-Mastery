#!/usr/bin/env python3
"""
===============================================================================
Distributed Rate Limiter Simulator: Sliding Window Log vs Token Bucket
===============================================================================
Metaphor:
  A subway turnstile.
  - Naive Fixed Window: The turnstile resets its counter at 12:00:00 and 12:01:00.
    A crowd of 100 enters at 12:00:59, and another 100 enters at 12:01:01.
    Result: 200 people rushed through in 2 seconds, crushing the platform!
  - Sliding Window Log: The turnstile counts how many people walked through in the
    EXACT rolling 60-second window before your foot steps forward.
===============================================================================
"""

import time
import threading
from collections import deque
from typing import Dict, Tuple


class FixedWindowLimiter:
    """
    Vulnerable to the Edge-of-Window Burst Flaw.
    Allows up to 2x the limit across window boundaries.
    """
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window_seconds = window_seconds
        self.lock = threading.Lock()
        self.current_window = 0
        self.counter = 0

    def allow_request(self, current_time: float) -> Tuple[bool, str]:
        with self.lock:
            window_bucket = int(current_time // self.window_seconds)
            if window_bucket != self.current_window:
                self.current_window = window_bucket
                self.counter = 0

            if self.counter < self.limit:
                self.counter += 1
                return True, f"ALLOWED ({self.counter}/{self.limit})"
            return False, f"REJECTED 429 ({self.counter}/{self.limit})"


class SlidingWindowLogLimiter:
    """
    Production-grade sliding window log (simulates Redis ZSET):
    - ZREMRANGEBYSCORE: Remove timestamps older than (now - window)
    - ZCARD: Count requests in the rolling window
    - ZADD: Append current timestamp if under limit
    """
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window_seconds = window_seconds
        self.lock = threading.Lock()
        # Per-user timestamp logs: {user_id: deque([t1, t2, ...])}
        self.user_logs: Dict[str, deque] = {}

    def allow_request(self, user_id: str, current_time: float) -> Tuple[bool, str]:
        with self.lock:
            if user_id not in self.user_logs:
                self.user_logs[user_id] = deque()

            log = self.user_logs[user_id]
            cutoff = current_time - self.window_seconds

            # 1. Purge entries outside sliding window
            while log and log[0] <= cutoff:
                log.popleft()

            # 2. Check current count
            if len(log) < self.limit:
                log.append(current_time)
                return True, f"ALLOWED ({len(log)}/{self.limit} in last {self.window_seconds}s)"
            else:
                oldest = log[0]
                retry_after = round(self.window_seconds - (current_time - oldest), 2)
                return False, f"REJECTED 429 (Retry-After: {retry_after}s)"


class TokenBucketLimiter:
    """
    Smooth replenishment with burst support.
    Tokens refill continuously at (capacity / refill_period) tokens/sec.
    """
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.last_update = time.time()
        self.lock = threading.Lock()

    def allow_request(self, tokens_needed: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.last_update = now

            # Refill tokens up to maximum capacity
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False


def run_demonstration():
    print("=" * 70)
    print(" DISTRIBUTED RATE LIMITER ARCHITECTURAL BENCHMARK")
    print("=" * 70)

    # SCENARIO 1: The Edge-of-Window Flaw in Fixed Window Limiter
    print("\n--- [EXPERIMENT 1] Fixed Window Boundary Flaw Demonstration ---")
    print("Config: Max 5 requests per 10-second window (t=0 to 10, t=10 to 20)")
    fixed_limiter = FixedWindowLimiter(limit=5, window_seconds=10.0)

    # 5 requests sent at t = 9.5s (end of Window 0)
    print("\n[t = 9.5s] Burst 1: Sending 5 requests at the end of Window 0...")
    for i in range(5):
        allowed, msg = fixed_limiter.allow_request(current_time=9.5)
        print(f"  Req {i+1}: {msg}")

    # 5 requests sent at t = 10.1s (start of Window 1)
    print("\n[t = 10.1s] Burst 2: Sending 5 requests at the start of Window 1...")
    for i in range(5):
        allowed, msg = fixed_limiter.allow_request(current_time=10.1)
        print(f"  Req {i+6}: {msg}")

    print("\n[ANALYSIS] In a 0.6-second span (t=9.5 to 10.1), 10 requests PASSED!")
    print("           Fixed Window allowed 2x the capacity across boundary.")

    # SCENARIO 2: Sliding Window Log Prevents Boundary Burst
    print("\n" + "=" * 70)
    print("--- [EXPERIMENT 2] Sliding Window Log: Strict Rolling Guarantee ---")
    print("Config: Max 5 requests per rolling 10-second window")
    sliding_limiter = SlidingWindowLogLimiter(limit=5, window_seconds=10.0)

    print("\n[t = 9.5s] Burst 1: Sending 5 requests...")
    for i in range(5):
        allowed, msg = sliding_limiter.allow_request(user_id="alice", current_time=9.5)
        print(f"  Req {i+1}: {msg}")

    print("\n[t = 10.1s] Burst 2: Sending 5 requests at boundary...")
    for i in range(5):
        allowed, msg = sliding_limiter.allow_request(user_id="alice", current_time=10.1)
        print(f"  Req {i+6}: {msg}")

    print("\n[ANALYSIS] Sliding Window correctly throttled all requests at t=10.1s!")
    print("           It strictly guarantees no more than 5 requests in any 10-second interval.")

    # SCENARIO 3: Concurrent Multi-Threaded Stress Test
    print("\n" + "=" * 70)
    print("--- [EXPERIMENT 3] Multi-Threaded Concurrent Sliding Window Test ---")
    print("Spinning up 20 concurrent worker threads against a 10 req/sec quota...")

    concurrent_limiter = SlidingWindowLogLimiter(limit=10, window_seconds=1.0)
    results = {"allowed": 0, "rejected": 0}
    res_lock = threading.Lock()

    def worker(worker_id: int):
        now = time.time()
        allowed, _ = concurrent_limiter.allow_request(user_id="cluster_client", current_time=now)
        with res_lock:
            if allowed:
                results["allowed"] += 1
            else:
                results["rejected"] += 1

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Results across 20 simultaneous threads:")
    print(f"  - Requests Allowed  : {results['allowed']} (Expected: exactly 10)")
    print(f"  - Requests Throttled: {results['rejected']} (Expected: exactly 10)")
    assert results["allowed"] == 10, f"Thread-safety failed! Expected 10, got {results['allowed']}"
    print("  [PASS] Concurrent sliding window is 100% thread-safe under contention.")
    print("=" * 70)


if __name__ == "__main__":
    run_demonstration()
