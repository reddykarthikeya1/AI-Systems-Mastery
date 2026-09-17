"""Module 24 Test Suite: Production DBRE, PITR & Zero-Downtime Migrations."""

from __future__ import annotations

import pytest
from dbre_engine import (
    ConnectionPoolExhaustedError,
    ContinuousWALArchiver,
    ExpandContractMigrator,
    PITRRecoveryEngine,
    TransactionConnectionPooler,
)


def test_continuous_wal_archiving() -> None:
    archiver = ContinuousWALArchiver()
    r1 = archiver.append("INSERT", "users", "u1", {"name": "Alice"}, timestamp_us=100)
    r2 = archiver.append("UPDATE", "users", "u1", {"name": "Alice Smith"}, timestamp_us=150)
    r3 = archiver.append("DELETE", "users", "u1", {}, timestamp_us=200)

    assert len(archiver.records) == 3
    assert r1.lsn == 1
    assert r2.lsn == 2
    assert r3.lsn == 3
    assert r2.timestamp_us == 150


def test_pitr_recovery_prevents_accidental_drop_table() -> None:
    engine = PITRRecoveryEngine()

    # Initial state at t=1000
    initial_db = {
        "accounts": {
            "a1": {"owner": "Alice", "balance": 100},
            "a2": {"owner": "Bob", "balance": 200},
        }
    }
    backup_id = engine.take_base_backup(initial_db, timestamp_us=1000)

    # WAL stream
    archiver = ContinuousWALArchiver()
    archiver.append("INSERT", "accounts", "a3", {"owner": "Carol", "balance": 300}, timestamp_us=1010)
    archiver.append("UPDATE", "accounts", "a1", {"owner": "Alice", "balance": 500}, timestamp_us=1020)
    # Disaster at t=1030!
    archiver.append("DROP_TABLE", "accounts", "", {}, timestamp_us=1030)

    # Execute PITR to t=1025 (safely before DROP_TABLE)
    restored = engine.restore_to_timestamp(backup_id, target_timestamp_us=1025, wal_stream=archiver.records)

    assert "accounts" in restored
    assert len(restored["accounts"]) == 3
    assert restored["accounts"]["a1"]["balance"] == 500
    assert restored["accounts"]["a3"]["owner"] == "Carol"


def test_expand_contract_migration_full_lifecycle() -> None:
    table = [
        {"id": 1, "phone": "555-0100"},
        {"id": 2, "phone": "555-0200"},
    ]

    # Phase 1: Expand (Add new nullable column)
    ExpandContractMigrator.expand_add_column(table, "mobile_number")
    assert table[0]["mobile_number"] is None
    assert table[1]["mobile_number"] is None

    # Phase 2: Dual-write new incoming row
    ExpandContractMigrator.dual_write_insert(
        table, {"id": 3, "phone": "555-0300"}, old_col="phone", new_col="mobile_number"
    )
    assert len(table) == 3
    assert table[2]["phone"] == "555-0300"
    assert table[2]["mobile_number"] == "555-0300"

    # Phase 3: Backfill historical rows
    updated = ExpandContractMigrator.backfill_batch(table, old_col="phone", new_col="mobile_number", batch_size=5)
    assert updated == 2
    assert table[0]["mobile_number"] == "555-0100"
    assert table[1]["mobile_number"] == "555-0200"

    # Phase 5: Contract (Drop old column)
    ExpandContractMigrator.contract_drop_column(table, "phone")
    for r in table:
        assert "phone" not in r
        assert "mobile_number" in r


def test_transaction_connection_pooler_limits() -> None:
    pool = TransactionConnectionPooler(max_connections=2)

    c1 = pool.acquire()
    _ = pool.acquire()
    assert len(pool.in_use_connections) == 2

    # Attempting to acquire when full raises ConnectionPoolExhaustedError
    with pytest.raises(ConnectionPoolExhaustedError):
        pool.acquire()

    # Release connection 1
    pool.release(c1)
    assert len(pool.in_use_connections) == 1

    # Now acquire succeeds
    c3 = pool.acquire()
    assert c3 == c1
