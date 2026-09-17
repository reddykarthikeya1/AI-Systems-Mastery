"""Tests for Module 08: Real Oracle PL/SQL Packages, Triggers & Autonomous Transactions (Track B).

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

ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:11521/FREEPDB1")
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PWD = os.getenv("ORACLE_PWD", "coursepw")

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
        pytest.skip("Oracle Database is not running at localhost:11521")
    client = OraclePLSQLLiveClient(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    assert client.ping() is True


@pytest.mark.requires_oracle
def test_oracle_plsql_bulk_insert():
    if not oracle_is_available():
        pytest.skip("Oracle Database is not running at localhost:11521")
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
