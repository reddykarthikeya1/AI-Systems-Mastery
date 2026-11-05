"""Tests for E-Commerce Flash Sale Inventory Reservation System (Workshop 11)."""
import time
import pytest
from workshop_ecommerce.flash_sale_inventory import (
    FlashSaleInventoryService,
    FlashSaleInventory,
    PostgresInventoryStore,
    SimulatedPostgresLedger,
    ReservationState,
)


def test_flash_sale_successful_reservation():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_iphone", 10)

    # Initial hold
    res = svc.reserve(
        item_id="item_iphone",
        user_id="user_1",
        quantity=2,
        idempotency_key="idemp_abc123",
        ttl_seconds=300.0,
    )

    assert res.success is True
    assert res.status == "HELD"
    assert res.record.quantity == 2
    assert svc.get_stock("item_iphone") == 8


def test_reject_invalid_quantity():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_1", 10)

    res = svc.reserve("item_1", "user_1", quantity=0, idempotency_key="k1")
    assert res.success is False
    assert res.status == "ERROR"

    res_neg = svc.reserve("item_1", "user_1", quantity=-5, idempotency_key="k2")
    assert res_neg.success is False
    assert res_neg.status == "ERROR"


def test_out_of_stock_rejection():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_ps5", 3)

    # Attempt to reserve 5 items when only 3 exist
    res = svc.reserve("item_ps5", "user_2", quantity=5, idempotency_key="k3")
    assert res.success is False
    assert res.status == "OUT_OF_STOCK"
    assert res.remaining_stock == 3
    assert svc.get_stock("item_ps5") == 3


def test_idempotency_key_deduplication():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_gpu", 5)

    # 1st request
    res1 = svc.reserve("item_gpu", "user_3", quantity=1, idempotency_key="checkout_nonce_99")
    assert res1.success is True
    assert svc.get_stock("item_gpu") == 4

    # 2nd request with EXACT SAME idempotency key (e.g. client network retry)
    res2 = svc.reserve("item_gpu", "user_3", quantity=1, idempotency_key="checkout_nonce_99")
    assert res2.success is True
    assert res2.record.reservation_id == res1.record.reservation_id
    # Stock must remain 4, NOT deducted a second time!
    assert svc.get_stock("item_gpu") == 4


def test_reservation_confirmation_and_pg_reconciliation():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_tv", 10)

    res = svc.reserve("item_tv", "user_4", quantity=2, idempotency_key="pay_1")
    res_id = res.record.reservation_id

    # Confirm reservation upon successful payment
    confirm_res = svc.confirm("item_tv", res_id)
    assert confirm_res.success is True
    assert confirm_res.record.status == ReservationState.CONFIRMED

    # Verify PostgreSQL reconciliation
    assert pg.inventory["item_tv"] == 8
    assert res_id in pg.orders


def test_user_release_restores_stock():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_mac", 5)

    res = svc.reserve("item_mac", "user_5", quantity=2, idempotency_key="rel_1")
    res_id = res.record.reservation_id
    assert svc.get_stock("item_mac") == 3

    # User cancels reservation
    rel_res = svc.release("item_mac", res_id)
    assert rel_res.success is True
    assert rel_res.record.status == ReservationState.RELEASED
    # Stock restored back to 5
    assert svc.get_stock("item_mac") == 5


def test_expired_reservation_reconciliation_daemon():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_watch", 10)

    base_time = 1000.0
    res = svc.reserve(
        "item_watch",
        "user_6",
        quantity=3,
        idempotency_key="exp_1",
        ttl_seconds=60.0,
        now=base_time,
    )
    assert svc.get_stock("item_watch") == 7

    # Run reconciler before expiration -> 0 restored
    restored_early = svc.reconcile_expired_reservations("item_watch", now=base_time + 30.0)
    assert restored_early == 0
    assert svc.get_stock("item_watch") == 7

    # Run reconciler after expiration (e.g. 70 seconds later)
    restored_late = svc.reconcile_expired_reservations("item_watch", now=base_time + 70.0)
    assert restored_late == 3
    # Stock restored to 10
    assert svc.get_stock("item_watch") == 10


def test_idempotency_parameter_mismatch_rejected():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_laptop", 10)

    # Initial reservation: qty=2, user=user_1
    res1 = svc.reserve("item_laptop", "user_1", quantity=2, idempotency_key="idemp_fixed_key")
    assert res1.success is True

    # Re-use same key with mismatched quantity (requested 5 instead of 2)
    res_mismatch_qty = svc.reserve("item_laptop", "user_1", quantity=5, idempotency_key="idemp_fixed_key")
    assert res_mismatch_qty.success is False
    assert res_mismatch_qty.status == "ERROR"
    assert "parameter mismatch" in (res_mismatch_qty.message or "").lower()

    # Re-use same key with mismatched user (user_2 instead of user_1)
    res_mismatch_user = svc.reserve("item_laptop", "user_2", quantity=2, idempotency_key="idemp_fixed_key")
    assert res_mismatch_user.success is False
    assert res_mismatch_user.status == "ERROR"
    assert "parameter mismatch" in (res_mismatch_user.message or "").lower()

    # Stock must remain 8 (deducted only once)
    assert svc.get_stock("item_laptop") == 8


def test_duplicate_confirmation_rejected():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_speaker", 5)

    res = svc.reserve("item_speaker", "user_dup", quantity=1, idempotency_key="pay_dup_1")
    assert res.success is True
    res_id = res.record.reservation_id

    # 1st confirm -> Success
    c1 = svc.confirm("item_speaker", res_id)
    assert c1.success is True
    assert c1.status == "CONFIRMED"

    # 2nd confirm on already CONFIRMED reservation -> Rejected
    c2 = svc.confirm("item_speaker", res_id)
    assert c2.success is False
    assert c2.status == "INVALID_STATE"


