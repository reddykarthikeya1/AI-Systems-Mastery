"""Tests for Exponential Backoff Retry Logic."""
from __future__ import annotations

import pytest
from p01_retry_decorator import retry_call


def test_retry_call():
    calls = 0
    def flaky():
        nonlocal calls
        calls += 1
        if calls < 3: raise ValueError('temporary')
        return 'success'
    assert retry_call(flaky, max_attempts=4) == 'success'
    assert calls == 3
