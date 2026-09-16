"""Tests for Module 24: Production DBRE Migrations, Backups & HA (Track B)."""

from __future__ import annotations

import pytest

def _postgres_is_up() -> bool:
    try:
        from dbre_live import DBRELiveClient
        client = DBRELiveClient()
        return client.ping()
    except Exception:
        return False

requires_postgres = pytest.mark.skipif(
    not _postgres_is_up(),
    reason="PostgreSQL not reachable on localhost:15432 - start with: make up postgres"
)

pytestmark = [pytest.mark.requires_postgres, requires_postgres]


def test_dbre_live_ping():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    assert client.ping() is True


def test_zero_downtime_expand_contract_migration():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    tbl = "dbre_users_migration_test"

    client.setup_customer_table(tbl)
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO {tbl} (full_name) VALUES ('Grace Hopper'), ('Alan Turing');")

    # Execute 5-phase zero-downtime migration
    phases = client.execute_expand_contract_migration(tbl)
    assert phases["phase_1_expand"] == "SUCCESS"
    assert phases["phase_2_trigger"] == "SUCCESS"
    assert phases["phase_3_backfill"] == "SUCCESS"
    assert phases["phase_4_contract"] == "SUCCESS"

    # Verify data is successfully split without data loss
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT first_name, last_name FROM {tbl} ORDER BY id;")
            rows = cur.fetchall()
            assert rows[0] == ("Grace", "Hopper")
            assert rows[1] == ("Alan", "Turing")


def test_current_wal_lsn_advancement():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    lsn1 = client.get_current_wal_lsn()
    assert "/" in lsn1  # Format: X/YYYYYYYY

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TEMP TABLE wal_bump (id INT); INSERT INTO wal_bump VALUES (1);")

    lsn2 = client.get_current_wal_lsn()
    assert lsn1 <= lsn2


def test_streaming_replication_view_accessible():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    # In single-node standalone, pg_stat_replication returns 0 rows without error
    status = client.query_replication_status()
    assert isinstance(status, list)


def test_hot_standby_feedback_setting():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SHOW hot_standby_feedback;")
            setting = cur.fetchone()[0]
            assert setting in ("on", "off")


def test_pg_database_size_and_metrics():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_database_size(current_database());")
            db_size = cur.fetchone()[0]
            assert db_size > 0


def test_checkpoint_command_execution():
    from dbre_live import DBRELiveClient
    client = DBRELiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CHECKPOINT;")


def test_track_a_dbre_model_reconciliation():
    """Track A <-> Track B: Handbuilt ExpandContractMigrator model matches real schema evolution."""
    from dbre_engine import ExpandContractMigrator

    # 1. Expand
    records = [{"id": 1, "full_name": "Linus Torvalds"}]
    ExpandContractMigrator.expand_add_column(records, "first_name")
    assert "first_name" in records[0] and records[0]["first_name"] is None

    # 2. Backfill
    ExpandContractMigrator.backfill_batch(records, "full_name", "first_name", lambda fn: fn.split()[0])
    assert records[0]["first_name"] == "Linus"

    # 3. Contract
    ExpandContractMigrator.contract_drop_column(records, "full_name")
    assert "full_name" not in records[0]