def test_duplicate_release_rejected():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_headphone", 5)

    res = svc.reserve("item_headphone", "user_rel", quantity=2, idempotency_key="rel_dup_1")
    assert res.success is True
    res_id = res.record.reservation_id
    assert svc.get_stock("item_headphone") == 3

    # 1st release -> Success, restores stock
    r1 = svc.release("item_headphone", res_id)
    assert r1.success is True
    assert svc.get_stock("item_headphone") == 5

    # 2nd release on already RELEASED reservation -> Rejected, stock not incremented again!
    r2 = svc.release("item_headphone", res_id)
    assert r2.success is False
    assert r2.status == "INVALID_STATE"
    assert svc.get_stock("item_headphone") == 5


def test_race_between_confirm_and_expire():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_limited", 5)

    base_time = 2000.0
    res = svc.reserve(
        "item_limited",
        "user_slow",
        quantity=2,
        idempotency_key="race_key_1",
        ttl_seconds=30.0,
        now=base_time,
    )
    assert res.success is True
    res_id = res.record.reservation_id
    assert svc.get_stock("item_limited") == 3

    # Background reconciliation worker runs at base_time + 40 (reservation has expired)
    restored = svc.reconcile_expired_reservations("item_limited", now=base_time + 40.0)
    assert restored == 2
    assert svc.get_stock("item_limited") == 5

    # User attempts to confirm AFTER expiration reconciliation has processed
    confirm_late = svc.confirm("item_limited", res_id, now=base_time + 41.0)
    assert confirm_late.success is False
    assert confirm_late.status == "INVALID_STATE"
    # PostgreSQL ledger must not have recorded this late order
    assert res_id not in pg.orders
    assert svc.get_stock("item_limited") == 5


def test_postgres_reconciliation_failure_rejects_confirmation():
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_authoritative", 10)

    res = svc.reserve("item_authoritative", "user_pg_fail", quantity=4, idempotency_key="pg_fail_1")
    res_id = res.record.reservation_id

    # Simulate an authoritative discrepancy: Postgres ledger stock was reduced externally
    # (e.g. warehouse physical damage or failover data loss)
    pg.inventory["item_authoritative"] = 2  # Less than reservation quantity of 4!

    confirm_res = svc.confirm("item_authoritative", res_id)
    assert confirm_res.success is False
    assert confirm_res.status == "RECONCILIATION_FAILED"
    assert "PostgreSQL authoritative ledger" in confirm_res.message
    # Redis reservation status is rolled back / released
    assert confirm_res.record.status == ReservationState.RELEASED
    # Redis stock is restored
    assert svc.get_stock("item_authoritative") == 10


def test_confirm_expiration_default_time():
    """Verify that calling confirm() without passing now still strictly rejects expired reservations."""
    pg = SimulatedPostgresLedger()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_exp", 5)

    # Reserve with expires_at in the past relative to current wall-clock time
    res = svc.reserve(
        "item_exp",
        "user_exp",
        quantity=1,
        idempotency_key="exp_default_1",
        ttl_seconds=10.0,
        now=time.time() - 100.0,
    )
    assert res.success is True
    res_id = res.record.reservation_id

    # Calling confirm without passing `now` defaults to time.time(), strictly rejecting expired reservation
    confirm_res = svc.confirm("item_exp", res_id)
    assert confirm_res.success is False
    assert confirm_res.status == "INVALID_STATE"
    assert "EXPIRED" in (confirm_res.message or "")
    assert res_id not in pg.orders

    # Also test calling confirm with single argument confirm(res_id)
    res2 = svc.reserve(
        "item_exp",
        "user_exp2",
        quantity=1,
        idempotency_key="exp_default_2",
        ttl_seconds=5.0,
        now=time.time() - 50.0,
    )
    assert res2.success is True
    res2_id = res2.record.reservation_id
    confirm_res2 = svc.confirm(res2_id)
    assert confirm_res2.success is False
    assert confirm_res2.status == "INVALID_STATE"
    assert "EXPIRED" in (confirm_res2.message or "")


def test_dual_write_crash_window_simulation():
    """Simulates a failure where PostgreSQL reconciliation raises an unhandled exception or connection error,
    verifying how the system rolls back Redis/in-memory state and records the inconsistency."""
    class FaultyPostgresLedger(SimulatedPostgresLedger):
        def reconcile_confirmed_order(self, item_id, reservation):
            raise ConnectionError("PostgreSQL connection timeout / network partition during confirmation commit")

    pg = FaultyPostgresLedger()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_dual_write", 5)

    res = svc.reserve("item_dual_write", "user_crash", quantity=2, idempotency_key="crash_1")
    assert res.success is True
    assert svc.get_stock("item_dual_write") == 3
    res_id = res.record.reservation_id

    # Confirm triggers simulated crash/network partition in PostgreSQL reconciliation
    confirm_res = svc.confirm("item_dual_write", res_id)
    assert confirm_res.success is False
    assert confirm_res.status == "RECONCILIATION_FAILED"
    assert "PostgreSQL reconciliation error" in (confirm_res.message or "")

    # State is safely rolled back to RELEASED and stock is restored
    assert confirm_res.record.status == ReservationState.RELEASED
    assert svc.get_stock("item_dual_write") == 5

    # Verifies the system recorded the inconsistency for asynchronous reconciliation
    assert len(svc.inconsistencies) == 1
    assert svc.inconsistencies[0]["reservation_id"] == res_id
    assert "connection timeout" in svc.inconsistencies[0]["error"].lower()
    assert res_id not in pg.orders


