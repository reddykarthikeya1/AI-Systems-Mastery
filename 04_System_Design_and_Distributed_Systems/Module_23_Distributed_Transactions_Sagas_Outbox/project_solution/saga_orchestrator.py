"""Module 23: Distributed Transactions, Saga Orchestration & Transactional Outbox Pattern.

Reference implementation of Orchestrated Saga State Machine with backward
compensations, atomic Transactional Outbox CDC relay, and idempotent message consumption.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import abc
import enum
import time
import uuid
from dataclasses import dataclass
from typing import Any

# ============================================================================
# 1. Saga State Machine Definitions
# ============================================================================

class SagaStatus(enum.StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    FAILED = "FAILED"


@dataclass
class SagaExecutionLog:
    step_name: str
    action: str  # "EXECUTE" or "COMPENSATE"
    success: bool
    timestamp: float
    error_message: str | None = None


class SagaStep(abc.ABC):
    """Abstract interface for a participant step in an orchestrated Saga."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Unique identifier for this step."""
        pass

    @abc.abstractmethod
    def execute(self, context: dict[str, Any]) -> bool:
        """Executes forward local transaction (T_i). Returns True on success, False on failure."""
        pass

    @abc.abstractmethod
    def compensate(self, context: dict[str, Any]) -> bool:
        """Executes backward compensating transaction (C_i) to undo changes made in execute()."""
        pass


# ============================================================================
# 2. Domain Steps Implementation
# ============================================================================

class OrderCreationStep(SagaStep):
    """Step 1: Creates an order in PENDING status; cancels it if compensation triggered."""

    @property
    def name(self) -> str:
        return "OrderCreationStep"

    def execute(self, context: dict[str, Any]) -> bool:
        order_db = context.setdefault("order_db", {})
        order_id = context["order_id"]
        order_db[order_id] = {"status": "PENDING", "amount": context["amount"]}
        return True

    def compensate(self, context: dict[str, Any]) -> bool:
        order_db = context.get("order_db", {})
        order_id = context["order_id"]
        if order_id in order_db:
            order_db[order_id]["status"] = "CANCELLED"
        return True


class PaymentProcessingStep(SagaStep):
    """Step 2: Debits customer balance; refunds balance on compensation."""

    @property
    def name(self) -> str:
        return "PaymentProcessingStep"

    def execute(self, context: dict[str, Any]) -> bool:
        accounts = context.setdefault("accounts_db", {})
        user_id = context["user_id"]
        amount = context["amount"]
        user_bal = accounts.get(user_id, 0.0)

        if user_bal < amount:
            context["failure_reason"] = f"Insufficient funds: Balance {user_bal} < {amount}"
            return False

        accounts[user_id] = user_bal - amount
        context["payment_id"] = f"pay_{uuid.uuid4().hex[:8]}"
        return True

    def compensate(self, context: dict[str, Any]) -> bool:
        accounts = context.get("accounts_db", {})
        user_id = context["user_id"]
        amount = context["amount"]
        # Refund user balance
        accounts[user_id] = accounts.get(user_id, 0.0) + amount
        return True


class InventoryReservationStep(SagaStep):
    """Step 3: Reserves warehouse stock; releases stock back on compensation."""

    @property
    def name(self) -> str:
        return "InventoryReservationStep"

    def execute(self, context: dict[str, Any]) -> bool:
        inventory = context.setdefault("inventory_db", {})
        sku = context["sku"]
        qty = context["quantity"]
        stock = inventory.get(sku, 0)

        if stock < qty:
            context["failure_reason"] = f"Out of stock for SKU {sku}: stock {stock} < {qty}"
            return False

        inventory[sku] = stock - qty
        return True

    def compensate(self, context: dict[str, Any]) -> bool:
        inventory = context.get("inventory_db", {})
        sku = context["sku"]
        qty = context["quantity"]
        inventory[sku] = inventory.get(sku, 0) + qty
        return True


# ============================================================================
# 3. Saga Orchestrator Engine
# ============================================================================

class SagaOrchestrator:
    """Manages forward step execution and backward compensation rollback."""

    def __init__(self, steps: list[SagaStep]) -> None:
        self.steps = steps
        self.status = SagaStatus.PENDING
        self.logs: list[SagaExecutionLog] = []

    def run(self, context: dict[str, Any]) -> bool:
        """Executes saga. If any step fails, rolls back all completed steps in reverse."""
        self.status = SagaStatus.RUNNING
        executed_steps: list[SagaStep] = []

        for step in self.steps:
            try:
                success = step.execute(context)
            except Exception as e:
                success = False
                context["failure_reason"] = str(e)

            now = time.time()
            self.logs.append(SagaExecutionLog(
                step_name=step.name,
                action="EXECUTE",
                success=success,
                timestamp=now,
                error_message=context.get("failure_reason") if not success else None,
            ))

            if success:
                executed_steps.append(step)
            else:
                # Step failed: initiate backward compensation
                self._compensate(executed_steps, context)
                return False

        self.status = SagaStatus.COMPLETED
        return True

    def _compensate(self, executed_steps: list[SagaStep], context: dict[str, Any]) -> None:
        """Triggers compensating transactions in reverse order of execution."""
        self.status = SagaStatus.COMPENSATING

        for step in reversed(executed_steps):
            try:
                comp_success = step.compensate(context)
            except Exception:
                comp_success = False

            now = time.time()
            self.logs.append(SagaExecutionLog(
                step_name=step.name,
                action="COMPENSATE",
                success=comp_success,
                timestamp=now,
            ))

        self.status = SagaStatus.COMPENSATED


# ============================================================================
# 4. Transactional Outbox Pattern & CDC Relay
# ============================================================================

class OutboxStatus(enum.StrEnum):
    UNPUBLISHED = "UNPUBLISHED"
    PUBLISHED = "PUBLISHED"


@dataclass
class OutboxRecord:
    event_id: str
    aggregate_id: str
    event_type: str
    payload: dict[str, Any]
    status: OutboxStatus = OutboxStatus.UNPUBLISHED


class TransactionalOutboxStore:
    """Simulates relational database table with ACID atomic outbox insertion."""

    def __init__(self) -> None:
        self.records: dict[str, OutboxRecord] = {}

    def insert_with_transaction(self, record: OutboxRecord) -> None:
        """Atomically inserts domain state and outbox event."""
        self.records[record.event_id] = record

    def fetch_unpublished(self) -> list[OutboxRecord]:
        return [r for r in self.records.values() if r.status == OutboxStatus.UNPUBLISHED]

    def mark_published(self, event_id: str) -> None:
        if event_id in self.records:
            self.records[event_id].status = OutboxStatus.PUBLISHED


class IdempotentConsumer:
    """Consumes outbox events safely avoiding duplicate processing."""

    def __init__(self) -> None:
        self.processed_ids: set[str] = set()
        self.handled_events: list[dict[str, Any]] = []

    def consume(self, event: OutboxRecord) -> bool:
        """Returns True if newly processed, False if duplicate detected and dropped."""
        if event.event_id in self.processed_ids:
            return False  # Deduplication hit

        self.processed_ids.add(event.event_id)
        self.handled_events.append(event.payload)
        return True
