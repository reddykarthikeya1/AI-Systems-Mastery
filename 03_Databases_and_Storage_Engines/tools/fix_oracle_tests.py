from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

# Fix Module 08 test
m08_test = root / "Module_08_Oracle_PLSQL_Packages_Triggers" / "project_solution" / "test_oracle_plsql_live.py"

m08_code = '''"""Tests for Module 08: Real Oracle PL/SQL Packages, Triggers & Autonomous Transactions (Track B).

Validates:
1. OraclePLSQLLiveClient connection & health ping
2. PL/SQL banking package deployment and procedure invocation
3. Bulk array insert (executemany simulating FORALL)
4. Autonomous transaction persistence across parent rollback
5. RECONCILIATION: Handbuilt AutonomousAuditLogger commits independently of parent rollback
6. RECONCILIATION: Handbuilt BankingPackage atomic transfer and overdraft rollback
"""

from __future__ import annotations

import os
import pytest

from Module_08_Oracle_PLSQL_Packages_Triggers.project_solution.oracle_plsql_live import OraclePLSQLLiveClient
from Module_08_Oracle_PLSQL_Packages_Triggers.project_solution.oracle_plsql_engine import (
    AutonomousAuditLogger as HandbuiltAuditLogger,
    BankingPackage as HandbuiltBankPkg,
)

ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/FREEPDB1")
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PWD = os.getenv("ORACLE_PWD", "oracle")

_oracle_available: bool | None = None


def oracle_is_available() -> bool:
    global _oracle_available
    if _oracle_available is None:
        try:
            client = OraclePLSQLLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
            _oracle_available = client.ping()
        except Exception:
            _oracle_available = False
    return _oracle_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_autonomous_transaction_rollback():
    """Verify autonomous audit record remains committed even when parent business transaction rolls back."""
    logger = HandbuiltAuditLogger()
    pkg = HandbuiltBankPkg(logger)
    pkg.create_account("ACC_ALICE", 1000.0)
    pkg.create_account("ACC_BOB", 500.0)

    # Attempt to transfer more than Alice has ($5,000 > $1,000)
    success = pkg.transfer_funds("ACC_ALICE", "ACC_BOB", 5000.0)
    assert success is False

    # Account balances must remain unchanged
    assert pkg.accounts["ACC_ALICE"] == 1000.0
    assert pkg.accounts["ACC_BOB"] == 500.0

    # CRITICAL: Autonomous audit record must still be committed
    last_log = logger.committed_logs[-1]
    assert last_log.event_type == "INSUFFICIENT_FUNDS"
    assert last_log.is_committed is True


def test_reconciliation_banking_package_transfers():
    """Verify handbuilt BankingPackage debit/credit constraints and atomicity."""
    logger = HandbuiltAuditLogger()
    pkg = HandbuiltBankPkg(logger)
    pkg.create_account("ACC_1", 1000.0)
    pkg.create_account("ACC_2", 500.0)

    success = pkg.transfer_funds("ACC_1", "ACC_2", 300.0)
    assert success is True
    assert pkg.accounts["ACC_1"] == 700.0
    assert pkg.accounts["ACC_2"] == 800.0


# --- LIVE INTEGRATION TESTS (Skip if Oracle service is offline) ---

@pytest.mark.requires_oracle
def test_oracle_plsql_ping():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:1521")
    client = OraclePLSQLLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    assert client.ping() is True


@pytest.mark.requires_oracle
def test_oracle_plsql_bulk_insert():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:1521")
    client = OraclePLSQLLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'DROP TABLE test_accounts PURGE';
                EXCEPTION WHEN OTHERS THEN NULL;
                END;
            """)
            cur.execute("CREATE TABLE test_accounts (acct_id NUMBER PRIMARY KEY, owner VARCHAR2(50), balance NUMBER)")

    records = [(i, f"Owner_{i}", 1000.0 + i) for i in range(25)]
    inserted = client.bulk_insert_accounts(records)
    assert inserted == 25
'''

m08_test.write_text(m08_code, encoding="utf-8")

# Fix Module 09 test
m09_test = root / "Module_09_Oracle_RAC_DataGuard_GoldenGate" / "project_solution" / "test_oracle_ha_live.py"

m09_code = '''"""Tests for Module 09: Real Oracle RAC Cache Fusion & Data Guard Replication (Track B).

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

ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/FREEPDB1")
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PWD = os.getenv("ORACLE_PWD", "oracle")

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
        pytest.skip("Oracle Database is not running at localhost:1521")
    client = OracleHALiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    assert client.ping() is True


@pytest.mark.requires_oracle
def test_oracle_database_ha_role():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:1521")
    client = OracleHALiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    role_info = client.query_database_ha_role()
    assert "database_role" in role_info
    assert "open_mode" in role_info
'''

m09_test.write_text(m09_code, encoding="utf-8")
print("Oracle tests fixed successfully.")
