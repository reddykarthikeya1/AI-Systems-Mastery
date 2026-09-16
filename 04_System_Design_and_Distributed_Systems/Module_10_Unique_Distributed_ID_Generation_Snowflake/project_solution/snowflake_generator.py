#!/usr/bin/env python3
"""Module 10: In-Process Architectural Simulation Model: Twitter Snowflake 64-Bit Distributed ID Generator.

Bit Structure:
- 1  bit : Sign bit (unused, always 0)
- 41 bits: Milliseconds since custom epoch (~69.7 years lifespan)
- 5  bits: Datacenter ID (0 - 31)
- 5  bits: Worker ID     (0 - 31)
- 12 bits: Sequence ID   (0 - 4095 per millisecond per worker)
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass

# Custom Epoch: Jan 1, 2024 00:00:00 UTC in milliseconds
DEFAULT_CUSTOM_EPOCH = 1704067200000

# Bit allocation constants
TIMESTAMP_BITS = 41
DATACENTER_ID_BITS = 5
WORKER_ID_BITS = 5
SEQUENCE_BITS = 12

# Maximum values (masks)
MAX_DATACENTER_ID = (1 << DATACENTER_ID_BITS) - 1  # 31
MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1          # 31
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1            # 4095

# Bit shift offsets
WORKER_ID_SHIFT = SEQUENCE_BITS                     # 12
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS # 17
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS # 22


@dataclass(frozen=True)
class ParsedSnowflake:
    id: int
    timestamp_ms: int
    datacenter_id: int
    worker_id: int
    sequence: int


class ClockMovedBackwardsError(RuntimeError):
    """Raised when the system physical clock moves backwards due to NTP skew."""


class SnowflakeGenerator:
    """Thread-safe, high-throughput 64-bit Snowflake ID Generator."""

    def __init__(
        self,
        datacenter_id: int,
        worker_id: int,
        epoch: int = DEFAULT_CUSTOM_EPOCH,
    ) -> None:
        if not (0 <= datacenter_id <= MAX_DATACENTER_ID):
            raise ValueError(f"datacenter_id must be between 0 and {MAX_DATACENTER_ID}")
        if not (0 <= worker_id <= MAX_WORKER_ID):
            raise ValueError(f"worker_id must be between 0 and {MAX_WORKER_ID}")

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.epoch = epoch

        self._sequence = 0
        self._last_timestamp = -1
        self._lock = threading.Lock()

    def _current_timestamp_ms(self) -> int:
        return time.time_ns() // 1_000_000

    def _wait_next_millis(self, last_timestamp: int) -> int:
        timestamp = self._current_timestamp_ms()
        while timestamp <= last_timestamp:
            time.sleep(0.0001)  # 100 microseconds spin sleep
            timestamp = self._current_timestamp_ms()
        return timestamp

    def next_id(self) -> int:
        """Generates the next k-ordered, monotonically increasing 64-bit unique ID."""
        with self._lock:
            timestamp = self._current_timestamp_ms()

            if timestamp < self._last_timestamp:
                drift = self._last_timestamp - timestamp
                raise ClockMovedBackwardsError(
                    f"Clock moved backwards by {drift} ms! Refusing to generate ID to protect uniqueness."
                )

            if timestamp == self._last_timestamp:
                # Sequence increment within same millisecond
                self._sequence = (self._sequence + 1) & MAX_SEQUENCE
                if self._sequence == 0:
                    # Sequence overflow (generated > 4096 IDs in 1ms) -> wait for next ms
                    timestamp = self._wait_next_millis(self._last_timestamp)
            else:
                # New millisecond -> reset sequence
                self._sequence = 0

            self._last_timestamp = timestamp

            # Bitwise packing
            snowflake_id = (
                ((timestamp - self.epoch) << TIMESTAMP_SHIFT)
                | (self.datacenter_id << DATACENTER_ID_SHIFT)
                | (self.worker_id << WORKER_ID_SHIFT)
                | self._sequence
            )
            return snowflake_id

    def parse_id(self, snowflake_id: int) -> ParsedSnowflake:
        """Unpacks a 64-bit snowflake ID into its semantic components."""
        sequence = snowflake_id & MAX_SEQUENCE
        worker_id = (snowflake_id >> WORKER_ID_SHIFT) & MAX_WORKER_ID
        datacenter_id = (snowflake_id >> DATACENTER_ID_SHIFT) & MAX_DATACENTER_ID
        relative_timestamp = snowflake_id >> TIMESTAMP_SHIFT
        absolute_timestamp = relative_timestamp + self.epoch

        return ParsedSnowflake(
            id=snowflake_id,
            timestamp_ms=absolute_timestamp,
            datacenter_id=datacenter_id,
            worker_id=worker_id,
            sequence=sequence,
        )
