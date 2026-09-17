"""Tests for Module 09: Real Oracle RAC Cache Fusion & Data Guard Replication (Track B).

Validates:
1. OracleHALiveClient connection & health ping
2. High Availability database role and protection mode queries
3. RAC cluster instance status queries
4. Standby destination status and transmission verification
5. RECONCILIATION: Handbuilt Cache Fusion dirty block transfer across RAC nodes over interconnect
6. RECONCILIATION: Handbuilt Data Guard standby replication with SCN tracking and read-only query support
"""

from __future__ import annotations

import os
import pytest

from Module_09_Oracle_RAC_DataGuard_GoldenGate.project_solution.oracle_ha_live import OracleHALiveClient
from Module_09_Oracle_RAC_DataGuard_GoldenGate.project_solution.oracle_rac_engine import (
    CacheFusionCoordinator as HandbuiltCacheFusion,
    DataGuardEngine as HandbuiltDataGuard,
    RACNode as HandbuiltRACNode,
    ProtectionMode,
)

ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:11521/FREEPDB1")
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PWD = os.getenv("ORACLE_PWD", "coursepw")

_oracle_available: bool | None = None


def oracle_is_available() -> bool:
    global _oracle_available
    if _oracle_available is None:
        try:
            client = OracleHALiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
            _oracle_available = client.ping()
        except Exception:
            _oracle_available = False
    return _oracle_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_rac_cache_fusion_dirty_block_transfer():
    """Verify handbuilt Cache Fusion transfers dirty blocks between node RAMs without disk I/O."""
    node1 = HandbuiltRACNode(node_id="node1")
    node2 = HandbuiltRACNode(node_id="node2")
    coordinator = HandbuiltCacheFusion(nodes=[node1, node2])

    # Node 1 writes to block 42 -> marked dirty in Node 1's buffer cache
    node1.write_block(block_id=42, updates={"balance": 500})
    assert node1.buffer_cache[42].is_dirty is True
    assert 42 not in node2.buffer_cache

    # Node 2 requests block 42 -> Coordinator coordinates Cache Fusion transfer across interconnect
    transferred_block = coordinator.request_block_for_read(requesting_node_id="node2", block_id=42)
    assert transferred_block is not None
    assert transferred_block.data["balance"] == 500
    assert 42 in node2.buffer_cache
    assert coordinator.transfers_count == 1


def test_reconciliation_dataguard_scn_replication():
    """Verify handbuilt Data Guard standby applies redo records by SCN and serves read-only queries."""
    engine = HandbuiltDataGuard(primary_id="prim", standby_id="stby", mode=ProtectionMode.MAX_AVAILABILITY)

    # Commit transactions on primary
    engine.commit_on_primary(scn=1001, sql_dml="INSERT INTO t VALUES (1)")
    engine.commit_on_primary(scn=1002, sql_dml="UPDATE t SET v=2 WHERE id=1")

    # Read-only standby query returns applied SCNs
    scns = engine.query_standby_readonly()
    assert 1001 in scns
    assert 1002 in scns

    # Switchover promotes standby to primary
    engine.perform_switchover()
    assert engine.primary_id == "stby"
    assert engine.standby_id == "prim"


# --- LIVE INTEGRATION TESTS (Skip if Oracle service is offline) ---

@pytest.mark.requires_oracle
def test_oracle_ha_ping():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OracleHALiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    assert client.ping() is True


@pytest.mark.requires_oracle
def test_oracle_database_ha_role():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OracleHALiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    role_info = client.query_database_ha_role()
    assert "database_role" in role_info
    assert "open_mode" in role_info
