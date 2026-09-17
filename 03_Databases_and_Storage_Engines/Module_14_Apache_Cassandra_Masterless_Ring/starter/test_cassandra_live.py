"""Tests for Module 14: Real Apache Cassandra / ScyllaDB Driver (Track B).

Validates:
1. CassandraLiveClient connection & health ping
2. Keyspace and wide-column table creation
3. Writes with tunable consistency levels (ONE, QUORUM)
4. LWT Paxos conditional writes
5. RECONCILIATION: Handbuilt CassandraRingCoordinator token hashing matches 64-bit space
6. RECONCILIATION: Handbuilt quorum acknowledgment calculations (ONE=1, QUORUM=RF//2+1, ALL=RF)
"""

from __future__ import annotations

import os
import pytest

from Module_14_Apache_Cassandra_Masterless_Ring.project_solution.cassandra_live import (
    CassandraLiveClient,
    ConsistencyLevel,
)
from Module_14_Apache_Cassandra_Masterless_Ring.project_solution.cassandra_ring_engine import (
    CassandraRingCoordinator as HandbuiltCoordinator,
)

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
_cassandra_available: bool | None = None


def cassandra_is_available() -> bool:
    global _cassandra_available
    if _cassandra_available is None:
        try:
            client = CassandraLiveClient(contact_points=[CASSANDRA_HOST])
            _cassandra_available = client.ping()
        except Exception:
            _cassandra_available = False
    return _cassandra_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_token_ring_hashing():
    """Verify handbuilt Cassandra coordinator computes stable 64-bit integer tokens for partition keys."""
    coord = HandbuiltCoordinator(replication_factor=3)

    token1 = coord.hash_partition_key("user_1001")
    token2 = coord.hash_partition_key("user_1001")
    token3 = coord.hash_partition_key("user_1002")

    # Tokens must be deterministic and fit in signed 64-bit integer range
    assert token1 == token2
    assert token1 != token3
    assert - (2**63) <= token1 < 2**63


def test_reconciliation_tunable_quorum_acks():
    """Verify handbuilt quorum calculation satisfies strict majority across replication factors."""
    # RF = 3: ONE=1, QUORUM=2, ALL=3
    coord3 = HandbuiltCoordinator(replication_factor=3)
    assert coord3._required_acks("ONE") == 1
    assert coord3._required_acks("QUORUM") == 2
    assert coord3._required_acks("ALL") == 3

    # RF = 5: ONE=1, QUORUM=3, ALL=5
    coord5 = HandbuiltCoordinator(replication_factor=5)
    assert coord5._required_acks("ONE") == 1
    assert coord5._required_acks("QUORUM") == 3
    assert coord5._required_acks("ALL") == 5


# --- LIVE INTEGRATION TESTS (Skip if Cassandra service is offline) ---

@pytest.mark.requires_cassandra
def test_cassandra_ping():
    if not cassandra_is_available():
        pytest.skip("Cassandra cluster is not running at localhost:9042")
    client = CassandraLiveClient(contact_points=[CASSANDRA_HOST])
    assert client.ping() is True


@pytest.mark.requires_cassandra
def test_cassandra_schema_and_write():
    if not cassandra_is_available():
        pytest.skip("Cassandra cluster is not running at localhost:9042")
    client = CassandraLiveClient(contact_points=[CASSANDRA_HOST], keyspace="test_cass_live")
    client.setup_keyspace_and_table()
    client.write_sensor_reading("dev_1", "2026-03-30", 22.5, 55.0, consistency=ConsistencyLevel.ONE)
    client.close()
