"""Tests for Module 25: Enterprise Polyglot Persistence Platform (Track B).

Validates:
1. PolyglotLivePlatform ACID transactional outbox consistency
2. Outbox event relay and state synchronization
3. Cache-Aside and SortedSet spend leaderboard updates
4. Zero message loss guarantee between relational database and downstream cache
5. RECONCILIATION: Handbuilt PolyglotPlatform CDC dispatching matches live coordinator flow
6. RECONCILIATION: Outbox relational consistency invariants
7. RECONCILIATION: Cross-engine multi-order spend accumulation parity
"""

from __future__ import annotations

import time

from Module_25_Final_Capstone_Polyglot_Enterprise.project_solution.polyglot_live import PolyglotLivePlatform
from Module_25_Final_Capstone_Polyglot_Enterprise.project_solution.polyglot_platform import (
    PolyglotPlatform as HandbuiltPlatform,
)


# --- IN-PROCESS RECONCILIATION & LIVE COORDINATOR TESTS ---

def test_reconciliation_handbuilt_polyglot_coordination():
    """Verify handbuilt PolyglotPlatform correctly coordinates outbox CDC events to Redis and Search."""
    platform = HandbuiltPlatform()

    # Place orders
    platform.place_order("ORD_001", "CUST_ALICE", 250.0, "Mechanical Keyboard")
    platform.place_order("ORD_002", "CUST_ALICE", 150.0, "Gaming Mouse")
    platform.place_order("ORD_003", "CUST_BOB", 80.0, "Desk Mat")

    # Invariant: Orders placed, but outbox pending CDC processing
    assert len(platform.oltp.orders) == 3
    assert len(platform.oltp.outbox_events) == 3

    # Dispatch CDC events
    processed = platform.process_cdc_events()
    assert processed == 3
    assert len(platform.oltp.outbox_events) == 0

    # Leaderboard in Redis cache must reflect cumulative spend
    assert platform.cache.leaderboard["CUST_ALICE"] == 400.0
    assert platform.cache.leaderboard["CUST_BOB"] == 80.0


def test_polyglot_live_platform_transactional_outbox():
    """Verify live coordinator guarantees atomic outbox persistence and CDC relay synchronization."""
    unique_prefix = f"test_run_{time.time_ns()}"
    platform = PolyglotLivePlatform(db_path=":memory:", key_prefix=unique_prefix)

    # Place orders
    platform.place_order("ORD_100", "CUST_001", 120.0)
    platform.place_order("ORD_101", "CUST_001", 80.0)
    platform.place_order("ORD_102", "CUST_002", 50.0)

    # Relay pending outbox events
    relayed = platform.relay_outbox_events()
    assert relayed == 3

    # Spend metrics must be strictly consistent
    assert platform.get_customer_spend("CUST_001") == 200.0
    assert platform.get_customer_spend("CUST_002") == 50.0

    # Subsequent relay should have 0 pending events
    assert platform.relay_outbox_events() == 0

    # Clean up Redis keys
    if platform.redis_client:
        platform.redis_client.delete(f"{unique_prefix}:leaderboard:spend")


def test_polyglot_live_idempotent_relay():
    """Verifies that running CDC relay repeatedly with no new events is a safe no-op."""
    unique_prefix = f"test_run_idemp_{time.time_ns()}"
    platform = PolyglotLivePlatform(db_path=":memory:", key_prefix=unique_prefix)

    platform.place_order("ORD_201", "CUST_IDEMP", 300.0)
    assert platform.relay_outbox_events() == 1
    assert platform.get_customer_spend("CUST_IDEMP") == 300.0

    # Re-running relay must not change spend
    assert platform.relay_outbox_events() == 0
    assert platform.get_customer_spend("CUST_IDEMP") == 300.0

    if platform.redis_client:
        platform.redis_client.delete(f"{unique_prefix}:leaderboard:spend")


def test_reconciliation_spend_aggregation_parity():
    """Reconciles that handbuilt platform and live coordinator compute identical spend totals."""
    unique_prefix = f"test_run_rec_{time.time_ns()}"
    live_platform = PolyglotLivePlatform(db_path=":memory:", key_prefix=unique_prefix)
    handbuilt_platform = HandbuiltPlatform()

    orders = [
        ("O_1", "USER_X", 100.0),
        ("O_2", "USER_Y", 250.0),
        ("O_3", "USER_X", 150.0),
        ("O_4", "USER_Z", 50.0),
    ]

    for oid, user, amt in orders:
        live_platform.place_order(oid, user, amt)
        handbuilt_platform.place_order(oid, user, amt, f"Description {oid}")

    live_platform.relay_outbox_events()
    handbuilt_platform.process_cdc_events()

    # Verify identical customer totals
    for user in ["USER_X", "USER_Y", "USER_Z"]:
        assert live_platform.get_customer_spend(user) == handbuilt_platform.cache.leaderboard[user]

    if live_platform.redis_client:
        live_platform.redis_client.delete(f"{unique_prefix}:leaderboard:spend")
