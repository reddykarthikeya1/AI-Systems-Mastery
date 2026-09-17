"""Tests for Module 01 Real Storage Engine (Track B)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from storage_live import StorageLiveEngine


def test_storage_live_write_and_commit() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = StorageLiveEngine(tmpdir, sync_on_write=True)
        tx1 = 101
        engine.write_record(tx1, {"id": 1, "name": "Alice", "balance": 500.0})
        engine.write_record(tx1, {"id": 2, "name": "Bob", "balance": 750.0})

        # Before commit, read should still be empty in persistent table
        assert engine.read_record(1) is None
        assert engine.count_records() == 0

        # Commit transaction
        engine.commit_transaction(tx1)

        assert engine.count_records() == 2
        r1 = engine.read_record(1)
        assert r1 is not None
        assert r1["name"] == "Alice"
        assert r1["balance"] == 500.0


def test_storage_live_crash_recovery_atomicity() -> None:
    """Simulates power-cut / crash where tx2 committed, but tx3 only wrote partially without commit."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine1 = StorageLiveEngine(tmpdir, sync_on_write=True)
        # Tx 1: Committed
        engine1.write_record(1, {"id": "acc_1", "user": "Charlie", "credits": 100})
        engine1.commit_transaction(1)

        # Tx 2: Uncommitted crash simulation
        engine1.write_record(2, {"id": "acc_2", "user": "Eve", "credits": 999999})
        # Simulate abrupt kill without commit_transaction(2)

        # Reopen engine in same data_dir (simulating recovery upon reboot)
        engine_restarted = StorageLiveEngine(tmpdir, sync_on_write=True)

        # Tx 1 must survive (Durability)
        assert engine_restarted.read_record("acc_1") is not None
        # Tx 2 must NOT be present (Atomicity rollback of uncommitted work)
        assert engine_restarted.read_record("acc_2") is None
        assert engine_restarted.count_records() == 1


def test_storage_live_crc_corruption_detection() -> None:
    """Verifies that corrupted WAL tail bytes are detected and discarded cleanly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = StorageLiveEngine(tmpdir, sync_on_write=True)
        engine.write_record(1, {"id": "k1", "val": "legitimate"})
        engine.commit_transaction(1)

        # Append garbage bytes to the WAL
        wal_file = Path(tmpdir) / "engine.wal"
        with open(wal_file, "ab") as f:
            f.write(b"\xde\xad\xbe\xef\x00\x00\x00\x01garbled_packet_corrupt")

        # Restart engine and verify recovery isolates corruption
        engine_recovery = StorageLiveEngine(tmpdir, sync_on_write=True)
        assert engine_recovery.read_record("k1") == {"id": "k1", "val": "legitimate"}
