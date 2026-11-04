"""Dual-Dimensional Rate Limiter (RPM + TPM) for LLM Serving & API Gateways.

Motivation:
-----------
LLM gateways (e.g., OpenAI, Anthropic, Gemini) enforce multi-dimensional quotas:
1. RPM (Requests Per Minute): Throttles network/connection overhead and queue depth.
2. TPM (Tokens Per Minute): Throttles GPU compute time and KV-cache memory pressure.

A single query consuming 30,000 tokens could overwhelm GPU memory even if RPM is low.
Conversely, hundreds of 5-token queries could overwhelm connection pools even if TPM is low.

Atomic Invariant:
-----------------
Both buckets MUST be checked and decremented atomically.
If either RPM or TPM is exhausted:
  - ZERO tokens are deducted (all-or-nothing rollback).
  - The request is rejected with `retry_after_seconds`.
"""

from __future__ import annotations
import math
import threading
import time
from dataclasses import dataclass
from typing import Any, Optional, Tuple

LUA_DUAL_TOKEN_BUCKET = """
-- KEYS[1]: Redis hash key for the client bucket
-- ARGV[1]: Current timestamp (floating point seconds)
-- ARGV[2]: Max RPM (capacity)
-- ARGV[3]: Max TPM (capacity)
-- ARGV[4]: Requested RPM cost (usually 1)
-- ARGV[5]: Requested TPM cost (e.g., prompt + max completion tokens)

local key = KEYS[1]
local now = tonumber(ARGV[1])
local max_rpm = tonumber(ARGV[2])
local max_tpm = tonumber(ARGV[3])
local cost_rpm = tonumber(ARGV[4])
local cost_tpm = tonumber(ARGV[5])

-- Refill rates per second
local rpm_refill_rate = max_rpm / 60.0
local tpm_refill_rate = max_tpm / 60.0

local data = redis.call('HMGET', key, 'rpm_tokens', 'tpm_tokens', 'last_updated')
local rpm_tokens = tonumber(data[1])
local tpm_tokens = tonumber(data[2])
local last_updated = tonumber(data[3])

if not last_updated then
    rpm_tokens = max_rpm
    tpm_tokens = max_tpm
    last_updated = now
else
    local elapsed = math.max(0, now - last_updated)
    rpm_tokens = math.min(max_rpm, rpm_tokens + (elapsed * rpm_refill_rate))
    tpm_tokens = math.min(max_tpm, tpm_tokens + (elapsed * tpm_refill_rate))
    last_updated = now
end

-- Atomic check: Both must be sufficient
if (rpm_tokens >= cost_rpm) and (tpm_tokens >= cost_tpm) then
    rpm_tokens = rpm_tokens - cost_rpm
    tpm_tokens = tpm_tokens - cost_tpm
    redis.call('HMSET', key, 'rpm_tokens', rpm_tokens, 'tpm_tokens', tpm_tokens, 'last_updated', last_updated)
    redis.call('EXPIRE', key, 120) -- 2 minutes TTL
    return {1, rpm_tokens, tpm_tokens, 0} -- Allowed, remaining_rpm, remaining_tpm, retry_after
else
    -- Compute retry_after based on whichever bucket is deficient
    local rpm_deficit = math.max(0, cost_rpm - rpm_tokens)
    local tpm_deficit = math.max(0, cost_tpm - tpm_tokens)
    local wait_rpm = rpm_deficit / rpm_refill_rate
    local wait_tpm = tpm_deficit / tpm_refill_rate
    local retry_after = math.max(wait_rpm, wait_tpm)
    
    -- Save refilled tokens even on rejection
    redis.call('HMSET', key, 'rpm_tokens', rpm_tokens, 'tpm_tokens', tpm_tokens, 'last_updated', last_updated)
    redis.call('EXPIRE', key, 120)
    return {0, rpm_tokens, tpm_tokens, retry_after}
end
"""


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    remaining_rpm: float
    remaining_tpm: float
    retry_after_seconds: float
    reason: Optional[str] = None


