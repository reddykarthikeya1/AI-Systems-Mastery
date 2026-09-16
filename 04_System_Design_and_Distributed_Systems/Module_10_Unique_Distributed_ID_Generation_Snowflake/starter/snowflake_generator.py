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
from dataclasses import dataclass
DEFAULT_CUSTOM_EPOCH = 1704067200000
TIMESTAMP_BITS = 41
DATACENTER_ID_BITS = 5
WORKER_ID_BITS = 5
SEQUENCE_BITS = 12
MAX_DATACENTER_ID = (1 << DATACENTER_ID_BITS) - 1
MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

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

    def __init__(self, datacenter_id: int, worker_id: int, epoch: int=DEFAULT_CUSTOM_EPOCH) -> None:
        if not 0 <= datacenter_id <= MAX_DATACENTER_ID:
            raise ValueError(f'datacenter_id must be between 0 and {MAX_DATACENTER_ID}')
        if not 0 <= worker_id <= MAX_WORKER_ID:
            raise ValueError(f'worker_id must be between 0 and {MAX_WORKER_ID}')
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.epoch = epoch
        self._sequence = 0
        self._last_timestamp = -1
        self._lock = threading.Lock()

    def _current_timestamp_ms(self) -> int:
        raise NotImplementedError('10: implement _current_timestamp_ms()')

    def _wait_next_millis(self, last_timestamp: int) -> int:
        raise NotImplementedError('10: implement _wait_next_millis()')

    def next_id(self) -> int:
        """Generates the next k-ordered, monotonically increasing 64-bit unique ID."""
        raise NotImplementedError('10: implement next_id()')

    def parse_id(self, snowflake_id: int) -> ParsedSnowflake:
        """Unpacks a 64-bit snowflake ID into its semantic components."""
        raise NotImplementedError('10: implement parse_id()')