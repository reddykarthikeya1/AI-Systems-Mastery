"""Module 14 Test Suite: Apache Cassandra Masterless Ring, Quorum & LWW."""

from __future__ import annotations

import pytest
from cassandra_ring_engine import (
    CassandraRingCoordinator,
    CassandraRow,
    ReadTimeoutError,
    WriteTimeoutError,
)


def test_token_ring_natural_endpoints() -> None:
    ring = CassandraRingCoordinator(replication_factor=3)
    ring.add_node("node-1", token=-5000)
    ring.add_node("node-2", token=0)
    ring.add_node("node-3", token=5000)
    ring.add_node("node-4", token=10000)

    # Any partition key should map to exactly 3 distinct nodes clockwise
    endpoints = ring.get_natural_endpoints("users:user_123")
    assert len(endpoints) == 3
    node_ids = [n.node_id for n in endpoints]
    # Verify all 3 are distinct
    assert len(set(node_ids)) == 3


def test_quorum_write_and_read_strong_consistency() -> None:
    ring = CassandraRingCoordinator(replication_factor=3)
    ring.add_node("n1", token=-1000)
    ring.add_node("n2", token=0)
    ring.add_node("n3", token=1000)

    pk = "tenant_99"
    ck = "sensor_alpha"
    data = {"temperature": 23.5, "unit": "celsius"}

    # Write at QUORUM (requires 2 of 3 acks)
    success = ring.write(pk, ck, data, consistency="QUORUM", timestamp_us=1000)
    assert success is True

    # Read at QUORUM (requires 2 of 3 responses)
    read_data = ring.read(pk, ck, consistency="QUORUM")
    assert read_data == data


def test_write_timeout_when_nodes_offline() -> None:
    ring = CassandraRingCoordinator(replication_factor=3)
    ring.add_node("n1", token=-1000)
    ring.add_node("n2", token=0)
    ring.add_node("n3", token=1000)

    pk = "orders"
    ck = "order_1"
    endpoints = ring.get_natural_endpoints(pk)

    # Bring down 2 of 3 replicas
    endpoints[0].is_online = False
    endpoints[1].is_online = False

    # QUORUM (requires 2 acks) must fail with WriteTimeoutError
    with pytest.raises(WriteTimeoutError):
        ring.write(pk, ck, {"amount": 50}, consistency="QUORUM")

    # ONE (requires 1 ack) must succeed since endpoints[2] is online
    success = ring.write(pk, ck, {"amount": 50}, consistency="ONE")
    assert success is True

    # Read at QUORUM must fail with ReadTimeoutError
    with pytest.raises(ReadTimeoutError):
        ring.read(pk, ck, consistency="QUORUM")

    # Read at ONE succeeds
    read_val = ring.read(pk, ck, consistency="ONE")
    assert read_val == {"amount": 50}


def test_read_repair_stale_replica_sync() -> None:
    ring = CassandraRingCoordinator(replication_factor=3)
    ring.add_node("n1", token=-1000)
    ring.add_node("n2", token=0)
    ring.add_node("n3", token=1000)

    pk = "accounts"
    ck = "acc_007"
    endpoints = ring.get_natural_endpoints(pk)

    # Simulate network partition divergence:
    # Replica 0 has older write at t=1000 with balance 100
    endpoints[0].write_row(
        CassandraRow(pk, ck, {"balance": 100}, timestamp_us=1000, is_tombstone=False)
    )
    # Replica 1 has newer write at t=2000 with balance 500
    endpoints[1].write_row(
        CassandraRow(pk, ck, {"balance": 500}, timestamp_us=2000, is_tombstone=False)
    )

    # Read with QUORUM queries both replicas and resolves via LWW
    res = ring.read(pk, ck, consistency="QUORUM")
    assert res == {"balance": 500}

    # Verify Read Repair synchronously updated replica 0
    repaired_row = endpoints[0].read_row(pk, ck)
    assert repaired_row is not None
    assert repaired_row.data == {"balance": 500}
    assert repaired_row.timestamp_us == 2000


def test_tombstone_deletion_lww() -> None:
    ring = CassandraRingCoordinator(replication_factor=3)
    ring.add_node("n1", token=-1000)
    ring.add_node("n2", token=0)
    ring.add_node("n3", token=1000)

    pk = "devices"
    ck = "dev_1"

    # Write at t=1000
    ring.write(pk, ck, {"status": "ACTIVE"}, consistency="QUORUM", timestamp_us=1000)
    assert ring.read(pk, ck, consistency="QUORUM") == {"status": "ACTIVE"}

    # Delete (writes tombstone at t=2000)
    ring.delete(pk, ck, consistency="QUORUM", timestamp_us=2000)
    assert ring.read(pk, ck, consistency="QUORUM") is None

    # Stale write arriving with older timestamp t=1500 is rejected by LWW
    ring.write(pk, ck, {"status": "STALE"}, consistency="QUORUM", timestamp_us=1500)
    assert ring.read(pk, ck, consistency="QUORUM") is None

    # Fresh write arriving with newer timestamp t=3000 resurrects row
    ring.write(pk, ck, {"status": "RECONNECTED"}, consistency="QUORUM", timestamp_us=3000)
    assert ring.read(pk, ck, consistency="QUORUM") == {"status": "RECONNECTED"}
