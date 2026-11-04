"""Tests for E-Commerce Flash Sale Inventory Reservation System (Workshop 11)."""
import pytest
from workshop_ecommerce.flash_sale_inventory import (
    FlashSaleInventoryService,
    PostgresInventoryStore,
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
