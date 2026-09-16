"""Module 09: Oracle RAC Cache Fusion & Data Guard Replication Engine Reference Solution.

Implements:
1. RAC Node with local Buffer Cache and Interconnect message dispatcher.
2. Cache Fusion Coordinator transferring dirty blocks between node buffer caches over RAM.
3. Active Data Guard Standby Database replicating Redo SCNs and supporting Read-Only queries.
4. Seamless failover switchover promoting Standby to Primary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ProtectionMode(Enum):
    MAX_PROTECTION = "MAX_PROTECTION"
    MAX_AVAILABILITY = "MAX_AVAILABILITY"
    MAX_PERFORMANCE = "MAX_PERFORMANCE"


@dataclass
class CachedBlock:
    block_id: int
    data: dict[str, Any]
    is_dirty: bool = False
    lock_mode: str = "SHARED"  # SHARED or EXCLUSIVE


class RACNode:
    """Simulates an individual Oracle RAC instance with private SGA and buffer cache."""

    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.buffer_cache: dict[int, CachedBlock] = {}
        self.is_alive: bool = True

    def read_block(self, block_id: int) -> CachedBlock | None:
        if not self.is_alive:
            raise RuntimeError(f"Node {self.node_id} is offline.")
        return self.buffer_cache.get(block_id)

    def write_block(self, block_id: int, updates: dict[str, Any]) -> CachedBlock:
        if not self.is_alive:
            raise RuntimeError(f"Node {self.node_id} is offline.")
        if block_id not in self.buffer_cache:
            blk = CachedBlock(block_id=block_id, data=updates, is_dirty=True, lock_mode="EXCLUSIVE")
            self.buffer_cache[block_id] = blk
            return blk

        blk = self.buffer_cache[block_id]
        blk.data.update(updates)
        blk.is_dirty = True
        blk.lock_mode = "EXCLUSIVE"
        return blk


class CacheFusionCoordinator:
    """Simulates Oracle Global Cache Service (GCS) managing cross-instance block transfers."""

    def __init__(self, nodes: list[RACNode]) -> None:
        self.nodes = {n.node_id: n for n in nodes}
        self.transfers_count = 0

    def request_block_for_read(self, requesting_node_id: str, block_id: int) -> CachedBlock:
        """Fetches block from another RAC node's cache via Cache Fusion, avoiding disk reads."""
        req_node = self.nodes[requesting_node_id]
        if not req_node.is_alive:
            raise RuntimeError(f"Requesting node {requesting_node_id} is offline.")

        # Check if already in requesting node's buffer cache
        if block_id in req_node.buffer_cache:
            return req_node.buffer_cache[block_id]

        # Scan other alive RAC nodes for the block in RAM (Cache Fusion)
        for other_id, other_node in self.nodes.items():
            if other_id != requesting_node_id and other_node.is_alive:
                if block_id in other_node.buffer_cache:
                    source_blk = other_node.buffer_cache[block_id]
                    # Cache Fusion Transfer: Copy directly over interconnect
                    self.transfers_count += 1
                    fused_block = CachedBlock(
                        block_id=block_id,
                        data=dict(source_blk.data),
                        is_dirty=source_blk.is_dirty,
                        lock_mode="SHARED",
                    )
                    req_node.buffer_cache[block_id] = fused_block
                    # Downgrade source node to SHARED
                    source_blk.lock_mode = "SHARED"
                    return fused_block

        # Fallback to shared disk read (slow path)
        disk_blk = CachedBlock(block_id=block_id, data={}, is_dirty=False, lock_mode="SHARED")
        req_node.buffer_cache[block_id] = disk_blk
        return disk_blk


class DataGuardEngine:
    """Simulates Oracle Active Data Guard physical standby replication."""

    def __init__(self, primary_id: str, standby_id: str, mode: ProtectionMode = ProtectionMode.MAX_AVAILABILITY) -> None:
        self.primary_id = primary_id
        self.standby_id = standby_id
        self.mode = mode
        self.primary_redo_log: list[dict[str, Any]] = []
        self.standby_applied_scns: list[int] = []
        self.is_standby_open_readonly: bool = True
        self.network_link_healthy: bool = True

    def commit_on_primary(self, scn: int, sql_dml: str) -> bool:
        """Commits redo vector on primary and evaluates standby synchronization."""
        entry = {"scn": scn, "dml": sql_dml}
        self.primary_redo_log.append(entry)

        if self.mode == ProtectionMode.MAX_PROTECTION:
            if not self.network_link_healthy:
                raise RuntimeError("Max Protection violation: Standby unreachable. Primary halted!")
            self.standby_applied_scns.append(scn)
            return True

        elif self.mode == ProtectionMode.MAX_AVAILABILITY:
            if self.network_link_healthy:
                self.standby_applied_scns.append(scn)
            # If network broken, downgrades to async without halting primary
            return True

        elif self.mode == ProtectionMode.MAX_PERFORMANCE:
            # Asynchronous: ships in background
            if self.network_link_healthy:
                self.standby_applied_scns.append(scn)
            return True

        return False

    def query_standby_readonly(self) -> list[int]:
        """Returns SCNs available for read-only reporting on the standby database."""
        if not self.is_standby_open_readonly:
            raise RuntimeError("Standby database is not open for read queries.")
        return list(self.standby_applied_scns)

    def perform_switchover(self) -> None:
        """Promotes Standby to Primary and demotes Primary to Standby."""
        old_primary = self.primary_id
        self.primary_id = self.standby_id
        self.standby_id = old_primary
