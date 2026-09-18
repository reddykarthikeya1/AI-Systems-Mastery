"""Problem 01 — Exponential Backoff Retry Logic

Target: Production-grade implementation
"""

from __future__ import annotations


def retry_call(fn, max_attempts: int = 3, base_delay: float = 0.01):
    attempts = 0
    while True:
        try:
            attempts += 1
            return fn()
        except Exception as e:
            if attempts >= max_attempts:
                raise e
