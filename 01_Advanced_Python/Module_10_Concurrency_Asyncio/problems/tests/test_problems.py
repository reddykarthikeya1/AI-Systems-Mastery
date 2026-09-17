"""Tests for Token Bucket Rate Limiter."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_token_bucket_limiter import TokenBucket
except ImportError:
    from p01_token_bucket_limiter import TokenBucket


def test_token_bucket_limiter():
    b = TokenBucket(2.0, 1.0)
    assert b.allow(0.0) is True
    assert b.allow(0.0) is True
    assert b.allow(0.0) is False
    assert b.allow(1.0) is True
