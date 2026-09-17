"""Automated pytest test suite for Module 05 PostgreSQL MVCC & EXPLAIN Engine."""

import pytest
from mvcc_engine import MVCCTable, QueryCostEstimator, Snapshot


@pytest.fixture
def mvcc_table() -> MVCCTable:
    tbl = MVCCTable("accounts")
    # Insert Alice (XID 100) and Bob (XID 100)
    tbl.insert("acc_1", {"name": "Alice", "balance": 100}, xid=100)
    tbl.insert("acc_2", {"name": "Bob", "balance": 200}, xid=100)
    return tbl


def test_initial_insert_and_visibility(mvcc_table: MVCCTable) -> None:
    # Snapshot at XID 105: Sees committed transactions < 105
    snap = Snapshot(snapshot_xid=105, xmin=100, xmax=106, active_xids=set())
    rows = mvcc_table.select(snap)
    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    assert rows[0]["balance"] == 100


def test_mvcc_update_creates_version_chain_without_overwriting(mvcc_table: MVCCTable) -> None:
    # Update Alice's balance to 150 at XID 110
    success = mvcc_table.update("acc_1", {"name": "Alice", "balance": 150}, xid=110)
    assert success is True

    # Total physical tuples in table is now 3 (2 for Alice, 1 for Bob)
    assert len(mvcc_table.tuples) == 3

    # Original Alice tuple has xmin=100, xmax=110
    v1 = mvcc_table.tuples[0]
    assert v1.xmin == 100 and v1.xmax == 110

    # New Alice tuple has xmin=110, xmax=0
    v2 = mvcc_table.tuples[2]
    assert v2.xmin == 110 and v2.xmax == 0


def test_snapshot_isolation_sees_consistent_past_state(mvcc_table: MVCCTable) -> None:
    # Tx 110 updates Alice
    mvcc_table.update("acc_1", {"name": "Alice", "balance": 150}, xid=110)

    # Snapshot for an ongoing transaction Tx 105 (started before Tx 110)
    old_snap = Snapshot(snapshot_xid=105, xmin=100, xmax=106, active_xids=set())
    rows_old = mvcc_table.select(old_snap)
    alice_old = next(r for r in rows_old if r["name"] == "Alice")
    assert alice_old["balance"] == 100  # Sees version 1!

    # Snapshot for a new transaction Tx 115 (started after Tx 110 committed)
    new_snap = Snapshot(snapshot_xid=115, xmin=111, xmax=116, active_xids=set())
    rows_new = mvcc_table.select(new_snap)
    alice_new = next(r for r in rows_new if r["name"] == "Alice")
    assert alice_new["balance"] == 150  # Sees version 2!


def test_delete_marks_tuple_dead(mvcc_table: MVCCTable) -> None:
    # Delete Bob at XID 120
    assert mvcc_table.delete("acc_2", xid=120) is True

    # Snapshot before delete sees Bob
    snap_before = Snapshot(snapshot_xid=115, xmin=110, xmax=116, active_xids=set())
    assert len(mvcc_table.select(snap_before)) == 2

    # Snapshot after delete sees only Alice
    snap_after = Snapshot(snapshot_xid=125, xmin=121, xmax=126, active_xids=set())
    rows_after = mvcc_table.select(snap_after)
    assert len(rows_after) == 1
    assert rows_after[0]["name"] == "Alice"


def test_vacuum_purges_dead_tuples_when_safe(mvcc_table: MVCCTable) -> None:
    # Update Alice at XID 110 and Delete Bob at XID 120
    mvcc_table.update("acc_1", {"name": "Alice", "balance": 150}, xid=110)
    mvcc_table.delete("acc_2", xid=120)

    # Currently 3 tuples in table
    assert len(mvcc_table.tuples) == 3

    # Vacuum with oldest_active_xid = 105:
    # Both dead tuples have xmax > 105, so VACUUM CANNOT reclaim them (active transaction might still need them)
    reclaimed = mvcc_table.vacuum(oldest_active_xid=105)
    assert reclaimed == 0
    assert len(mvcc_table.tuples) == 3

    # Now all transactions have caught up (oldest_active_xid = 125):
    # Old Alice (xmax=110) and Bob (xmax=120) are both safely purged!
    reclaimed = mvcc_table.vacuum(oldest_active_xid=125)
    assert reclaimed == 2
    assert len(mvcc_table.tuples) == 1
    assert mvcc_table.tuples[0].data["name"] == "Alice"
    assert mvcc_table.tuples[0].data["balance"] == 150


def test_cost_estimator_crossover_point() -> None:
    estimator = QueryCostEstimator()
    table_pages = 5_000
    total_tuples = 500_000

    # 1. Very selective query (0.01% of rows match): Index Scan should win decisively
    plan_selective = estimator.select_cheapest_plan(table_pages, total_tuples, selectivity=0.0001)
    assert plan_selective == "Index Scan"

    # 2. Unselective query (30% of rows match): Seq Scan should win decisively
    plan_broad = estimator.select_cheapest_plan(table_pages, total_tuples, selectivity=0.30)
    assert plan_broad == "Seq Scan"
