"""Automated pytest test suite for Module 09 Oracle RAC & Data Guard Engine."""

import pytest
from oracle_rac_engine import (
    CacheFusionCoordinator,
    DataGuardEngine,
    ProtectionMode,
    RACNode,
)


@pytest.fixture
def rac_cluster() -> tuple[RACNode, RACNode, CacheFusionCoordinator]:
    node1 = RACNode("RAC_NODE_1")
    node2 = RACNode("RAC_NODE_2")
    coordinator = CacheFusionCoordinator([node1, node2])
    return node1, node2, coordinator


def test_local_block_write_and_read(rac_cluster: tuple[RACNode, RACNode, CacheFusionCoordinator]) -> None:
    node1, _, _ = rac_cluster
    node1.write_block(101, {"acc": "ALICE", "bal": 5000})

    blk = node1.read_block(101)
    assert blk is not None
    assert blk.data["bal"] == 5000
    assert blk.is_dirty is True
    assert blk.lock_mode == "EXCLUSIVE"


def test_cache_fusion_interconnect_transfer(
    rac_cluster: tuple[RACNode, RACNode, CacheFusionCoordinator]
) -> None:
    node1, node2, coordinator = rac_cluster

    # Node 1 writes to Block 202
    node1.write_block(202, {"acc": "BOB", "bal": 9000})

    # Node 2 needs to read Block 202. It is not in Node 2's cache!
    assert node2.read_block(202) is None

    # Request via Cache Fusion
    fused_block = coordinator.request_block_for_read("RAC_NODE_2", 202)
    assert fused_block is not None
    assert fused_block.data["bal"] == 9000
    assert coordinator.transfers_count == 1

    # Node 2's buffer cache now contains the block
    assert node2.read_block(202) is not None
    # Both nodes now hold SHARED locks
    assert node1.read_block(202).lock_mode == "SHARED"
    assert node2.read_block(202).lock_mode == "SHARED"


def test_dead_node_raises_runtime_error(rac_cluster: tuple[RACNode, RACNode, CacheFusionCoordinator]) -> None:
    node1, _, _ = rac_cluster
    node1.is_alive = False

    with pytest.raises(RuntimeError, match="Node RAC_NODE_1 is offline"):
        node1.read_block(101)


def test_dataguard_max_protection_sync_and_fail() -> None:
    dg = DataGuardEngine(primary_id="DB_LON_PRI", standby_id="DB_DUB_STB", mode=ProtectionMode.MAX_PROTECTION)

    # Normal commit works
    assert dg.commit_on_primary(1001, "INSERT INTO USERS VALUES (1)") is True
    assert 1001 in dg.standby_applied_scns

    # Break network link: Max Protection MUST halt primary!
    dg.network_link_healthy = False
    with pytest.raises(RuntimeError, match="Max Protection violation: Standby unreachable"):
        dg.commit_on_primary(1002, "UPDATE USERS SET BAL = 100")


def test_dataguard_max_availability_downgrade() -> None:
    dg = DataGuardEngine(primary_id="DB_LON_PRI", standby_id="DB_DUB_STB", mode=ProtectionMode.MAX_AVAILABILITY)

    # Break network link: Max Availability DOES NOT halt, continues as async!
    dg.network_link_healthy = False
    success = dg.commit_on_primary(2001, "INSERT INTO AUDIT VALUES ('FAILOVER_TEST')")
    assert success is True
    # Primary logged it
    assert dg.primary_redo_log[-1]["scn"] == 2001
    # Standby did not receive it yet (retained on primary)
    assert 2001 not in dg.standby_applied_scns


def test_dataguard_standby_readonly_and_switchover() -> None:
    dg = DataGuardEngine(primary_id="DB_LON_PRI", standby_id="DB_DUB_STB")
    dg.commit_on_primary(3001, "INSERT INTO LOGS VALUES (1)")
    dg.commit_on_primary(3002, "INSERT INTO LOGS VALUES (2)")

    # Read-only query on standby returns applied SCNs
    scns = dg.query_standby_readonly()
    assert scns == [3001, 3002]

    # Perform zero-downtime planned switchover
    dg.perform_switchover()
    assert dg.primary_id == "DB_DUB_STB"
    assert dg.standby_id == "DB_LON_PRI"
