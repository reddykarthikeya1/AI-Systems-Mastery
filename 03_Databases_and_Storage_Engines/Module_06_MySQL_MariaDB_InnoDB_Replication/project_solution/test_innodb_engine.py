"""Automated pytest test suite for Module 06 MySQL InnoDB & Binlog Engine."""

import pytest
from innodb_engine import BinlogEventType, BinlogReplicationEngine, InnoDBClusteredTable


@pytest.fixture
def users_table() -> InnoDBClusteredTable:
    tbl = InnoDBClusteredTable(table_name="users", primary_key="id")
    tbl.create_secondary_index("email")
    tbl.insert({"id": 1, "email": "alice@corp.com", "name": "Alice", "role": "admin"})
    tbl.insert({"id": 2, "email": "bob@corp.com", "name": "Bob", "role": "developer"})
    return tbl


def test_primary_key_clustered_access(users_table: InnoDBClusteredTable) -> None:
    row = users_table.get_by_primary_key(1)
    assert row is not None
    assert row["name"] == "Alice"
    assert row["role"] == "admin"


def test_duplicate_primary_key_rejected(users_table: InnoDBClusteredTable) -> None:
    with pytest.raises(ValueError, match="Duplicate entry for primary key: '1'"):
        users_table.insert({"id": 1, "email": "imposter@corp.com", "name": "Imposter"})


def test_secondary_index_bookmark_lookup(users_table: InnoDBClusteredTable) -> None:
    # Querying a column not in secondary index ('name') requires bookmark lookup
    row, was_covering = users_table.get_by_secondary_index(
        column_name="email",
        value="bob@corp.com",
        projected_columns=["name", "role"],
    )
    assert row is not None
    assert row["name"] == "Bob"
    assert row["role"] == "developer"
    assert was_covering is False  # Required clustered index hop


def test_covering_index_fast_path(users_table: InnoDBClusteredTable) -> None:
    # Querying ONLY the indexed column and primary key ('id', 'email')
    row, was_covering = users_table.get_by_secondary_index(
        column_name="email",
        value="alice@corp.com",
        projected_columns=["id", "email"],
    )
    assert row is not None
    assert row["id"] == 1
    assert row["email"] == "alice@corp.com"
    assert was_covering is True  # Bypassed clustered index!


def test_binlog_recording_and_gtid_generation() -> None:
    engine = BinlogReplicationEngine(server_uuid="MYSQL-PRIMARY-UUID-001")

    ev1 = engine.record_event(
        event_type=BinlogEventType.WRITE_ROWS,
        table_name="users",
        before_image=None,
        after_image={"id": 10, "email": "charlie@corp.com", "name": "Charlie"},
    )
    assert ev1.gtid == "MYSQL-PRIMARY-UUID-001:1"

    ev2 = engine.record_event(
        event_type=BinlogEventType.UPDATE_ROWS,
        table_name="users",
        before_image={"id": 10, "name": "Charlie"},
        after_image={"id": 10, "name": "Charles"},
    )
    assert ev2.gtid == "MYSQL-PRIMARY-UUID-001:2"
    assert len(engine.binlog) == 2


def test_replica_replication_and_gtid_idempotency() -> None:
    engine = BinlogReplicationEngine(server_uuid="MYSQL-PRIMARY-UUID-001")
    replica = InnoDBClusteredTable(table_name="users", primary_key="id")
    executed_gtids: set[str] = set()

    # Step 1: Record insert and update on master
    engine.record_event(
        event_type=BinlogEventType.WRITE_ROWS,
        table_name="users",
        before_image=None,
        after_image={"id": 42, "email": "lead@corp.com", "name": "Lead"},
    )
    engine.record_event(
        event_type=BinlogEventType.UPDATE_ROWS,
        table_name="users",
        before_image={"id": 42, "name": "Lead"},
        after_image={"id": 42, "name": "Senior Lead"},
    )

    # Step 2: Replicate to slave
    applied = engine.replicate_to(replica, executed_gtids)
    assert applied == 2
    assert replica.get_by_primary_key(42)["name"] == "Senior Lead"

    # Step 3: Re-running replication is idempotent (GTID prevents duplicates)
    applied_again = engine.replicate_to(replica, executed_gtids)
    assert applied_again == 0
    assert len(executed_gtids) == 2
