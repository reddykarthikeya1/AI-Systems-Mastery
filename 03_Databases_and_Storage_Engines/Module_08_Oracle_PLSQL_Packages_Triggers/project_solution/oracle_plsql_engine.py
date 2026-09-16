"""Module 08: Oracle PL/SQL Packages, Triggers & Autonomous Transactions Engine Reference Solution.

Implements:
1. Banking Package with account debit, credit, and balance transfer procedures.
2. Autonomous Audit Logger that commits entries independently of parent rollback.
3. Bulk execution processor simulating FORALL batch operations.
4. Compound DML Trigger state machine executing across 4 lifecycle phases.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import uuid


class TriggerPhase(Enum):
    BEFORE_STATEMENT = "BEFORE_STATEMENT"
    BEFORE_EACH_ROW = "BEFORE_EACH_ROW"
    AFTER_EACH_ROW = "AFTER_EACH_ROW"
    AFTER_STATEMENT = "AFTER_STATEMENT"


@dataclass
class AuditRecord:
    event_id: str
    event_type: str
    details: str
    is_committed: bool = True


class AutonomousAuditLogger:
    """Simulates PRAGMA AUTONOMOUS_TRANSACTION: writes commit independently of parent."""

    def __init__(self) -> None:
        self.committed_logs: list[AuditRecord] = []

    def log_event(self, event_type: str, details: str) -> AuditRecord:
        """Immediately commits audit record to persistent storage."""
        record = AuditRecord(
            event_id=f"AUDIT_{uuid.uuid4().hex[:8].upper()}",
            event_type=event_type,
            details=details,
            is_committed=True,
        )
        self.committed_logs.append(record)
        return record


class BankingPackage:
    """Simulates an Oracle Stored Package managing account balances and transfers."""

    def __init__(self, audit_logger: AutonomousAuditLogger) -> None:
        self.audit_logger = audit_logger
        self.accounts: dict[str, float] = {}

    def create_account(self, account_id: str, initial_deposit: float) -> None:
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        self.accounts[account_id] = initial_deposit
        self.audit_logger.log_event("ACCOUNT_CREATED", f"Account {account_id} opened with ${initial_deposit:.2f}")

    def transfer_funds(self, from_acc: str, to_acc: str, amount: float) -> bool:
        """Transfers funds. If funds insufficient, logs autonomous failure and rolls back."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if from_acc not in self.accounts or to_acc not in self.accounts:
            self.audit_logger.log_event("TRANSFER_FAILED", f"Invalid account {from_acc} or {to_acc}")
            return False

        # Snapshot for rollback
        saved_from = self.accounts[from_acc]
        saved_to = self.accounts[to_acc]

        # Debit source
        if self.accounts[from_acc] < amount:
            # Overdraft: Autonomous audit log survives parent rollback
            self.audit_logger.log_event(
                "INSUFFICIENT_FUNDS",
                f"Transfer of ${amount:.2f} failed from {from_acc} (Current: ${saved_from:.2f})",
            )
            # Rollback
            self.accounts[from_acc] = saved_from
            self.accounts[to_acc] = saved_to
            return False

        self.accounts[from_acc] -= amount
        self.accounts[to_acc] += amount
        self.audit_logger.log_event(
            "TRANSFER_SUCCESS",
            f"Transferred ${amount:.2f} from {from_acc} to {to_acc}",
        )
        return True


class BulkProcessor:
    """Simulates Oracle FORALL bulk DML execution."""

    @staticmethod
    def forall_update(accounts: dict[str, float], adjustments: list[tuple[str, float]]) -> int:
        """Applies batch updates in a single vectorized pass."""
        updated = 0
        for acc_id, delta in adjustments:
            if acc_id in accounts:
                accounts[acc_id] += delta
                updated += 1
        return updated


class CompoundTrigger:
    """Simulates Oracle Compound DML Trigger avoiding ORA-04091 mutating table errors."""

    def __init__(self) -> None:
        self.phase_log: list[TriggerPhase] = []
        self.buffered_row_ids: list[str] = []
        self.aggregated_total: float = 0.0

    def execute_phase(
        self,
        phase: TriggerPhase,
        row_id: str | None = None,
        row_value: float | None = None,
    ) -> None:
        """Executes trigger phase, buffering row IDs during row-level phases for statement-level processing."""
        self.phase_log.append(phase)

        if phase == TriggerPhase.BEFORE_STATEMENT:
            # Step 1: Initialize temporary structures
            self.buffered_row_ids.clear()
            self.aggregated_total = 0.0

        elif phase == TriggerPhase.BEFORE_EACH_ROW:
            # Step 2: Per-row validation
            if row_value is not None and row_value < 0:
                raise ValueError(f"Trigger rejected negative value: {row_value}")

        elif phase == TriggerPhase.AFTER_EACH_ROW:
            # Step 3: Buffer without querying the mutating table
            if row_id:
                self.buffered_row_ids.append(row_id)
            if row_value is not None:
                self.aggregated_total += row_value

        elif phase == TriggerPhase.AFTER_STATEMENT:
            # Step 4: Table mutation complete! Safe to run post-statement audits
            pass
