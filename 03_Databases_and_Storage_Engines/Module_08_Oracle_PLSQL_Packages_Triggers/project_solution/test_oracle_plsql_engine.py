"""Automated pytest test suite for Module 08 Oracle PL/SQL & Triggers Engine."""

import pytest
from oracle_plsql_engine import (
    AutonomousAuditLogger,
    BankingPackage,
    BulkProcessor,
    CompoundTrigger,
    TriggerPhase,
)


@pytest.fixture
def banking_system() -> tuple[BankingPackage, AutonomousAuditLogger]:
    logger = AutonomousAuditLogger()
    pkg = BankingPackage(logger)
    pkg.create_account("ACC_ALICE", 1000.0)
    pkg.create_account("ACC_BOB", 500.0)
    return pkg, logger


def test_account_creation_and_audit(banking_system: tuple[BankingPackage, AutonomousAuditLogger]) -> None:
    pkg, logger = banking_system
    assert pkg.accounts["ACC_ALICE"] == 1000.0
    assert pkg.accounts["ACC_BOB"] == 500.0
    assert len(logger.committed_logs) == 2


def test_successful_transfer(banking_system: tuple[BankingPackage, AutonomousAuditLogger]) -> None:
    pkg, logger = banking_system
    success = pkg.transfer_funds("ACC_ALICE", "ACC_BOB", 300.0)
    assert success is True
    assert pkg.accounts["ACC_ALICE"] == 700.0
    assert pkg.accounts["ACC_BOB"] == 800.0

    last_log = logger.committed_logs[-1]
    assert last_log.event_type == "TRANSFER_SUCCESS"


def test_autonomous_audit_persists_across_parent_rollback(
    banking_system: tuple[BankingPackage, AutonomousAuditLogger]
) -> None:
    pkg, logger = banking_system
    initial_alice_balance = pkg.accounts["ACC_ALICE"]
    initial_bob_balance = pkg.accounts["ACC_BOB"]

    # Attempt to transfer more than Alice has ($5,000 > $1,000)
    success = pkg.transfer_funds("ACC_ALICE", "ACC_BOB", 5000.0)
    assert success is False

    # Verify rollback preserved balances
    assert pkg.accounts["ACC_ALICE"] == initial_alice_balance
    assert pkg.accounts["ACC_BOB"] == initial_bob_balance

    # CRITICAL: Autonomous audit record must be committed despite rollback!
    last_log = logger.committed_logs[-1]
    assert last_log.event_type == "INSUFFICIENT_FUNDS"
    assert "Transfer of $5000.00 failed" in last_log.details
    assert last_log.is_committed is True


def test_bulk_forall_processing() -> None:
    accounts = {"ACC_1": 100.0, "ACC_2": 200.0, "ACC_3": 300.0}
    adjustments = [("ACC_1", 50.0), ("ACC_2", -20.0), ("ACC_3", 10.0)]

    updated_count = BulkProcessor.forall_update(accounts, adjustments)
    assert updated_count == 3
    assert accounts["ACC_1"] == 150.0
    assert accounts["ACC_2"] == 180.0
    assert accounts["ACC_3"] == 310.0


def test_compound_trigger_four_phase_execution() -> None:
    trg = CompoundTrigger()

    # Phase 1: Before Statement
    trg.execute_phase(TriggerPhase.BEFORE_STATEMENT)

    # Phase 2 & 3: Row processing
    trg.execute_phase(TriggerPhase.BEFORE_EACH_ROW, row_id="R1", row_value=100.0)
    trg.execute_phase(TriggerPhase.AFTER_EACH_ROW, row_id="R1", row_value=100.0)

    trg.execute_phase(TriggerPhase.BEFORE_EACH_ROW, row_id="R2", row_value=250.0)
    trg.execute_phase(TriggerPhase.AFTER_EACH_ROW, row_id="R2", row_value=250.0)

    # Phase 4: After Statement
    trg.execute_phase(TriggerPhase.AFTER_STATEMENT)

    assert len(trg.phase_log) == 6
    assert trg.buffered_row_ids == ["R1", "R2"]
    assert trg.aggregated_total == 350.0


def test_compound_trigger_rejects_invalid_values() -> None:
    trg = CompoundTrigger()
    trg.execute_phase(TriggerPhase.BEFORE_STATEMENT)

    with pytest.raises(ValueError, match="Trigger rejected negative value: -50.0"):
        trg.execute_phase(TriggerPhase.BEFORE_EACH_ROW, row_id="R_BAD", row_value=-50.0)
