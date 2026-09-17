"""Unit and integration test suite for Module 20: Flash Sale & Inventory Reservation."""

import concurrent.futures

from flash_sale_engine import (
    AtomicInventoryReservationManager,
    ReservationStatus,
)


def test_atomic_reservation_and_overselling_prevention() -> None:
    mgr = AtomicInventoryReservationManager()
    sku = "PLAYSTATION_5"
    mgr.register_sku(sku, total_stock=5)

    # Reserve 3 units
    ok1, tok1 = mgr.reserve(sku, "user_1", quantity=3, ttl_sec=60.0, current_time=0.0)
    assert ok1 is True
    assert tok1 is not None
    assert tok1.quantity == 3
    assert tok1.status == ReservationStatus.RESERVED

    # Reserve 2 units
    ok2, _tok2 = mgr.reserve(sku, "user_2", quantity=2, ttl_sec=60.0, current_time=0.0)
    assert ok2 is True

    # Try reserving 1 more unit (available is 0)
    ok3, tok3 = mgr.reserve(sku, "user_3", quantity=1, ttl_sec=60.0, current_time=0.0)
    assert ok3 is False
    assert tok3 is None

    snap = mgr.get_stock_snapshot(sku)
    assert snap["available"] == 0
    assert snap["reserved"] == 5
    assert snap["purchased"] == 0
    assert mgr.verify_conservation_invariant(sku) is True


def test_confirm_purchase_lifecycle() -> None:
    mgr = AtomicInventoryReservationManager()
    sku = "TAYLOR_SWIFT_VIP"
    mgr.register_sku(sku, total_stock=10)

    ok, tok = mgr.reserve(sku, "fan_1", quantity=2, ttl_sec=100.0, current_time=10.0)
    assert ok is True

    # Confirm purchase before expiration (T=50s <= T=110s)
    success = mgr.confirm_purchase(tok.reservation_id, current_time=50.0)
    assert success is True
    assert tok.status == ReservationStatus.PURCHASED

    snap = mgr.get_stock_snapshot(sku)
    assert snap["available"] == 8
    assert snap["reserved"] == 0
    assert snap["purchased"] == 2
    assert mgr.verify_conservation_invariant(sku) is True

    # Confirming already purchased reservation should return False
    assert mgr.confirm_purchase(tok.reservation_id, current_time=55.0) is False


def test_ttl_expiry_and_reaper_rollback() -> None:
    mgr = AtomicInventoryReservationManager()
    sku = "LIMITED_EDITION_SNEAKER"
    mgr.register_sku(sku, total_stock=4)

    ok, tok = mgr.reserve(sku, "sneakerhead", quantity=3, ttl_sec=30.0, current_time=0.0)
    assert ok is True
    assert tok.expires_at == 30.0

    # User attempts to confirm AFTER expiration at T=40.0s
    confirmed = mgr.confirm_purchase(tok.reservation_id, current_time=40.0)
    assert confirmed is False
    assert tok.status == ReservationStatus.EXPIRED

    # Stock should have been restored back to available
    snap = mgr.get_stock_snapshot(sku)
    assert snap["available"] == 4
    assert snap["reserved"] == 0
    assert mgr.verify_conservation_invariant(sku) is True


def test_background_reaper_batch_rollback() -> None:
    mgr = AtomicInventoryReservationManager()
    sku = "GPU_RTX_5090"
    mgr.register_sku(sku, total_stock=10)

    # 3 reservations with different TTLs
    _, tok1 = mgr.reserve(sku, "u1", 2, ttl_sec=10.0, current_time=0.0)
    _, _tok2 = mgr.reserve(sku, "u2", 3, ttl_sec=20.0, current_time=0.0)
    _, _tok3 = mgr.reserve(sku, "u3", 4, ttl_sec=50.0, current_time=0.0)

    # At T=15s, tok1 has expired, tok2 and tok3 are still active
    reaped = mgr.reap_expired_reservations(current_time=15.0)
    assert len(reaped) == 1
    assert reaped[0].reservation_id == tok1.reservation_id

    snap = mgr.get_stock_snapshot(sku)
    assert snap["available"] == 3  # Initial 10 - 3 (tok2) - 4 (tok3) + 2 (tok1 restored) = 3
    assert mgr.verify_conservation_invariant(sku) is True


def test_explicit_cancellation() -> None:
    mgr = AtomicInventoryReservationManager()
    sku = "SMARTPHONE_PRO"
    mgr.register_sku(sku, total_stock=5)

    _, tok = mgr.reserve(sku, "u1", 2, ttl_sec=60.0, current_time=0.0)
    assert mgr.get_stock_snapshot(sku)["available"] == 3

    assert mgr.cancel_reservation(tok.reservation_id) is True
    assert tok.status == ReservationStatus.CANCELLED
    assert mgr.get_stock_snapshot(sku)["available"] == 5
    assert mgr.verify_conservation_invariant(sku) is True


def test_high_concurrency_stress_test() -> None:
    mgr = AtomicInventoryReservationManager()
    sku = "HOT_CONCERT_TICKET"
    initial_stock = 20
    mgr.register_sku(sku, total_stock=initial_stock)

    success_reservations = []
    rejected_count = 0
    num_threads = 50

    def attempt_reserve(idx: int) -> None:
        nonlocal rejected_count
        ok, tok = mgr.reserve(sku, f"thread_user_{idx}", quantity=1, ttl_sec=30.0, current_time=10.0)
        with mgr._lock:
            if ok and tok:
                success_reservations.append(tok)
            else:
                rejected_count += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        futures = [pool.submit(attempt_reserve, i) for i in range(num_threads)]
        concurrent.futures.wait(futures)

    # Exactly 20 reservations should succeed, 30 must fail
    assert len(success_reservations) == initial_stock
    assert rejected_count == (num_threads - initial_stock)

    snap = mgr.get_stock_snapshot(sku)
    assert snap["available"] == 0
    assert snap["reserved"] == initial_stock
    assert mgr.verify_conservation_invariant(sku) is True
