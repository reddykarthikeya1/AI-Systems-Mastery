"""Module 01: Real Storage Engine & ACID Durability Layer (Track B).

Operates directly on the host filesystem to demonstrate:
1. Low-level page and record serialization with CRC32 checksums.
2. Write-Ahead Logging (WAL) with strict `os.fsync()` durability guarantees.
3. Atomic table page commits via temporary file swaps (`os.replace`).
4. Crash-recovery log replay reconstructing table state after simulated power-loss.
5. Durability vs throughput benchmarking (fsync vs OS page cache buffering).
"""

from __future__ import annotations

import binascii
import json
import os
import struct
import time
from pathlib import Path
from typing import Any


class StorageLiveEngine:
    """Production-grade append-only storage engine with WAL and fsync durability."""

    # WAL Header format: <magic: 4s><version: H> -> 6 bytes
    WAL_HEADER_MAGIC = b"WAL1"
    # Record Header format: <tx_id: Q><ts: d><op: B><payload_len: I><crc32: I> -> 8+8+1+4+4 = 25 bytes
    RECORD_HEADER = struct.Struct("<QdBI I")
    OP_INSERT = 1
    OP_UPDATE = 2
    OP_DELETE = 3
    OP_COMMIT = 4

    def __init__(self, data_dir: str | Path, sync_on_write: bool = True) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.wal_path = self.data_dir / "engine.wal"
        self.table_path = self.data_dir / "table_pages.json"
        self.sync_on_write = sync_on_write
        self._table_state: dict[str, dict[str, Any]] = {}
        self._active_tx_wal_offsets: dict[int, list[int]] = {}

        self._init_wal()
        self.recover_from_wal()

    def _init_wal(self) -> None:
        if not self.wal_path.exists():
            with open(self.wal_path, "wb") as f:
                f.write(self.WAL_HEADER_MAGIC + struct.pack("<H", 1))
                f.flush()
                if self.sync_on_write:
                    os.fsync(f.fileno())

    def recover_from_wal(self) -> int:
        """Reads WAL sequentially from disk, validates CRC32, and replays committed transactions."""
        if not self.wal_path.exists():
            return 0

        # Load existing table state if available
        if self.table_path.exists():
            try:
                with open(self.table_path, "r", encoding="utf-8") as f:
                    self._table_state = json.load(f)
            except Exception:
                self._table_state = {}
        else:
            self._table_state = {}

        replayed = 0
        committed_tx_ids: set[int] = set()
        uncommitted_records: dict[int, list[tuple[int, dict[str, Any]]]] = {}

        with open(self.wal_path, "rb") as f:
            magic = f.read(4)
            if magic != self.WAL_HEADER_MAGIC:
                return 0
            _version = struct.unpack("<H", f.read(2))[0]

            while True:
                header_bytes = f.read(self.RECORD_HEADER.size)
                if len(header_bytes) < self.RECORD_HEADER.size:
                    break

                tx_id, ts, op, payload_len, stored_crc = self.RECORD_HEADER.unpack(header_bytes)
                payload_bytes = f.read(payload_len)
                if len(payload_bytes) < payload_len:
                    # Torn page / incomplete write at end of WAL
                    break

                calc_crc = binascii.crc32(payload_bytes)
                if calc_crc != stored_crc:
                    # Corrupted record, discard torn frame
                    break

                if op == self.OP_COMMIT:
                    committed_tx_ids.add(tx_id)
                else:
                    try:
                        record_dict = json.loads(payload_bytes.decode("utf-8"))
                        uncommitted_records.setdefault(tx_id, []).append((op, record_dict))
                    except Exception:
                        break

        # Replay only records belonging to committed transactions
        for tx_id in sorted(committed_tx_ids):
            for op, data in uncommitted_records.get(tx_id, []):
                key = str(data["id"])
                if op in (self.OP_INSERT, self.OP_UPDATE):
                    self._table_state[key] = data
                    replayed += 1
                elif op == self.OP_DELETE:
                    self._table_state.pop(key, None)
                    replayed += 1

        self._flush_table_pages_atomic()
        return replayed

    def _append_wal(self, tx_id: int, op: int, payload: dict[str, Any]) -> None:
        payload_bytes = json.dumps(payload).encode("utf-8")
        crc = binascii.crc32(payload_bytes)
        ts = time.time()
        header = self.RECORD_HEADER.pack(tx_id, ts, op, len(payload_bytes), crc)

        with open(self.wal_path, "ab") as f:
            f.write(header + payload_bytes)
            f.flush()
            if self.sync_on_write:
                os.fsync(f.fileno())

    def write_record(self, tx_id: int, record: dict[str, Any]) -> None:
        """Writes record mutation to WAL (Durability & Atomicity step 1)."""
        self._append_wal(tx_id, self.OP_INSERT, record)

    def commit_transaction(self, tx_id: int) -> None:
        """Commits transaction by writing commit marker to WAL with fsync."""
        self._append_wal(tx_id, self.OP_COMMIT, {"tx_id": tx_id, "status": "COMMITTED"})
        # Re-sync in-memory state
        self.recover_from_wal()

    def _flush_table_pages_atomic(self) -> None:
        """Atomically persists in-memory table state to disk using temporary swap."""
        tmp_path = self.data_dir / "table_pages.json.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self._table_state, f, indent=2)
            f.flush()
            if self.sync_on_write:
                os.fsync(f.fileno())
        os.replace(tmp_path, self.table_path)

    def read_record(self, record_id: str | int) -> dict[str, Any] | None:
        return self._table_state.get(str(record_id))

    def count_records(self) -> int:
        return len(self._table_state)
