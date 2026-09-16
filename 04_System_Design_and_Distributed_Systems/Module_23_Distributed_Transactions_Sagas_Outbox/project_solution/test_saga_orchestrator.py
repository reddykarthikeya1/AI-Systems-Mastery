"""Unit and integration test suite for Module 23: Saga Orchestrator & Outbox Pattern."""

from saga_orchestrator import (
    IdempotentConsumer,
    InventoryReservationStep,
    OrderCreationStep,
    OutboxRecord,
    PaymentProcessingStep,
    SagaOrchestrator,
    SagaStatus,
    TransactionalOutboxStore,
)


def test_saga_happy_path_success() -> None:
    steps = [OrderCreationStep(), PaymentProcessingStep(), InventoryReservationStep()]
    orchestrator = SagaOrchestrator(steps)

    ctx = {
        "order_id": "ord_1",
        "user_id": "u1",
        "sku": "ITEM_A",
        "amount": 100.0,
        "quantity": 2,
        "accounts_db": {"u1": 500.0},
        "inventory_db": {"ITEM_A": 10},
    }

    assert orchestrator.run(ctx) is True
    assert orchestrator.status == SagaStatus.COMPLETED
    assert ctx["accounts_db"]["u1"] == 400.0
    assert ctx["inventory_db"]["ITEM_A"] == 8
    assert ctx["order_db"]["ord_1"]["status"] == "PENDING"
    assert len(orchestrator.logs) == 3


def test_saga_payment_failure_rollback() -> None:
    steps = [OrderCreationStep(), PaymentProcessingStep(), InventoryReservationStep()]
    orchestrator = SagaOrchestrator(steps)

    ctx = {
        "order_id": "ord_2",
        "user_id": "u2",
        "sku": "ITEM_A",
        "amount": 1000.0,  # User has only 100
        "quantity": 1,
        "accounts_db": {"u2": 100.0},
        "inventory_db": {"ITEM_A": 10},
    }

    assert orchestrator.run(ctx) is False
    assert orchestrator.status == SagaStatus.COMPENSATED
    assert ctx["accounts_db"]["u2"] == 100.0
    # Step 1 OrderCreation was executed and must have been compensated
    assert ctx["order_db"]["ord_2"]["status"] == "CANCELLED"
    # Inventory was never reached
    assert ctx["inventory_db"]["ITEM_A"] == 10


def test_saga_inventory_failure_backward_compensation() -> None:
    steps = [OrderCreationStep(), PaymentProcessingStep(), InventoryReservationStep()]
    orchestrator = SagaOrchestrator(steps)

    ctx = {
        "order_id": "ord_3",
        "user_id": "u3",
        "sku": "ITEM_RARE",
        "amount": 50.0,
        "quantity": 5,  # Warehouse only has 2
        "accounts_db": {"u3": 200.0},
        "inventory_db": {"ITEM_RARE": 2},
    }

    assert orchestrator.run(ctx) is False
    assert orchestrator.status == SagaStatus.COMPENSATED
    # User had money deducted in Step 2, but compensation restored it back to 200.0
    assert ctx["accounts_db"]["u3"] == 200.0
    assert ctx["order_db"]["ord_3"]["status"] == "CANCELLED"
    assert ctx["inventory_db"]["ITEM_RARE"] == 2


def test_transactional_outbox_and_idempotent_consumer() -> None:
    outbox = TransactionalOutboxStore()
    consumer = IdempotentConsumer()

    rec = OutboxRecord(
        event_id="evt_001",
        aggregate_id="agg_10",
        event_type="UserRegistered",
        payload={"username": "dev_guru"},
    )

    outbox.insert_with_transaction(rec)
    unpub = outbox.fetch_unpublished()
    assert len(unpub) == 1
    assert unpub[0].event_id == "evt_001"

    # Consume first time
    assert consumer.consume(unpub[0]) is True
    outbox.mark_published("evt_001")
    assert len(outbox.fetch_unpublished()) == 0

    # Consume second time (duplicate retry)
    assert consumer.consume(rec) is False
    assert len(consumer.handled_events) == 1
