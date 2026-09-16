"""Module 13: Redis Sentinel, Clustering, Lua & Streams Engine (Solution).

Implements:
1. RedisClusterRouter: 16,384 Hash Slot management, Hash Tag extraction, and -MOVED redirection.
2. SentinelCoordinator: Quorum-based failure detection (SDOWN/ODOWN) and replica offset promotion.
3. LuaScriptExecutor: SHA1 script registry and atomic token bucket rate-limiting.
4. RedisStreamEngine: Stream append, Consumer Groups, Pending Entries List (PEL), and XCLAIM recovery.
"""

from __future__ import annotations

import binascii
import hashlib
from typing import Any, Callable


class ClusterMovedError(Exception):
    """Raised when a query hits a node that does not own the requested hash slot."""

    def __init__(self, slot: int, target_node: str) -> None:
        super().__init__(f"-MOVED {slot} {target_node}")
        self.slot = slot
        self.target_node = target_node


class RedisClusterRouter:
    """Simulates Redis Cluster 16,384 Hash Slot routing and Hash Tag extraction."""

    def __init__(self) -> None:
        # Maps slot index (0 to 16383) to node ID
        self.slots: dict[int, str] = {}

    @staticmethod
    def extract_hash_tag(key: str) -> str:
        """Extract substring inside first '{...}' if present, else return key."""
        start = key.find("{")
        if start != -1:
            end = key.find("}", start + 1)
            if end != -1 and end > start + 1:
                return key[start + 1 : end]
        return key

    @classmethod
    def compute_slot(cls, key: str) -> int:
        """Compute CRC16 modulo 16384 for the key or its extracted hash tag."""
        tag = cls.extract_hash_tag(key)
        crc = binascii.crc_hqx(tag.encode("utf-8"), 0)
        return crc % 16384

    def assign_range(self, node_id: str, start_slot: int, end_slot: int) -> None:
        """Assign an inclusive slot range to a specific cluster node."""
        for slot in range(start_slot, end_slot + 1):
            self.slots[slot] = node_id

    def get_node_for_key(self, key: str) -> str:
        """Resolve which cluster node currently owns the key."""
        slot = self.compute_slot(key)
        if slot not in self.slots:
            raise KeyError(f"Slot {slot} is unassigned in cluster topology")
        return self.slots[slot]

    def execute_command(self, client_connected_node: str, key: str, cmd: str, *args: str) -> str:
        """Simulate command execution, raising ClusterMovedError if client sent to wrong shard."""
        correct_node = self.get_node_for_key(key)
        if client_connected_node != correct_node:
            slot = self.compute_slot(key)
            raise ClusterMovedError(slot=slot, target_node=correct_node)
        return f"OK: {cmd} executed on {correct_node}"


class SentinelCoordinator:
    """Coordinates quorum-based failure detection and automated failover."""

    def __init__(self, master_id: str, quorum: int = 2) -> None:
        self.master_id = master_id
        self.quorum = quorum
        self.replicas: dict[str, dict[str, int]] = {}
        self.sentinel_votes: dict[str, bool] = {}

    def register_replica(self, replica_id: str, priority: int, repl_offset: int) -> None:
        self.replicas[replica_id] = {
            "priority": priority,
            "repl_offset": repl_offset,
        }

    def report_heartbeat(self, sentinel_id: str, is_master_alive: bool) -> None:
        self.sentinel_votes[sentinel_id] = is_master_alive

    def check_health(self) -> str:
        dead_votes = sum(1 for alive in self.sentinel_votes.values() if not alive)
        if dead_votes == 0:
            return "HEALTHY"
        if dead_votes < self.quorum:
            return "SDOWN"
        return "ODOWN"

    def execute_failover(self) -> str:
        status = self.check_health()
        if status != "ODOWN":
            raise RuntimeError(f"Cannot failover when master status is {status}; requires ODOWN")

        eligible = [
            (rep_id, meta)
            for rep_id, meta in self.replicas.items()
            if meta["priority"] > 0
        ]
        if not eligible:
            raise RuntimeError("No eligible replicas found for failover (priority > 0)")

        # Sort by repl_offset desc, then priority asc, then replica_id asc
        promoted_id, _ = max(
            eligible,
            key=lambda item: (item[1]["repl_offset"], -item[1]["priority"], -ord(item[0][0])),
        )

        self.master_id = promoted_id
        del self.replicas[promoted_id]
        self.sentinel_votes.clear()
        return promoted_id


