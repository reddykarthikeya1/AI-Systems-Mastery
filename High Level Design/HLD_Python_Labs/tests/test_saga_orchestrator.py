"""Tests for Distributed Saga Orchestrator Pattern (Chapter 18)."""
import pytest
from ch18_saga_orchestrator.saga_orchestrator import (
    SagaOrchestrator,
    SagaStep,
    SagaStatus,
)


def test_saga_successful_execution():
    orchestrator = SagaOrchestrator(name="BookingSaga")
    execution_order = []

    def step1_forward(ctx):
        execution_order.append("reserve_hotel")
        return {"hotel_id": "H101"}

    def step2_forward(ctx):
        execution_order.append("book_flight")
        return {"flight_id": "FL404"}

    orchestrator.add_step(SagaStep("HotelStep", step1_forward))
    orchestrator.add_step(SagaStep("FlightStep", step2_forward))

    result = orchestrator.execute(initial_payload={"user": "Alice"})

    assert result.status == SagaStatus.COMPLETED
    assert result.step_results["HotelStep"] == {"hotel_id": "H101"}
    assert result.step_results["FlightStep"] == {"flight_id": "FL404"}
    assert execution_order == ["reserve_hotel", "book_flight"]


def test_saga_reverse_compensation_on_failure():
    orchestrator = SagaOrchestrator(name="PaymentOrderSaga")
    compensations_called = []

    def step1_forward(ctx):
        return "step1_ok"

    def step1_compensate(ctx):
        compensations_called.append("step1_rollback")

    def step2_forward(ctx):
        return "step2_ok"

    def step2_compensate(ctx):
        compensations_called.append("step2_rollback")

    def step3_failing(ctx):
        raise ValueError("Inventory unavailable")

    orchestrator.add_step(SagaStep("Payment", step1_forward, step1_compensate))
    orchestrator.add_step(SagaStep("Inventory", step2_forward, step2_compensate))
    orchestrator.add_step(SagaStep("Shipping", step3_failing, None))

    result = orchestrator.execute(initial_payload={"order": 123})

    assert result.status == SagaStatus.COMPENSATED
    assert "Inventory unavailable" in result.error

    # Crucial Saga Invariant: Compensations must run in REVERSE order of forward steps!
    # Step 2 compensated first, then Step 1
    assert compensations_called == ["step2_rollback", "step1_rollback"]


def test_saga_step_retry_before_abort():
    orchestrator = SagaOrchestrator(name="RetrySaga")
    attempts = 0

    def flaky_service(ctx):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Temporary network blip")
        return "success_on_attempt_3"

    orchestrator.add_step(
        SagaStep(
            "FlakyStep",
            flaky_service,
            max_retries=3,
            retry_delay_seconds=0.01,
        )
    )

    result = orchestrator.execute(initial_payload={})
    assert result.status == SagaStatus.COMPLETED
    assert attempts == 3
    assert result.step_results["FlakyStep"] == "success_on_attempt_3"
