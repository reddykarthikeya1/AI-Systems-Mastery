"""Tests for E-Commerce Flash Sale Inventory Reservation System (Workshop 11)."""
import time
import pytest
from workshop_ecommerce.flash_sale_inventory import (
    FlashSaleInventoryService,
    FlashSaleInventory,
    PostgresInventoryStore,
    SimulatedPostgresLedger,
    ReservationState,
    ReservationRecord,
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


def test_idempotent_confirmation_rollback():
    """Verify that confirmation rollback is idempotent and never restores stock more than once."""
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_rollback", 10)

    res = svc.reserve("item_rollback", "user_rb", quantity=3, idempotency_key="idemp_rb_1")
    assert res.success is True
    res_id = res.record.reservation_id
    assert svc.get_stock("item_rollback") == 7

    # Confirm reservation
    confirm_res = svc.confirm("item_rollback", res_id)
    assert confirm_res.success is True
    assert svc.get_stock("item_rollback") == 7

    # First rollback call: restores 3 items to stock (7 + 3 = 10)
    rb1 = svc.rollback_confirmation("item_rollback", res_id)
    assert rb1.success is True
    assert rb1.record.status == ReservationState.RELEASED
    assert svc.get_stock("item_rollback") == 10
    assert res_id in svc._rolled_back_reservations

    # Second rollback call: idempotent, must NOT restore inventory a second time (stock remains 10)
    rb2 = svc.rollback_confirmation("item_rollback", res_id)
    assert rb2.success is True
    assert svc.get_stock("item_rollback") == 10

    # Third rollback call using alias or single parameter: still strictly 10
    rb3 = svc.rollback(res_id)
    assert rb3.success is True
    assert svc.get_stock("item_rollback") == 10


def test_exact_expiry_boundary_condition():
    """Verify that a reservation with expires_at = T is strictly expired when now == T (now >= expires_at)."""
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_boundary", 10)

    base_time = 1000.0
    ttl = 30.0
    res = svc.reserve(
        "item_boundary",
        "user_bound",
        quantity=2,
        idempotency_key="bound_key_1",
        ttl_seconds=ttl,
        now=base_time,
    )
    assert res.success is True
    res_id = res.record.reservation_id
    expires_at = res.record.expires_at
    assert expires_at == base_time + ttl  # 1030.0

    # Before boundary: now = 1029.9 -> Not expired
    # At exact boundary: now = 1030.0 -> Strictly expired (now >= expires_at)
    confirm_boundary = svc.confirm("item_boundary", res_id, now=expires_at)
    assert confirm_boundary.success is False
    assert confirm_boundary.status == "INVALID_STATE"
    assert "EXPIRED" in (confirm_boundary.message or "")
    assert res_id not in pg.orders

    # Verify reconciliation daemon also strictly handles now == expires_at
    res2 = svc.reserve(
        "item_boundary",
        "user_bound2",
        quantity=3,
        idempotency_key="bound_key_2",
        ttl_seconds=ttl,
        now=base_time,
    )
    assert res2.success is True
    res2_id = res2.record.reservation_id
    expires_at_2 = res2.record.expires_at

    restored = svc.reconcile_expired_reservations("item_boundary", now=expires_at_2)
    assert restored >= 3


def test_idempotent_postgres_reconciliation():
    """Verify that calling reconcile_confirmed_order multiple times with the same reservation ID
    succeeds idempotently without double-decrementing the DB ledger stock."""
    pg = PostgresInventoryStore()
    pg.set_initial_inventory("item_ledger", 10)

    rec = ReservationRecord(
        reservation_id="res_pg_idem_999",
        user_id="user_pg",
        quantity=3,
        status=ReservationState.HELD,
        created_at=100.0,
        expires_at=200.0,
    )

    # 1st reconciliation: decrements stock from 10 to 7
    ok1 = pg.reconcile_confirmed_order("item_ledger", rec)
    assert ok1 is True
    assert pg.inventory["item_ledger"] == 7
    assert "res_pg_idem_999" in pg.orders
    assert "res_pg_idem_999" in pg._reconciled_reservations

    # 2nd reconciliation: returns cached success, stock stays at 7
    ok2 = pg.reconcile_confirmed_order("item_ledger", rec)
    assert ok2 is True
    assert pg.inventory["item_ledger"] == 7

    # 3rd reconciliation: still stays at 7
    ok3 = pg.reconcile_confirmed_order("item_ledger", rec)
    assert ok3 is True
    assert pg.inventory["item_ledger"] == 7


def test_ambiguous_postgres_timeout_marks_pending_reconciliation():
    """Simulates a timeout exception during PostgreSQL reconciliation, verifying that:
    1. Status is transitioned to PENDING_RECONCILIATION.
    2. Stock is NOT restored prematurely.
    3. The inconsistency is queued in self.inconsistencies for manual/daemon reconciliation.
    """
    class TimingOutPostgresLedger(SimulatedPostgresLedger):
        def reconcile_confirmed_order(self, item_id, reservation):
            raise TimeoutError("PostgreSQL commit timed out awaiting socket response")

    pg = TimingOutPostgresLedger()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_timeout", 5)

    res = svc.reserve("item_timeout", "user_timeout", quantity=2, idempotency_key="timeout_key_1")
    assert res.success is True
    assert svc.get_stock("item_timeout") == 3
    res_id = res.record.reservation_id

    # Confirm triggers simulated ambiguous timeout
    confirm_res = svc.confirm("item_timeout", res_id)
    assert confirm_res.success is False
    assert confirm_res.status == "PENDING_RECONCILIATION"
    assert confirm_res.record.status == ReservationState.PENDING_RECONCILIATION
    assert "timeout" in (confirm_res.message or "").lower()

    # Ambiguous timeout: do NOT blindly restore stock! Stock must remain 3
    assert svc.get_stock("item_timeout") == 3

    # Inconsistency is queued for manual/daemon resolution
    assert len(svc.inconsistencies) == 1
    inc = svc.inconsistencies[0]
    assert inc["reservation_id"] == res_id
    assert inc["status"] == "PENDING_RECONCILIATION"
    assert "timed out" in inc["error"].lower() or "timeout" in inc["error"].lower()
    assert res_id not in pg.orders


def test_rollback_rejected_while_pending_reconciliation():
    """Verify that ordinary rollback is strictly prohibited from releasing a reservation
    that is in PENDING_RECONCILIATION, preventing inventory double-allocation under network ambiguity."""
    class TimingOutPostgresLedger(SimulatedPostgresLedger):
        def reconcile_confirmed_order(self, item_id, reservation):
            raise TimeoutError("Socket timeout on commit")

    pg = TimingOutPostgresLedger()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_rb_guard", 10)

    res = svc.reserve("item_rb_guard", "user_guard", quantity=4, idempotency_key="guard_key_1")
    assert res.success is True
    assert svc.get_stock("item_rb_guard") == 6
    res_id = res.record.reservation_id

    # Confirm causes timeout -> PENDING_RECONCILIATION
    c_res = svc.confirm("item_rb_guard", res_id)
    assert c_res.status == "PENDING_RECONCILIATION"

    # Attempting ordinary rollback must be rejected!
    rb_res = svc.rollback_confirmation("item_rb_guard", res_id)
    assert rb_res.success is False
    assert rb_res.status == "PENDING_RECONCILIATION"
    assert "cannot rollback reservation pending reconciliation" in (rb_res.message or "").lower()

    # Stock MUST NOT be released!
    assert svc.get_stock("item_rb_guard") == 6


def test_reconcile_pending_with_committed_order():
    """Simulates a database commit succeeded but socket timed out, followed by reconciliation
    confirming the order from the authoritative ledger without double-decrementing stock."""
    class CommitThenTimeoutPostgres(SimulatedPostgresLedger):
        def __init__(self):
            super().__init__()
            self.timeout_on_next = True

        def reconcile_confirmed_order(self, item_id, reservation):
            # Authoritative commit succeeds in PostgreSQL
            super().reconcile_confirmed_order(item_id, reservation)
            if self.timeout_on_next:
                self.timeout_on_next = False
                raise TimeoutError("Network dropped ack after DB commit")
            return True

    pg = CommitThenTimeoutPostgres()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_comm_timeout", 10)

    res = svc.reserve("item_comm_timeout", "user_comm", quantity=3, idempotency_key="comm_k1")
    assert res.success is True
    assert svc.get_stock("item_comm_timeout") == 7
    res_id = res.record.reservation_id

    # Confirm times out from client perspective
    c_res = svc.confirm("item_comm_timeout", res_id)
    assert c_res.status == "PENDING_RECONCILIATION"
    assert pg.has_order(res_id) is True  # DB actually committed

    # Run authoritative reconciliation
    rec_res = svc.reconcile_pending_reservation("item_comm_timeout", res_id)
    assert rec_res.success is True
    assert rec_res.status == "CONFIRMED"
    assert rec_res.record.status == ReservationState.CONFIRMED

    # Stock must remain 7 (not decremented twice!)
    assert svc.get_stock("item_comm_timeout") == 7

    # Repeated reconciliation is idempotent
    rec_res2 = svc.reconcile_pending_reservation("item_comm_timeout", res_id)
    assert rec_res2.success is True
    assert rec_res2.status == "CONFIRMED"
    assert svc.get_stock("item_comm_timeout") == 7


def test_reconcile_pending_with_definitively_aborted_transaction():
    """Simulates a transaction that definitely aborted in PostgreSQL, followed by reconciliation
    that safely releases the hold and restores stock exactly once."""
    class AbortPostgres(SimulatedPostgresLedger):
        def reconcile_confirmed_order(self, item_id, reservation):
            raise TimeoutError("Transaction aborted by deadlock detector")

    pg = AbortPostgres()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_abort", 10)

    res = svc.reserve("item_abort", "user_abort", quantity=4, idempotency_key="abort_k1")
    assert res.success is True
    assert svc.get_stock("item_abort") == 6
    res_id = res.record.reservation_id

    c_res = svc.confirm("item_abort", res_id)
    assert c_res.status == "PENDING_RECONCILIATION"
    assert pg.has_order(res_id) is False

    # Authoritative reconciliation verifies final absence: releases hold and restores stock
    rec_res = svc.reconcile_pending_reservation("item_abort", res_id, final_absence_confirmed=True)
    assert rec_res.success is True
    assert rec_res.status == "RELEASED"
    assert rec_res.record.status == ReservationState.RELEASED

    # Stock restored back to 10
    assert svc.get_stock("item_abort") == 10

    # Repeated reconciliation is idempotent: does NOT restore stock twice!
    rec_res2 = svc.reconcile_pending_reservation("item_abort", res_id, final_absence_confirmed=True)
    assert rec_res2.success is True
    assert rec_res2.status == "RELEASED"
    assert svc.get_stock("item_abort") == 10

    # Ordinary rollback also acknowledges already rolled back
    rb_res = svc.rollback_confirmation("item_abort", res_id)
    assert rb_res.success is True
    assert svc.get_stock("item_abort") == 10


def test_reconcile_pending_still_unreachable_remains_pending():
    """Simulates a database that remains unreachable during reconciliation, ensuring
    reservation stays in PENDING_RECONCILIATION without prematurely restoring stock."""
    class PersistentTimeoutPostgres(SimulatedPostgresLedger):
        def reconcile_confirmed_order(self, item_id, reservation):
            raise TimeoutError("PostgreSQL unreachable")

        def has_order(self, reservation_id):
            raise TimeoutError("PostgreSQL connection timeout during ledger check")

    pg = PersistentTimeoutPostgres()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_persist_to", 8)

    res = svc.reserve("item_persist_to", "user_pto", quantity=3, idempotency_key="pto_k1")
    assert res.success is True
    assert svc.get_stock("item_persist_to") == 5
    res_id = res.record.reservation_id

    svc.confirm("item_persist_to", res_id)

    # Reconciliation attempt fails because DB is still timing out
    rec_res = svc.reconcile_pending_reservation("item_persist_to", res_id)
    assert rec_res.success is False
    assert rec_res.status == "PENDING_RECONCILIATION"
    assert "unreachable" in (rec_res.message or "").lower() or "timeout" in (rec_res.message or "").lower()

    # Stock must remain 5
    assert svc.get_stock("item_persist_to") == 5


def test_confirmed_order_cannot_be_accidentally_released():
    """Verify that once an order is CONFIRMED, ordinary release() and rollback() cannot void it."""
    pg = PostgresInventoryStore()
    svc = FlashSaleInventory(postgres_db=pg)
    svc.initialize_stock("item_solid", 10)

    res = svc.reserve("item_solid", "user_solid", quantity=2, idempotency_key="solid_k1")
    assert res.success is True
    assert svc.get_stock("item_solid") == 8
    res_id = res.record.reservation_id

    confirm_res = svc.confirm("item_solid", res_id)
    assert confirm_res.success is True
    assert confirm_res.status == "CONFIRMED"

    # User release() must be rejected on CONFIRMED order
    rel_res = svc.release("item_solid", res_id)
    assert rel_res.success is False
    assert rel_res.status == "INVALID_STATE"

    # Stock remains 8
    assert svc.get_stock("item_solid") == 8


def test_intermediate_state_prevents_crash_dual_write_split_brain():
    """Verify that enforcing intermediate state PENDING_CONFIRMATION prevents crash dual-write split-brain:
    1. During confirm(), reservation atomically transitions HELD -> PENDING_CONFIRMATION and is removed from auto-expiry.
    2. A crash or timeout during PostgreSQL call leaves reservation in PENDING_CONFIRMATION / PENDING_RECONCILIATION,
       never falsely marked CONFIRMED in cache while absent in DB.
    3. Normal auto-expiry daemon does NOT evict or restore stock while in PENDING_CONFIRMATION.
    4. Authoritative reconciliation resolves the intermediate state safely.
    """
    class CrashingPostgres(SimulatedPostgresLedger):
        def __init__(self):
            super().__init__()
            self.observed_status_during_call = None
            self.in_expirations_during_call = None

        def reconcile_confirmed_order(self, item_id, reservation):
            # Inspect reservation state in the service during the PostgreSQL call
            rec = svc._reserves_store.get(item_id, {}).get(reservation.reservation_id)
            self.observed_status_during_call = rec.status if rec else None
            self.in_expirations_during_call = reservation.reservation_id in svc._expirations_store.get(item_id, {})
            # Simulate crash / timeout
            raise TimeoutError("Application process crashed or network partitioned before PostgreSQL ack")

    pg = CrashingPostgres()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_intermediate", 10)

    base_time = 1000.0
    res = svc.reserve(
        "item_intermediate",
        "user_int",
        quantity=3,
        idempotency_key="int_k1",
        ttl_seconds=30.0,
        now=base_time,
    )
    assert res.success is True
    res_id = res.record.reservation_id
    assert svc.get_stock("item_intermediate") == 7

    # Call confirm: triggers intermediate state then simulated crash
    confirm_res = svc.confirm("item_intermediate", res_id, now=base_time + 10.0)

    # 1. Verify intermediate state was active during PostgreSQL call
    assert pg.observed_status_during_call == ReservationState.PENDING_CONFIRMATION
    # 2. Verify removed from normal auto-expiry index during call
    assert pg.in_expirations_during_call is False

    # 3. Crash result: reservation is in PENDING_RECONCILIATION / PENDING_CONFIRMATION, NOT CONFIRMED!
    assert confirm_res.success is False
    assert confirm_res.status == "PENDING_RECONCILIATION"
    assert confirm_res.record.status == ReservationState.PENDING_RECONCILIATION
    assert pg.has_order(res_id) is False  # PostgreSQL has no committed order

    # 4. Normal auto-expiry daemon runs past original TTL (now = base_time + 50.0):
    # It must NOT prematurely evict or restore stock!
    restored = svc.reconcile_expired_reservations("item_intermediate", now=base_time + 50.0)
    assert restored == 0
    assert svc.get_stock("item_intermediate") == 7

    # 5. Authoritative reconciliation resolves the intermediate state
    # When transaction aborted and final absence confirmed: safely releases and restores stock
    rec_res = svc.reconcile_pending_reservation("item_intermediate", res_id, final_absence_confirmed=True)
    assert rec_res.success is True
    assert rec_res.status == "RELEASED"
    assert rec_res.record.status == ReservationState.RELEASED
    assert svc.get_stock("item_intermediate") == 10


def test_rollback_cannot_restore_stock_while_active_pg_order_exists():
    """Verify Rollback Invariant:
    A rollback CANNOT restore stock while leaving an active confirmed order in PostgreSQL.
    1. Checks postgres_db.has_order(res_id): if active and cannot be cancelled, rollback is rejected.
    2. If order CAN be cancelled, rollback coordinates cancellation with PostgreSQL and restores stock exactly once.
    """
    pg = PostgresInventoryStore()
    svc = FlashSaleInventoryService(postgres_db=pg)
    svc.initialize_stock("item_rb_invariant", 10)

    res = svc.reserve("item_rb_invariant", "user_inv", quantity=3, idempotency_key="inv_k1")
    assert res.success is True
    res_id = res.record.reservation_id
    assert svc.get_stock("item_rb_invariant") == 7

    # Confirm reservation
    confirm_res = svc.confirm("item_rb_invariant", res_id)
    assert confirm_res.success is True
    assert confirm_res.status == "CONFIRMED"
    assert pg.has_order(res_id) is True
    assert svc.get_stock("item_rb_invariant") == 7

    # Case 1: PostgreSQL order is active and CANNOT be cancelled (simulate non-cancellable order)
    original_cancel = pg.cancel_order
    pg.cancel_order = lambda r_id: False

    rb_fail = svc.rollback_confirmation("item_rb_invariant", res_id)
    assert rb_fail.success is False
    assert rb_fail.status == "ACTIVE_ORDER_EXISTS"
    assert "active confirmed order exists" in (rb_fail.message or "").lower()

    # Crucial Invariant Assertions:
    # Stock MUST NOT be restored while PostgreSQL holds active order!
    assert svc.get_stock("item_rb_invariant") == 7
    # Order in PostgreSQL MUST remain active!
    assert pg.has_order(res_id) is True
    # Reservation status in service must NOT be RELEASED!
    assert svc._reserves_store["item_rb_invariant"][res_id].status == ReservationState.CONFIRMED

    # Case 2: PostgreSQL coordinates cancellation successfully
    pg.cancel_order = original_cancel

    rb_ok = svc.rollback_confirmation("item_rb_invariant", res_id)
    assert rb_ok.success is True
    assert rb_ok.record.status == ReservationState.RELEASED

    # PostgreSQL order is cancelled
    assert pg.has_order(res_id) is False
    # Stock is now safely restored
    assert svc.get_stock("item_rb_invariant") == 10

    # Case 3: Idempotent repeat rollback does NOT double-restore stock
    rb_repeat = svc.rollback_confirmation("item_rb_invariant", res_id)
    assert rb_repeat.success is True
    assert svc.get_stock("item_rb_invariant") == 10