class LuaScriptExecutor:
    """Simulates Redis Lua scripting environment with SHA1 caching and atomic execution."""

    def __init__(self) -> None:
        self._scripts: dict[str, Callable[..., Any]] = {}

    def register_script(self, script_fn: Callable[..., Any], script_src: str) -> str:
        sha1 = hashlib.sha1(script_src.encode("utf-8")).hexdigest()
        self._scripts[sha1] = script_fn
        return sha1

    def evalsha(self, sha1: str, keys: list[str], args: list[Any], storage: dict[str, Any]) -> Any:
        if sha1 not in self._scripts:
            raise KeyError(f"NOSCRIPT No matching script. Please use EVAL instead with sha {sha1}")
        # Atomic execution inside simulated single thread
        return self._scripts[sha1](keys, args, storage)


def token_bucket_rate_limiter(
    keys: list[str],
    args: list[Any],
    storage: dict[str, Any],
) -> int:
    """Atomic Lua-style token bucket rate limiter.

    KEYS[0]: rate limit key
    ARGS[0]: capacity (int)
    ARGS[1]: refill_rate_per_sec (float)
    ARGS[2]: requested_tokens (int)
    ARGS[3]: current_timestamp (float)
    """
    key = keys[0]
    capacity = int(args[0])
    refill_rate = float(args[1])
    requested = int(args[2])
    now = float(args[3])

    state = storage.get(key, {"tokens": float(capacity), "last_updated": now})
    tokens = float(state["tokens"])
    last_updated = float(state["last_updated"])

    elapsed = max(0.0, now - last_updated)
    tokens = min(float(capacity), tokens + (elapsed * refill_rate))

    if tokens >= requested:
        tokens -= requested
        storage[key] = {"tokens": tokens, "last_updated": now}
        return 1  # Allowed
    else:
        storage[key] = {"tokens": tokens, "last_updated": now}
        return 0  # Rejected / Rate limited


class RedisStreamEngine:
    """Simulates Redis Streams, Consumer Groups, PEL, and message reclamation."""

    def __init__(self) -> None:
        self.streams: dict[str, list[dict[str, Any]]] = {}
        self.consumer_groups: dict[str, dict[str, Any]] = {}

    def xadd(self, stream_key: str, fields: dict[str, Any], entry_id: str | None = None) -> str:
        if stream_key not in self.streams:
            self.streams[stream_key] = []

        if entry_id is None:
            # Simulated timestamp-sequence ID
            entry_id = f"{1700000000000 + len(self.streams[stream_key]) * 1000}-0"

        entry = {"id": entry_id, "data": dict(fields)}
        self.streams[stream_key].append(entry)
        return entry_id

    def xgroup_create(self, stream_key: str, group_name: str) -> None:
        group_id = f"{stream_key}:{group_name}"
        self.consumer_groups[group_id] = {
            "stream_key": stream_key,
            "group_name": group_name,
            "last_delivered_idx": -1,
            "pel": {},  # entry_id -> {"consumer": str, "delivered_at": float, "data": dict}
        }

    def xreadgroup(
        self,
        stream_key: str,
        group_name: str,
        consumer_name: str,
        count: int = 1,
        now: float = 1000.0,
    ) -> list[dict[str, Any]]:
        group_id = f"{stream_key}:{group_name}"
        if group_id not in self.consumer_groups:
            raise KeyError(f"NOGROUP No such consumer group {group_name}")

        group = self.consumer_groups[group_id]
        stream_entries = self.streams.get(stream_key, [])
        delivered: list[dict[str, Any]] = []

        start_idx = group["last_delivered_idx"] + 1
        end_idx = min(start_idx + count, len(stream_entries))

        for idx in range(start_idx, end_idx):
            entry = stream_entries[idx]
            eid = entry["id"]
            # Record into Pending Entries List (PEL)
            group["pel"][eid] = {
                "consumer": consumer_name,
                "delivered_at": now,
                "data": entry["data"],
            }
            delivered.append(entry)
            group["last_delivered_idx"] = idx

        return delivered

    def xack(self, stream_key: str, group_name: str, entry_ids: list[str]) -> int:
        group_id = f"{stream_key}:{group_name}"
        if group_id not in self.consumer_groups:
            return 0

        pel = self.consumer_groups[group_id]["pel"]
        acked = 0
        for eid in entry_ids:
            if eid in pel:
                del pel[eid]
                acked += 1
        return acked

    def xclaim(
        self,
        stream_key: str,
        group_name: str,
        new_consumer: str,
        min_idle_ms: int,
        now: float = 2000.0,
    ) -> list[dict[str, Any]]:
        group_id = f"{stream_key}:{group_name}"
        if group_id not in self.consumer_groups:
            return []

        pel = self.consumer_groups[group_id]["pel"]
        reclaimed: list[dict[str, Any]] = []

        for eid, meta in list(pel.items()):
            idle_ms = (now - meta["delivered_at"]) * 1000
            if idle_ms >= min_idle_ms:
                meta["consumer"] = new_consumer
                meta["delivered_at"] = now
                reclaimed.append({"id": eid, "consumer": new_consumer, "data": meta["data"]})

        return reclaimed
