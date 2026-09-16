"""Module 04: PostgreSQL JSONB Document & Range Store Engine Reference Solution.

Implements:
1. Binary JSONB document storage with sorted keys and normalized formatting.
2. GIN-style inverted index over nested paths and scalar values for rapid containment (@>).
3. TOAST compression and chunking mechanism for attributes exceeding 2048 bytes.
4. Range exclusion index enforcing zero overlaps for time intervals (simulating GiST exclusion).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any
import uuid
import zlib


@dataclass(frozen=True)
class ToastPointer:
    toast_oid: str
    chunk_count: int
    raw_size_bytes: int
    compressed_size_bytes: int


@dataclass(frozen=True)
class TimeRange:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError(f"Invalid range: start ({self.start}) must precede end ({self.end})")

    def overlaps(self, other: TimeRange) -> bool:
        """Returns True if this range overlaps with other range [start, end)."""
        return self.start < other.end and self.end > other.start


class JSONBDocumentStore:
    """Simulates PostgreSQL JSONB binary storage, GIN inverted indexing, and TOAST compression."""

    def __init__(self, toast_threshold_bytes: int = 2048, toast_chunk_size: int = 2000) -> None:
        self.toast_threshold_bytes = toast_threshold_bytes
        self.toast_chunk_size = toast_chunk_size
        self._documents: dict[str, dict[str, Any] | ToastPointer] = {}
        self._toast_chunks: dict[str, list[bytes]] = {}
        self._gin_inverted_index: dict[str, set[str]] = {}  # "path:val" -> {doc_id, ...}

    def _extract_gin_entries(self, obj: Any, prefix: str = "") -> list[str]:
        """Recursively decomposes JSON object into GIN index key paths (jsonb_path_ops style)."""
        entries = []
        if isinstance(obj, dict):
            for k, v in sorted(obj.items()):
                path = f"{prefix}.{k}" if prefix else k
                if isinstance(v, (dict, list)):
                    entries.extend(self._extract_gin_entries(v, path))
                else:
                    entries.append(f"{path}:{json.dumps(v)}")
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    entries.extend(self._extract_gin_entries(item, prefix))
                else:
                    entries.append(f"{prefix}[]:{json.dumps(item)}")
        else:
            entries.append(f"{prefix}:{json.dumps(obj)}")
        return entries

    def insert(self, doc_id: str, document: dict[str, Any]) -> None:
        """Stores document, updates GIN inverted index, and triggers TOAST if size exceeds threshold."""
        # Serialize with sorted keys (PostgreSQL JSONB normalizes key order)
        raw_bytes = json.dumps(document, sort_keys=True).encode("utf-8")

        # Update GIN inverted index
        entries = self._extract_gin_entries(document)
        for entry in entries:
            if entry not in self._gin_inverted_index:
                self._gin_inverted_index[entry] = set()
            self._gin_inverted_index[entry].add(doc_id)

        # Evaluate TOAST threshold
        if len(raw_bytes) > self.toast_threshold_bytes:
            compressed = zlib.compress(raw_bytes, level=6)
            chunks = [
                compressed[i : i + self.toast_chunk_size]
                for i in range(0, len(compressed), self.toast_chunk_size)
            ]
            toast_oid = f"toast_{uuid.uuid4().hex[:8]}"
            self._toast_chunks[toast_oid] = chunks
            self._documents[doc_id] = ToastPointer(
                toast_oid=toast_oid,
                chunk_count=len(chunks),
                raw_size_bytes=len(raw_bytes),
                compressed_size_bytes=len(compressed),
            )
        else:
            # Inline storage in table page
            self._documents[doc_id] = document

    def get(self, doc_id: str) -> dict[str, Any]:
        """Retrieves document, decompressing and reassembling from TOAST chunks if necessary."""
        if doc_id not in self._documents:
            raise KeyError(f"Document with id '{doc_id}' not found.")

        stored = self._documents[doc_id]
        if isinstance(stored, ToastPointer):
            chunks = self._toast_chunks[stored.toast_oid]
            compressed = b"".join(chunks)
            raw_bytes = zlib.decompress(compressed)
            return json.loads(raw_bytes.decode("utf-8"))
        return stored

    def is_toasted(self, doc_id: str) -> bool:
        """Returns True if document was stored out-of-line in TOAST table."""
        return isinstance(self._documents.get(doc_id), ToastPointer)

    def contains(self, sub_document: dict[str, Any]) -> list[str]:
        """Simulates the PostgreSQL @> containment operator using the GIN inverted index.

        Returns list of doc_ids matching all paths and values in sub_document.
        """
        required_entries = self._extract_gin_entries(sub_document)
        if not required_entries:
            return list(self._documents.keys())

        # Intersect matching doc sets across all required entries
        candidate_sets: list[set[str]] = []
        for entry in required_entries:
            matching_docs = self._gin_inverted_index.get(entry, set())
            candidate_sets.append(matching_docs)

        if not candidate_sets:
            return []

        result_set = set.intersection(*candidate_sets)
        return sorted(result_set)


class RangeExclusionIndex:
    """Simulates PostgreSQL GiST exclusion constraints on temporal ranges."""

    def __init__(self) -> None:
        self._reservations: dict[str, list[tuple[str, TimeRange]]] = {}

    def add_reservation(self, resource_id: str, booking_id: str, time_range: TimeRange) -> None:
        """Adds a reservation, raising ValueError if an overlapping reservation exists for resource_id."""
        if resource_id not in self._reservations:
            self._reservations[resource_id] = []

        existing = self._reservations[resource_id]
        for existing_id, existing_range in existing:
            if time_range.overlaps(existing_range):
                raise ValueError(
                    f"Exclusion constraint violation: booking '{booking_id}' overlaps with "
                    f"existing booking '{existing_id}' [{existing_range.start} - {existing_range.end}] "
                    f"on resource '{resource_id}'."
                )

        self._reservations[resource_id].append((booking_id, time_range))

    def get_reservations(self, resource_id: str) -> list[tuple[str, TimeRange]]:
        return list(self._reservations.get(resource_id, []))
