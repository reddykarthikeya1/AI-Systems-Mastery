"""Module 09 Starter: Oracle RAC Cache Fusion & Data Guard Replication Engine.

TODO for Student:
Implement:
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
        raise NotImplementedError("Implement local cache read")

    def write_block(self, block_id: int, updates: dict[str, Any]) -> CachedBlock:
        raise NotImplementedError("Implement local block update and mark dirty")


class CacheFusionCoordinator:
    """Simulates Oracle Global Cache Service (GCS) managing cross-instance block transfers."""

    def __init__(self, nodes: list[RACNode]) -> None:
        self.nodes = {n.node_id: n for n in nodes}

    def request_block_for_read(self, requesting_node_id: str, block_id: int) -> CachedBlock:
        """Fetches block from another RAC node's cache via Cache Fusion, avoiding disk reads."""
        raise NotImplementedError("Implement Cache Fusion cross-instance block transfer")


class DataGuardEngine:
    """Simulates Oracle Active Data Guard physical standby replication."""

    def __init__(self, primary_id: str, standby_id: str, mode: ProtectionMode = ProtectionMode.MAX_AVAILABILITY) -> None:
        self.primary_id = primary_id
        self.standby_id = standby_id
        self.mode = mode
        self.primary_redo_log: list[dict[str, Any]] = []
        self.standby_applied_scns: list[int] = []
        self.is_standby_open_readonly = True

    def commit_on_primary(self, scn: int, sql_dml: str) -> bool:
        """Commits redo vector on primary and evaluates standby synchronization."""
        raise NotImplementedError("Implement primary commit with Data Guard redo transport")

    def perform_switchover(self) -> None:
        """Promotes Standby to Primary and demotes Primary to Standby."""
        raise NotImplementedError("Implement zero-data-loss Data Guard switchover")
