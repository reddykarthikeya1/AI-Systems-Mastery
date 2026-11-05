"""Tests for Distributed Saga Orchestrator Pattern (Chapter 18)."""
import asyncio
import time
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


def test_saga_compensation_retry():
    """Verify that a transient error during compensation is retried and succeeds."""
    orchestrator = SagaOrchestrator(name="CompRetrySaga")
    comp_attempts = 0

    def step1_forward(ctx):
        return "step1_ok"

    def flaky_compensation(ctx):
        nonlocal comp_attempts
        comp_attempts += 1
        if comp_attempts < 2:
            raise ConnectionError("Payment gateway busy during refund")
        return "refund_ok"

    def step2_failing(ctx):
        raise RuntimeError("Fraud check failed")

    orchestrator.add_step(
        SagaStep(
            "PaymentStep",
            step1_forward,
            flaky_compensation,
            compensation_retries=2,
            retry_delay_seconds=0.01,
        )
    )
    orchestrator.add_step(SagaStep("FraudStep", step2_failing))

    result = orchestrator.execute(initial_payload={})
    assert result.status == SagaStatus.COMPENSATED
    assert comp_attempts == 2


@pytest.mark.asyncio
async def test_async_saga_execution():
    """Verify asynchronous execution and non-blocking asyncio.sleep."""
    orchestrator = SagaOrchestrator(name="AsyncSaga")
    timeline = []

    async def async_step1(ctx):
        await asyncio.sleep(0.01)
        timeline.append("async_step1")
        return {"account": "A1"}

    async def async_comp1(ctx):
        await asyncio.sleep(0.01)
        timeline.append("async_comp1")

    async def async_step2(ctx):
        await asyncio.sleep(0.01)
        raise RuntimeError("Service offline")

    orchestrator.add_step(SagaStep("Step1", async_step1, async_comp1))
    orchestrator.add_step(SagaStep("Step2", async_step2))

    result = await orchestrator.execute_async(initial_payload={})
    assert result.status == SagaStatus.COMPENSATED
    assert timeline == ["async_step1", "async_comp1"]


@pytest.mark.asyncio
async def test_async_saga_with_sync_callables_does_not_block_loop():
    """Verify that synchronous step actions and compensations execute via asyncio.to_thread.

    This ensures that synchronous blocking operations inside steps do not block
    the main asyncio event loop, allowing concurrent coroutines to make progress.
    """
    orchestrator = SagaOrchestrator(name="SyncCallablesInAsyncSaga")
    timeline = []

    def blocking_sync_step(ctx):
        # Synchronous sleep simulates a blocking database call
        time.sleep(0.06)
        timeline.append("sync_forward")
        return {"db_row": 42}

    def failing_step(ctx):
        timeline.append("failing_step")
        raise RuntimeError("Downstream rejection")

    def blocking_sync_comp(ctx):
        time.sleep(0.04)
        timeline.append("sync_comp")

    orchestrator.add_step(SagaStep("SyncStep", blocking_sync_step, blocking_sync_comp))
    orchestrator.add_step(SagaStep("FailStep", failing_step))

    # Concurrently run a background asyncio ticker to verify event loop responsiveness
    ticker_count = 0
    stop_ticker = False

    async def background_ticker():
        nonlocal ticker_count
        while not stop_ticker:
            await asyncio.sleep(0.01)
            ticker_count += 1

    ticker_task = asyncio.create_task(background_ticker())

    try:
        result = await orchestrator.execute_async(initial_payload={})
        assert result.status == SagaStatus.COMPENSATED
        assert result.step_results["SyncStep"] == {"db_row": 42}
        assert timeline == ["sync_forward", "failing_step", "sync_comp"]
        # If the event loop were blocked by time.sleep, the ticker wouldn't run.
        # With asyncio.to_thread, ticker ticks concurrently during the 0.06s + 0.04s sleeps.
        assert ticker_count >= 3
    finally:
        stop_ticker = True
        await ticker_task
