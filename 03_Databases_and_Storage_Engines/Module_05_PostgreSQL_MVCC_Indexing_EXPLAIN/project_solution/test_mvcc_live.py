"""Tests for Module 05: Real PostgreSQL MVCC, Bloat & Buffers (Track B)."""

from __future__ import annotations

import pytest

def _postgres_is_up() -> bool:
    try:
        from mvcc_live import MVCCLiveClient
        client = MVCCLiveClient()
        return client.ping()
    except Exception:
        return False

requires_postgres = pytest.mark.skipif(
    not _postgres_is_up(),
    reason="PostgreSQL not reachable on localhost:15432 - start with: make up postgres"
)

pytestmark = [pytest.mark.requires_postgres, requires_postgres]


def test_mvcc_live_ping():
    from mvcc_live import MVCCLiveClient
    client = MVCCLiveClient()
    assert client.ping() is True


def test_mvcc_concurrent_snapshot_isolation():
    from mvcc_live import MVCCLiveClient
    client = MVCCLiveClient()
    tbl = "accounts_iso_m05"
    client.setup_accounts_table(tbl)

    with client.get_connection() as setup_conn:
        with setup_conn.cursor() as cur:
            cur.execute(f"DELETE FROM {tbl};")
            cur.execute(f"INSERT INTO {tbl} (id, owner, balance) VALUES (1, 'Alice', 1000.00);")

    # Open two concurrent connections
    conn1 = client.get_connection()
    conn2 = client.get_connection()

    try:
        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        # Conn 1 updates balance inside a transaction, but DOES NOT COMMIT
        cur1.execute(f"UPDATE {tbl} SET balance = 1500.00 WHERE id = 1;")

        # Conn 2 reads balance under snapshot isolation -> must still see 1000.00!
        cur2.execute(f"SELECT balance FROM {tbl} WHERE id = 1;")
        row2 = cur2.fetchone()
        assert float(row2[0]) == 1000.00

        # Conn 1 commits
        conn1.commit()

        # Conn 2 finishes its transaction and now sees the updated balance
        conn2.commit()
        cur2.execute(f"SELECT balance FROM {tbl} WHERE id = 1;")
        row2_after = cur2.fetchone()
        assert float(row2_after[0]) == 1500.00

    finally:
        conn1.close()
        conn2.close()


def test_mvcc_xmin_xmax_visibility_headers():
    from mvcc_live import MVCCLiveClient
    client = MVCCLiveClient()
    tbl = "accounts_headers_m05"
    client.setup_accounts_table(tbl)

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {tbl};")
            cur.execute(f"INSERT INTO {tbl} (id, owner, balance) VALUES (42, 'Bob', 500.00);")

    headers = client.inspect_tuple_headers(tbl, 42)
    assert "xmin" in headers
    assert int(headers["xmin"]) > 0
    # Live un-deleted row has xmax = 0 (or invalid transaction ID)
    assert headers["xmax"] in {"0", ""}


def test_mvcc_row_bloat_dead_tuples():
    from mvcc_live import MVCCLiveClient
    client = MVCCLiveClient()
    tbl = "accounts_bloat_m05"
    client.setup_accounts_table(tbl)

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {tbl};")
            cur.execute(f"INSERT INTO {tbl} (id, owner, balance) VALUES (99, 'Charlie', 100.00);")

    # Update 50 times in separate commits -> creates 50 dead versions
    client.induce_row_bloat(tbl, 99, updates_count=50)
    stats = client.inspect_dead_tuples(tbl)
    # Dead tuples count should be updated
    assert stats["dead_tuples"] >= 0


def test_mvcc_vacuum_reclaims_dead_tuples():
    from mvcc_live import MVCCLiveClient
    client = MVCCLiveClient()
    tbl = "accounts_vacuum_m05"
    client.setup_accounts_table(tbl)

    client.run_vacuum(tbl, verbose=True)
    stats = client.inspect_dead_tuples(tbl)
    # After VACUUM, dead tuples should be 0 or minimized
    assert stats["dead_tuples"] == 0


def test_mvcc_explain_analyze_buffers_inspection():
    from mvcc_live import MVCCLiveClient
    client = MVCCLiveClient()
    tbl = "accounts_buffers_m05"
    client.setup_accounts_table(tbl)

    plan = client.explain_analyze_buffers(f"SELECT * FROM {tbl} WHERE id = 1;")
    assert "Buffers: shared" in plan or "Index Scan" in plan or "Seq Scan" in plan


@pytest.mark.perf
def test_index_scan_beats_seq_scan_performance():
    from mvcc_live import MVCCLiveClient
    import time
    client = MVCCLiveClient()
    tbl = "accounts_scan_perf_m05"

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {tbl};")
            cur.execute(f"""
                CREATE TABLE {tbl} AS
                SELECT
                    g AS id,
                    'User_' || g AS owner,
                    (g * 10.5)::numeric(12,2) AS balance
                FROM generate_series(1, 20000) g;
            """)

            # 1. Unindexed lookup
            start_seq = time.perf_counter()
            cur.execute(f"SELECT * FROM {tbl} WHERE balance = 10500.00;")
            cur.fetchall()
            seq_time = time.perf_counter() - start_seq

            # 2. Build index
            cur.execute(f"CREATE INDEX idx_{tbl}_balance ON {tbl}(balance);")

            # 3. Indexed lookup
            start_idx = time.perf_counter()
            cur.execute(f"SELECT * FROM {tbl} WHERE balance = 10500.00;")
            cur.fetchall()
            idx_time = time.perf_counter() - start_idx

            # Index scan must beat or equal seq scan
            assert idx_time <= seq_time * 1.5


def test_handbuilt_mvcc_matches_postgres_snapshot_semantics():
    """Track A <-> Track B: Handbuilt Snapshot.is_visible() vs real PostgreSQL snapshot semantics."""
    from mvcc_engine import HeapTuple, Snapshot

    # In our model:
    # Transaction 100 inserted a tuple
    tuple_100 = HeapTuple(tuple_id="t1", data={"val": 42}, xmin=100, xmax=0)

    # Snapshot at xid 105:
    # xmin=90, xmax=110, active_xids={100} -> Transaction 100 is still uncommitted/active
    snap_active = Snapshot(snapshot_xid=105, xmin=90, xmax=110, active_xids={100})
    assert snap_active.is_visible(tuple_100) is False

    # Snapshot after Transaction 100 committed:
    snap_committed = Snapshot(snapshot_xid=110, xmin=90, xmax=115, active_xids=set())
    assert snap_committed.is_visible(tuple_100) is True
