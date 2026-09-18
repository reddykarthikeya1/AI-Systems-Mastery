"""Problem 01 — Exponential Backoff Retry Logic

Target: Production-grade implementation

Example:
    >>> calls = 0
    >>> def flaky():
    ...     global calls
    ...     calls += 1
    ...     if calls < 3:
    ...         raise ValueError('temporary')
    ...     return 'success'
    >>> retry_call(flaky, max_attempts=4)
    'success'
    >>> calls
    3

Hints:
    Hint 1: `fn` takes no arguments — your job is just to call it, catch a
        failure, and decide whether to try again or give up.
    Hint 2: Loop, counting attempts; call `fn()` inside a try/except and
        return its result immediately on success.
    Hint 3: Only re-raise once the attempt count has reached
        `max_attempts` — every earlier exception should be swallowed and
        retried, and the final re-raise must preserve the original
        exception (not wrap it in a new one).
"""

from __future__ import annotations


def retry_call(fn, max_attempts: int = 3, base_delay: float = 0.01):
    raise NotImplementedError('Implement retry_call')
