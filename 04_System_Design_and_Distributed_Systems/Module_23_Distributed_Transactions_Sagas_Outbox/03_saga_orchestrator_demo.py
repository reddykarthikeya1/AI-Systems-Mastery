"""Module 23: Standalone Interactive Demo - Saga Orchestrator & Transactional Outbox."""

from project_solution.saga_orchestrator import (
    IdempotentConsumer,
    InventoryReservationStep,
    OrderCreationStep,
    OutboxRecord,
    PaymentProcessingStep,
    SagaOrchestrator,
    TransactionalOutboxStore,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 23: DISTRIBUTED TRANSACTIONS, SAGAS & TRANSACTIONAL OUTBOX")
    print("=" * 80)

    # ---------------------------------------------------------
    # Scenario 1: Successful Happy Path Saga
    # ---------------------------------------------------------
    print("\n--- 1. Happy Path Saga: Order -> Payment -> Inventory Reservation ---")
    steps = [OrderCreationStep(), PaymentProcessingStep(), InventoryReservationStep()]
    orchestrator = SagaOrchestrator(steps)

    context_success = {
        "order_id": "ord_happy_101",
        "user_id": "alice",
        "sku": "MACBOOK_M3_PRO",
        "amount": 1500.0,
        "quantity": 1,
        "accounts_db": {"alice": 2500.0},
        "inventory_db": {"MACBOOK_M3_PRO": 5},
    }

    print(" Initial State: Alice Balance = $2500, MacBook Stock = 5")
    success = orchestrator.run(context_success)

    print(f" Saga Completed:       {success} | Final Status: {orchestrator.status.value}")
    print(f" Updated Alice Balance: ${context_success['accounts_db']['alice']}")
    print(f" Updated MacBook Stock: {context_success['inventory_db']['MACBOOK_M3_PRO']}")
    for log in orchestrator.logs:
        print(f"   Log: {log.action:<10} | {log.step_name:<26} | Success: {log.success}")

    # ---------------------------------------------------------
    # Scenario 2: Failure Triggering Backward Compensation
    # ---------------------------------------------------------
    print("\n--- 2. Unhappy Path Saga: Out of Stock Triggers Backward Rollback ---")
    orchestrator_fail = SagaOrchestrator(steps)

    context_fail = {
        "order_id": "ord_fail_999",
        "user_id": "bob",
        "sku": "VINTAGE_WATCH",
        "amount": 800.0,
        "quantity": 1,
        "accounts_db": {"bob": 1000.0},
        "inventory_db": {"VINTAGE_WATCH": 0},  # ZERO stock! Will fail on Step 3
    }

    print(" Initial State: Bob Balance = $1000, Watch Stock = 0")
    success_fail = orchestrator_fail.run(context_fail)

    print(f" Saga Completed:       {success_fail} | Final Status: {orchestrator_fail.status.value}")
    print(f" Failure Reason:       '{context_fail.get('failure_reason')}'")
    print(f" Compensated Balance:  ${context_fail['accounts_db']['bob']} (Fully refunded!)")
    print(f" Order Status:         {context_fail['order_db']['ord_fail_999']['status']}")
    print(" Orchestrator Execution Log:")
    for log in orchestrator_fail.logs:
        print(f"   Log: {log.action:<10} | {log.step_name:<26} | Success: {log.success}")

    # ---------------------------------------------------------
    # Scenario 3: Transactional Outbox Pattern & Idempotent Consumer
    # ---------------------------------------------------------
    print("\n--- 3. Transactional Outbox & Idempotent Consumer (CDC Relay) ---")
    outbox = TransactionalOutboxStore()
    consumer = IdempotentConsumer()

    event = OutboxRecord(
        event_id="evt_uuid_98765",
        aggregate_id="ord_happy_101",
        event_type="OrderPlacedEvent",
        payload={"order_id": "ord_happy_101", "amount": 1500.0, "status": "CONFIRMED"},
    )

    # Atomic DB transaction write
    outbox.insert_with_transaction(event)
    print(f" Outbox Event Inserted in DB. Unpublished Count: {len(outbox.fetch_unpublished())}")

    # CDC Worker sweeps unpublished events
    cdc_records = outbox.fetch_unpublished()
    for rec in cdc_records:
        # Publish to downstream consumer
        first_delivery = consumer.consume(rec)
        print(f" CDC Relay -> Consumer Delivery 1: Handled={first_delivery}")
        outbox.mark_published(rec.event_id)

    # Simulate network retry / duplicate delivery
    duplicate_delivery = consumer.consume(event)
    print(f" CDC Relay -> Consumer Delivery 2 (Duplicate Retry): Handled={duplicate_delivery}")
    print(f" Total Unique Events Processed: {len(consumer.handled_events)}")

    print("=" * 80)


if __name__ == "__main__":
    main()