class DualTokenBucketLimiter:
    """Thread-safe Dual Token Bucket (RPM + TPM) rate limiter."""

    def __init__(
        self,
        max_rpm: float = 60.0,
        max_tpm: float = 10_000.0,
        redis_client: Any = None,
    ) -> None:
        self.max_rpm = float(max_rpm)
        self.max_tpm = float(max_tpm)
        self.redis = redis_client
        self._lock = threading.Lock()
        # In-memory store: client_id -> (rpm_tokens, tpm_tokens, last_updated)
        self._buckets: dict[str, tuple[float, float, float]] = {}

    def _refill(
        self, current_rpm: float, current_tpm: float, elapsed: float
    ) -> tuple[float, float]:
        rpm_refill_rate = self.max_rpm / 60.0
        tpm_refill_rate = self.max_tpm / 60.0
        new_rpm = min(self.max_rpm, current_rpm + (elapsed * rpm_refill_rate))
        new_tpm = min(self.max_tpm, current_tpm + (elapsed * tpm_refill_rate))
        return new_rpm, new_tpm

    def acquire(
        self,
        client_id: str,
        tokens_requested: int = 1,
        now: Optional[float] = None,
    ) -> RateLimitResult:
        """Attempt to acquire 1 request slot and `tokens_requested` token slots."""
        if tokens_requested <= 0:
            raise ValueError("Requested tokens must be > 0")

        if now is None:
            now = time.monotonic()

        if self.redis is not None:
            key = f"rate_limit:{client_id}"
            res = self.redis.eval(
                LUA_DUAL_TOKEN_BUCKET,
                1,
                key,
                now,
                self.max_rpm,
                self.max_tpm,
                1,
                tokens_requested,
            )
            allowed = bool(res[0] == 1)
            rem_rpm = float(res[1])
            rem_tpm = float(res[2])
            retry_after = float(res[3])
            reason = None if allowed else ("RPM Exceeded" if rem_rpm < 1 else "TPM Exceeded")
            return RateLimitResult(
                allowed=allowed,
                remaining_rpm=rem_rpm,
                remaining_tpm=rem_tpm,
                retry_after_seconds=retry_after,
                reason=reason,
            )

        with self._lock:
            if client_id not in self._buckets:
                rpm_tokens = self.max_rpm
                tpm_tokens = self.max_tpm
                last_updated = now
            else:
                rpm_tokens, tpm_tokens, last_updated = self._buckets[client_id]
                elapsed = max(0.0, now - last_updated)
                rpm_tokens, tpm_tokens = self._refill(rpm_tokens, tpm_tokens, elapsed)
                last_updated = now

            cost_rpm = 1.0
            cost_tpm = float(tokens_requested)

            rpm_refill_rate = self.max_rpm / 60.0
            tpm_refill_rate = self.max_tpm / 60.0

            if rpm_tokens >= cost_rpm and tpm_tokens >= cost_tpm:
                rpm_tokens -= cost_rpm
                tpm_tokens -= cost_tpm
                self._buckets[client_id] = (rpm_tokens, tpm_tokens, last_updated)
                return RateLimitResult(
                    allowed=True,
                    remaining_rpm=rpm_tokens,
                    remaining_tpm=tpm_tokens,
                    retry_after_seconds=0.0,
                )
            else:
                rpm_deficit = max(0.0, cost_rpm - rpm_tokens)
                tpm_deficit = max(0.0, cost_tpm - tpm_tokens)
                wait_rpm = rpm_deficit / rpm_refill_rate if rpm_deficit > 0 else 0.0
                wait_tpm = tpm_deficit / tpm_refill_rate if tpm_deficit > 0 else 0.0
                retry_after = max(wait_rpm, wait_tpm)
                reason = "RPM Exceeded" if rpm_deficit > 0 else "TPM Exceeded"

                # Keep the refilled token values
                self._buckets[client_id] = (rpm_tokens, tpm_tokens, last_updated)
                return RateLimitResult(
                    allowed=False,
                    remaining_rpm=rpm_tokens,
                    remaining_tpm=tpm_tokens,
                    retry_after_seconds=retry_after,
                    reason=reason,
                )
