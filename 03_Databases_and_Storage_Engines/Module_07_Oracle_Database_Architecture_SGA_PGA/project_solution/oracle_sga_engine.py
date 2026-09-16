"""Module 07: Oracle Database SGA Memory & Storage Engine Reference Solution.

Implements:
1. Oracle Shared Pool Library Cache with Soft Parse vs Hard Parse plan caching.
2. Oracle Database Buffer Cache with touch-count LRU replacement algorithm.
3. Oracle Redo Log Buffer with LGWR synchronous flush on COMMIT.
4. Logical Tablespace Extent Allocator with High-Water Mark (HWM) tracking.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any


@dataclass
class BufferBlock:
    block_id: int
    data: dict[str, Any]
    is_dirty: bool = False
    touch_count: int = 1


class LibraryCache:
    """Simulates Oracle Shared Pool Library Cache for compiled SQL execution plans."""

    def __init__(self, capacity: int = 100) -> None:
        self.capacity = capacity
        self._plans: dict[str, str] = {}
        self.hard_parses = 0
        self.soft_parses = 0

    def parse_and_get_plan(self, sql_statement: str, bind_normalized_sql: str | None = None) -> tuple[str, bool]:
        """Returns (plan_hash, was_soft_parse)."""
        key = bind_normalized_sql if bind_normalized_sql else sql_statement
        if key in self._plans:
            self.soft_parses += 1
            return self._plans[key], True

        # Hard Parse: Generate plan hash
        self.hard_parses += 1
        plan_hash = f"PLAN_{hashlib.md5(key.encode('utf-8')).hexdigest()[:8].upper()}"
        self._plans[key] = plan_hash
        return plan_hash, False


class DatabaseBufferCache:
    """Simulates Oracle SGA Database Buffer Cache with Touch-Count LRU aging."""

    def __init__(self, capacity_blocks: int = 5) -> None:
        self.capacity = capacity_blocks
        self._cache: dict[int, BufferBlock] = {}

    def access_block(self, block_id: int, data: dict[str, Any] | None = None) -> BufferBlock:
        """Accesses block, incrementing touch_count, or reads into cache, evicting if necessary."""
        if block_id in self._cache:
            blk = self._cache[block_id]
            blk.touch_count += 1
            return blk

        # Cache Miss: Evict least-touched block if full
        if len(self._cache) >= self.capacity:
            victim_id = min(self._cache.keys(), key=lambda k: self._cache[k].touch_count)
            del self._cache[victim_id]

        new_block = BufferBlock(block_id=block_id, data=data or {}, is_dirty=False, touch_count=1)
        self._cache[block_id] = new_block
        return new_block

    def mark_dirty(self, block_id: int) -> None:
        """Marks block as modified in memory by DBWn."""
        if block_id in self._cache:
            self._cache[block_id].is_dirty = True

    def get_dirty_blocks(self) -> list[BufferBlock]:
        return [b for b in self._cache.values() if b.is_dirty]


class RedoLogBuffer:
    """Simulates the circular Redo Log Buffer flushed to disk by LGWR on COMMIT."""

    def __init__(self, buffer_size: int = 10) -> None:
        self.buffer_size = buffer_size
        self._buffer: list[str] = []
        self.flushed_to_online_redo_log: list[str] = []

    def append_redo_record(self, change_vector: str) -> None:
        """Appends change vector to in-memory buffer."""
        self._buffer.append(change_vector)

    def commit(self) -> int:
        """Simulates LGWR flush on COMMIT. Returns number of flushed redo records."""
        flushed_count = len(self._buffer)
        self.flushed_to_online_redo_log.extend(self._buffer)
        self._buffer.clear()
        return flushed_count


@dataclass
class Extent:
    extent_id: int
    start_block_id: int
    block_count: int


class TablespaceStorage:
    """Simulates Oracle logical extent allocation and high-water mark (HWM)."""

    def __init__(self, name: str, blocks_per_extent: int = 8) -> None:
        self.name = name
        self.blocks_per_extent = blocks_per_extent
        self.extents: list[Extent] = []
        self.high_water_mark_block: int = 0
        self._total_blocks_allocated: int = 0

    def allocate_extent(self) -> Extent:
        """Allocates a contiguous block extent."""
        ext_id = len(self.extents) + 1
        start_block = self._total_blocks_allocated + 1
        extent = Extent(extent_id=ext_id, start_block_id=start_block, block_count=self.blocks_per_extent)
        self.extents.append(extent)
        self._total_blocks_allocated += self.blocks_per_extent
        return extent

    def insert_row_into_block(self, target_block_id: int) -> None:
        """Simulates writing into a block, advancing high-water mark if beyond existing HWM."""
        if target_block_id > self._total_blocks_allocated:
            raise ValueError(f"Block #{target_block_id} has not been allocated in any extent!")
        if target_block_id > self.high_water_mark_block:
            self.high_water_mark_block = target_block_id
