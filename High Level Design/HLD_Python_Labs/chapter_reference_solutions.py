"""Small, executable reference solutions for textbook chapters without a dedicated lab.

These are teaching models, not production distributed services. Each class is kept
intentionally small so a learner can connect the textbook idea to runnable code.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
from math import ceil, floor
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple
import uuid


def _stable_bucket(key: str, count: int) -> int:
    if count <= 0:
        raise ValueError("count must be > 0")
    digest = sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % count


class RoundRobinBalancer:
    """Deterministic round-robin selection for a fixed backend set."""

    def __init__(self, backends: Sequence[str]) -> None:
        if not backends or len(set(backends)) != len(backends):
            raise ValueError("backends must be non-empty and unique")
        self.backends = list(backends)
        self._next = 0

    def choose(self) -> str:
        backend = self.backends[self._next]
        self._next = (self._next + 1) % len(self.backends)
        return backend


class CDNCache:
    """Tiny TTL edge-cache model with lazy expiry and an origin-fetch counter."""

    def __init__(self, ttl_seconds: float) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        self.ttl_seconds = ttl_seconds
        self._entries: Dict[str, Tuple[Any, float]] = {}
        self.origin_fetches = 0

    def get(self, key: str, now: float, origin: Callable[[str], Any]) -> Any:
        cached = self._entries.get(key)
        if cached is not None and now < cached[1]:
            return cached[0]
        self.origin_fetches += 1
        value = origin(key)
        self._entries[key] = (value, now + self.ttl_seconds)
        return value

    def invalidate(self, key: str) -> None:
        self._entries.pop(key, None)


class HashShardRouter:
    """Stable hash-based shard routing; changing shard count remaps many keys."""

    def __init__(self, shard_ids: Sequence[str]) -> None:
        if not shard_ids or len(set(shard_ids)) != len(shard_ids):
            raise ValueError("shard_ids must be non-empty and unique")
        self.shard_ids = list(shard_ids)

    def shard_for(self, key: str) -> str:
        return self.shard_ids[_stable_bucket(key, len(self.shard_ids))]


@dataclass(frozen=True)
class VersionedValue:
    value: Any
    version: int


class ReplicaGroup:
    """Primary plus asynchronously copied replicas with read-your-writes fallback."""

    def __init__(self, replica_count: int = 2) -> None:
        if replica_count < 1:
            raise ValueError("replica_count must be >= 1")
        self.primary: Dict[str, VersionedValue] = {}
        self.replicas: List[Dict[str, VersionedValue]] = [
            {} for _ in range(replica_count)
        ]

    def write(self, key: str, value: Any) -> int:
        version = self.primary.get(key, VersionedValue(None, 0)).version + 1
        self.primary[key] = VersionedValue(value, version)
        return version

    def replicate(self, replica_index: int) -> None:
        self.replicas[replica_index] = dict(self.primary)

    def read(self, key: str, replica_index: int = 0, min_version: int = 0) -> Optional[VersionedValue]:
        replica_value = self.replicas[replica_index].get(key)
        if replica_value is not None and replica_value.version >= min_version:
            return replica_value
        primary_value = self.primary.get(key)
        if primary_value is not None and replica_value is not None:
            # Read repair: replace the stale replica entry with the authoritative value.
            self.replicas[replica_index][key] = primary_value
        return primary_value


def cap_choice(partitioned: bool, prefer_availability: bool) -> str:
    """Return the chosen side of the CAP trade-off during a network partition."""
    if not partitioned:
        return "NORMAL_OPERATION"
    return "AP" if prefer_availability else "CP"


def pacelc_choice(partitioned: bool, prefer_availability: bool, prefer_low_latency: bool) -> str:
    """Return a compact PACELC choice label (PA/PC + EL/EC)."""
    if partitioned:
        return "PA" if prefer_availability else "PC"
    return "EL" if prefer_low_latency else "EC"


@dataclass
class VectorClock:
    """Minimal vector clock supporting increment and causal comparison."""

    counters: Dict[str, int]

    def tick(self, node: str) -> None:
        self.counters[node] = self.counters.get(node, 0) + 1

    def compare(self, other: "VectorClock") -> str:
        nodes = set(self.counters) | set(other.counters)
        less = any(self.counters.get(n, 0) < other.counters.get(n, 0) for n in nodes)
        greater = any(self.counters.get(n, 0) > other.counters.get(n, 0) for n in nodes)
        if less and greater:
            return "CONCURRENT"
        if less:
            return "BEFORE"
        if greater:
            return "AFTER"
        return "EQUAL"


@dataclass(frozen=True)
class LogRecord:
    partition: int
    offset: int
    key: str
    value: Any


class PartitionedLog:
    """A tiny partitioned append-only log with consumer-group offsets."""

    def __init__(self, partitions: int) -> None:
        if partitions <= 0:
            raise ValueError("partitions must be > 0")
        self.partitions: List[List[LogRecord]] = [[] for _ in range(partitions)]
        self.group_offsets: Dict[Tuple[str, int], int] = {}

    def append(self, key: str, value: Any) -> LogRecord:
        partition_id = _stable_bucket(key, len(self.partitions))
        records = self.partitions[partition_id]
        record = LogRecord(partition_id, len(records), key, value)
        records.append(record)
        return record

    def poll(self, group: str, partition_id: int, limit: int = 10) -> List[LogRecord]:
        if limit <= 0:
            raise ValueError("limit must be > 0")
        offset = self.group_offsets.get((group, partition_id), 0)
        return self.partitions[partition_id][offset : offset + limit]

    def commit(self, group: str, partition_id: int, next_offset: int) -> None:
        if not 0 <= next_offset <= len(self.partitions[partition_id]):
            raise ValueError("next_offset is outside the partition log")
        current = self.group_offsets.get((group, partition_id), 0)
        if next_offset < current:
            raise ValueError("consumer offsets cannot move backwards")
        self.group_offsets[(group, partition_id)] = next_offset


class ServiceRegistry:
    """Simple in-memory service discovery registry."""

    def __init__(self) -> None:
        self._instances: Dict[str, List[str]] = defaultdict(list)

    def register(self, service: str, address: str) -> None:
        if address not in self._instances[service]:
            self._instances[service].append(address)

    def resolve(self, service: str) -> Tuple[str, ...]:
        return tuple(self._instances.get(service, ()))

    def deregister(self, service: str, address: str) -> None:
        self._instances[service] = [x for x in self._instances[service] if x != address]


class ApiGateway:
    """Minimal route table with an explicit authentication boundary."""

    def __init__(self) -> None:
        self._routes: Dict[str, Tuple[Callable[[Any], Any], bool]] = {}

    def add_route(self, path: str, handler: Callable[[Any], Any], require_auth: bool = True) -> None:
        self._routes[path] = (handler, require_auth)

    def dispatch(self, path: str, payload: Any, authenticated: bool) -> Tuple[int, Any]:
        route = self._routes.get(path)
        if route is None:
            return 404, {"error": "not found"}
        handler, require_auth = route
        if require_auth and not authenticated:
            return 401, {"error": "authentication required"}
        return 200, handler(payload)


@dataclass
class _Upload:
    parts: Dict[int, bytes]


class MultipartObjectStore:
    """In-memory multipart upload model with ordered assembly and checksum validation."""

    def __init__(self) -> None:
        self._uploads: Dict[str, _Upload] = {}
        self.objects: Dict[str, bytes] = {}

    def begin(self) -> str:
        upload_id = str(uuid.uuid4())
        self._uploads[upload_id] = _Upload(parts={})
        return upload_id

    def upload_part(self, upload_id: str, part_number: int, data: bytes) -> str:
        if part_number <= 0:
            raise ValueError("part_number must be positive")
        if upload_id not in self._uploads:
            raise KeyError("unknown upload_id")
        self._uploads[upload_id].parts[part_number] = bytes(data)
        return sha256(data).hexdigest()

    def complete(self, upload_id: str, object_key: str, expected_checksums: Dict[int, str]) -> bytes:
        upload = self._uploads.get(upload_id)
        if upload is None:
            raise KeyError("unknown upload_id")
        if not expected_checksums or set(expected_checksums) != set(upload.parts):
            raise ValueError("uploaded parts do not match the completion manifest")
        for number, data in upload.parts.items():
            if sha256(data).hexdigest() != expected_checksums[number]:
                raise ValueError(f"checksum mismatch for part {number}")
        result = b"".join(upload.parts[n] for n in sorted(upload.parts))
        self.objects[object_key] = result
        del self._uploads[upload_id]
        return result


def estimate_capacity(daily_active_users: int, requests_per_user: float, peak_factor: float, average_object_bytes: int) -> Dict[str, float]:
    """Return transparent first-pass peak RPS and daily storage estimates."""
    if min(daily_active_users, requests_per_user, peak_factor, average_object_bytes) < 0:
        raise ValueError("estimation inputs cannot be negative")
    daily_requests = daily_active_users * requests_per_user
    average_rps = daily_requests / 86_400
    return {
        "daily_requests": daily_requests,
        "average_rps": average_rps,
        "peak_rps": average_rps * peak_factor,
        "daily_storage_bytes": daily_requests * average_object_bytes,
    }


class GraphANNIndex:
    """Small single-layer graph ANN teaching model; this is not a full HNSW implementation."""

    def __init__(self, max_neighbors: int = 3) -> None:
        if max_neighbors <= 0:
            raise ValueError("max_neighbors must be > 0")
        self.max_neighbors = max_neighbors
        self.vectors: Dict[str, Tuple[float, ...]] = {}
        self.edges: Dict[str, set[str]] = defaultdict(set)

    @staticmethod
    def _distance(a: Sequence[float], b: Sequence[float]) -> float:
        if len(a) != len(b):
            raise ValueError("vector dimensions must match")
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

    def add(self, item_id: str, vector: Sequence[float]) -> None:
        values = tuple(float(x) for x in vector)
        if not values:
            raise ValueError("vector cannot be empty")
        self.vectors[item_id] = values
        self.edges[item_id] = set()
        others = sorted(
            (self._distance(values, other), other_id)
            for other_id, other in self.vectors.items()
            if other_id != item_id
        )[: self.max_neighbors]
        for _, other_id in others:
            self.edges[item_id].add(other_id)
            self.edges[other_id].add(item_id)

    def search(self, query: Sequence[float], entry_id: str, ef: int = 10) -> List[Tuple[str, float]]:
        if entry_id not in self.vectors:
            raise KeyError(entry_id)
        if ef <= 0:
            raise ValueError("ef must be > 0")
        visited = {entry_id}
        frontier = [entry_id]
        while frontier and len(visited) < ef:
            current = min(frontier, key=lambda item: self._distance(query, self.vectors[item]))
            frontier.remove(current)
            for neighbor in self.edges[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    frontier.append(neighbor)
        ranked = sorted(
            ((item, self._distance(query, self.vectors[item])) for item in visited),
            key=lambda pair: pair[1],
        )
        return ranked[:ef]


class RaftElection:
    """Single-term Raft election teaching model with one vote per node per term."""

    def __init__(self, nodes: Sequence[str]) -> None:
        if len(nodes) < 1 or len(set(nodes)) != len(nodes):
            raise ValueError("nodes must be non-empty and unique")
        self.nodes = set(nodes)
        self.current_term = 0
        self.voted_for: Dict[str, Tuple[int, str]] = {}
        self.leader: Optional[str] = None

    def elect(self, candidate: str, term: int, votes: Iterable[str]) -> bool:
        if candidate not in self.nodes or term < self.current_term:
            return False
        if term > self.current_term:
            self.current_term = term
            self.voted_for = {node: vote for node, vote in self.voted_for.items() if vote[0] >= term}
            self.leader = None
        granted = set()
        for voter in votes:
            if voter not in self.nodes:
                continue
            previous = self.voted_for.get(voter)
            if previous is None or previous == (term, candidate):
                self.voted_for[voter] = (term, candidate)
                granted.add(voter)
        if candidate in granted and len(granted) > len(self.nodes) // 2:
            self.leader = candidate
            return True
        return False


class TumblingWindowAggregator:
    """Event-time tumbling windows; events older than the watermark are counted as late."""

    def __init__(self, window_seconds: int) -> None:
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.window_seconds = window_seconds
        self.watermark = float("-inf")
        self.windows: Dict[int, int] = defaultdict(int)
        self.late_events = 0

    def add(self, event_time: float, value: int = 1) -> bool:
        if event_time < self.watermark:
            self.late_events += 1
            return False
        start = floor(event_time / self.window_seconds) * self.window_seconds
        self.windows[start] += value
        return True

    def advance_watermark(self, watermark: float) -> Dict[int, int]:
        if watermark < self.watermark:
            raise ValueError("watermark cannot move backwards")
        self.watermark = watermark
        closed = {
            start: total
            for start, total in self.windows.items()
            if start + self.window_seconds <= watermark
        }
        for start in closed:
            del self.windows[start]
        return dict(sorted(closed.items()))


class LSMStore:
    """Tiny memtable/SSTable model to demonstrate flush, lookup and compaction."""

    def __init__(self) -> None:
        self.memtable: Dict[str, Any] = {}
        self.sstables: List[Dict[str, Any]] = []  # newest first

    def put(self, key: str, value: Any) -> None:
        self.memtable[key] = value

    def flush(self) -> None:
        if self.memtable:
            self.sstables.insert(0, dict(self.memtable))
            self.memtable.clear()

    def get(self, key: str) -> Any:
        if key in self.memtable:
            return self.memtable[key]
        for table in self.sstables:
            if key in table:
                return table[key]
        return None

    def compact(self) -> None:
        merged: Dict[str, Any] = {}
        for table in reversed(self.sstables):
            merged.update(table)
        merged.update(self.memtable)
        self.memtable.clear()
        self.sstables = [merged] if merged else []


class PresenceRegistry:
    """TTL-based chat presence model."""

    def __init__(self) -> None:
        self._last_seen: Dict[str, float] = {}

    def heartbeat(self, user_id: str, now: float) -> None:
        self._last_seen[user_id] = now

    def is_online(self, user_id: str, now: float, ttl_seconds: float) -> bool:
        last_seen = self._last_seen.get(user_id)
        return last_seen is not None and now - last_seen < ttl_seconds


class DriverCellIndex:
    """Coarse grid cell index for nearby-driver candidate retrieval."""

    def __init__(self, cell_size_degrees: float = 0.01) -> None:
        if cell_size_degrees <= 0:
            raise ValueError("cell_size_degrees must be > 0")
        self.cell_size = cell_size_degrees
        self.cells: Dict[Tuple[int, int], set[str]] = defaultdict(set)

    def cell_for(self, latitude: float, longitude: float) -> Tuple[int, int]:
        return (floor(latitude / self.cell_size), floor(longitude / self.cell_size))

    def add_driver(self, driver_id: str, latitude: float, longitude: float) -> None:
        self.cells[self.cell_for(latitude, longitude)].add(driver_id)

    def candidates(self, latitude: float, longitude: float, neighboring_cells: int = 1) -> set[str]:
        row, col = self.cell_for(latitude, longitude)
        return {
            driver
            for r in range(row - neighboring_cells, row + neighboring_cells + 1)
            for c in range(col - neighboring_cells, col + neighboring_cells + 1)
            for driver in self.cells.get((r, c), set())
        }
