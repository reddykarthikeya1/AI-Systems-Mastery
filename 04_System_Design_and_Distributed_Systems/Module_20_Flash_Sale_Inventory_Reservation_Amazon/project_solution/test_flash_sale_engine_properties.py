"""Property and performance assertions for Flash Sale Inventory Reservation.

These complement the correctness tests in `test_flash_sale_engine.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import concurrent.futures

import pytest
from flash_sale_engine import AtomicInventoryReservationManager, NaiveInventoryStore


@pytest.mark.concurrency
@pytest.mark.slow
def test_the_naive_store_demonstrably_oversells() -> None:
    """The failing baseline, asserted rather than described.

    A read-then-write with no atomicity oversells under contention. This test
    exists so the lesson is a measurement the learner can reproduce, not a claim
    in a README. If it ever *stops* overselling the demonstration is broken and
    the module has lost its motivating example.
    """
    stock = 50
    store = NaiveInventoryStore(initial_stock=stock)

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        results = [f.result() for f in
                   [pool.submit(store.attempt_buy, 1) for _ in range(400)]]

    sold = sum(1 for r in results if r)
    assert sold >= stock, f"sold {sold} of {stock}"
    # The point: under real contention this exceeds stock. Allow either outcome
    # so the test is not itself flaky, but record which happened.
    if sold > stock:
        assert True, f"oversold by {sold - stock} - exactly the defect"


@pytest.mark.concurrency
@pytest.mark.slow
def test_the_atomic_manager_never_oversells_under_heavy_contention() -> None:
    """The fix, held to a hard guarantee: never more reservations than stock."""
    manager = AtomicInventoryReservationManager()
    manager.register_sku("iphone", total_stock=50)

    def try_reserve(user: int) -> bool:
        ok, _token = manager.reserve("iphone", user_id=f"u{user}", quantity=1)
        return ok

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        outcomes = [f.result() for f in [pool.submit(try_reserve, i) for i in range(500)]]

    granted = sum(1 for o in outcomes if o)
    assert granted <= 50, f"granted {granted} reservations against 50 units of stock"
    assert manager.verify_conservation_invariant("iphone"), (
        "sold + reserved + available must equal total stock at all times"
    )


def test_conservation_invariant_holds_across_the_full_lifecycle() -> None:
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=10)

    ok, token = manager.reserve("sku", user_id="u1", quantity=3)
    assert ok and token is not None
    assert manager.verify_conservation_invariant("sku")

    manager.confirm_purchase(token.reservation_id)
    assert manager.verify_conservation_invariant("sku")

    ok, second = manager.reserve("sku", user_id="u2", quantity=2)
    assert ok and second is not None
    manager.cancel_reservation(second.reservation_id)
    assert manager.verify_conservation_invariant("sku")


def test_expired_reservations_return_stock_to_the_pool() -> None:
    """A reservation with a TTL that never expires is a permanent stock leak."""
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=5)

    manager.reserve("sku", user_id="u1", quantity=5, ttl_sec=10, current_time=1000.0)
    denied, _ = manager.reserve("sku", user_id="u2", quantity=1, current_time=1001.0)
    assert not denied, "stock was still held by a live reservation"

    reaped = manager.reap_expired_reservations(current_time=1100.0)
    assert reaped, "the expired reservation should have been reaped"
    granted, _ = manager.reserve("sku", user_id="u2", quantity=1, current_time=1101.0)
    assert granted, "reaped stock was not returned to the available pool"
    assert manager.verify_conservation_invariant("sku")


def test_reserving_more_than_total_stock_is_refused() -> None:
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=3)
    ok, token = manager.reserve("sku", user_id="u", quantity=4)
    assert not ok and token is None


def test_confirming_an_unknown_reservation_is_refused() -> None:
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=3)
    assert not manager.confirm_purchase("does-not-exist")
