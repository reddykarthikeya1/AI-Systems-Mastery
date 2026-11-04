"""Tests for Transactional Outbox Pattern & SKIP LOCKED Semantics (Chapter 12)."""
import pytest
from ch12_event_driven.transactional_outbox import (
    SimulatedRDBMS,
    TransactionalOutboxRepository,
    MessageBus,
    OutboxPollerWorker,
    IdempotentConsumer,
    OutboxStatus,
)


def test_atomic_transaction_and_rollback():
    db = SimulatedRDBMS()

    # Commit case
    with db.begin() as tx:
        tx.save_entity("accounts", "acc_1", {"balance": 500})
        tx.append_outbox("Account", "acc_1", "AccountCreated", {"balance": 500})

    assert db.get_entity("accounts", "acc_1") == {"balance": 500}
    assert len(db.outbox_table) == 1

    # Rollback case (exception during transaction)
    try:
        with db.begin() as tx:
            tx.save_entity("accounts", "acc_2", {"balance": 100})
            tx.append_outbox("Account", "acc_2", "AccountCreated", {"balance": 100})
            raise RuntimeError("Database constraint violated!")
    except RuntimeError:
        pass

    assert db.get_entity("accounts", "acc_2") is None
    # Outbox table must still have only 1 event, not 2
    assert len(db.outbox_table) == 1


def test_concurrent_pollers_skip_locked():
    db = SimulatedRDBMS()
    bus = MessageBus()

    # Populate 6 pending outbox records
    with db.begin() as tx:
        for i in range(6):
            tx.append_outbox("Order", f"ord_{i}", "OrderPlaced", {"index": i})

    worker_a = OutboxPollerWorker("worker_A", db, bus, batch_size=3)
    worker_b = OutboxPollerWorker("worker_B", db, bus, batch_size=3)

    # Worker A fetches 3 records
    records_a = db.fetch_pending_skip_locked("worker_A", batch_size=3)
    # Worker B fetches concurrently: SKIP LOCKED should give disjoint 3 records
    records_b = db.fetch_pending_skip_locked("worker_B", batch_size=3)

    assert len(records_a) == 3
    assert len(records_b) == 3

    ids_a = {r.event_id for r in records_a}
    ids_b = {r.event_id for r in records_b}
    # No collision between workers
    assert ids_a.isdisjoint(ids_b)


def test_poller_dispatch_and_dlq_on_repeated_failure():
    db = SimulatedRDBMS()
    # Message bus that always fails
    failing_bus = MessageBus(failure_rate=1.0)

    with db.begin() as tx:
        tx.append_outbox("Payment", "pay_1", "PaymentFailed", {"amount": 200})

    worker = OutboxPollerWorker("worker_1", db, failing_bus, batch_size=1, max_retries=2)

    # Attempt 1 -> fails, retry_count = 1
    worker.poll_and_dispatch()
    rec = list(db.outbox_table.values())[0]
    assert rec.status == OutboxStatus.PENDING
    assert rec.retry_count == 1

    # Attempt 2 -> fails, reaches max_retries=2 -> FAILED and sent to DLQ
    worker.poll_and_dispatch()
    rec = list(db.outbox_table.values())[0]
    assert rec.status == OutboxStatus.FAILED
    assert len(failing_bus.dlq) == 1


def test_idempotent_consumer():
    consumer = IdempotentConsumer()
    consumed_count = 0

    def handler(record):
        nonlocal consumed_count
        consumed_count += 1

    db = SimulatedRDBMS()
    with db.begin() as tx:
        rec = tx.append_outbox("User", "u1", "UserSignedUp", {"email": "u1@example.com"})

    # First delivery
    first_ok = consumer.handle(rec, handler)
    assert first_ok is True
    assert consumed_count == 1

    # Redelivery of duplicate message
    second_ok = consumer.handle(rec, handler)
    assert second_ok is False  # Deduplicated!
    assert consumed_count == 1
