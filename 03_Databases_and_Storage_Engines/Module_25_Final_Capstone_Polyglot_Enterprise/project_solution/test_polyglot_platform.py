"""Module 25 Test Suite: Enterprise Polyglot Persistence Platform.

Comprehensive test suite verifying:
- Transactional Outbox atomicity & rollbacks
- Change Data Capture (CDC) event relay & ordering
- Idempotent deduplication & poison-pill DLQ quarantine
- Cache-aside semantics & single-flight stampede protection
- Distributed locking with monotonic fencing tokens
- BM25 lexical search & vector nearest-neighbor retrieval
- Columnar warehouse OLAP aggregations
- Distributed Saga orchestration with compensating rollbacks
- Cross-engine multi-database reconciliation audit
"""

from __future__ import annotations

import time
from polyglot_platform import PolyglotPlatform, SagaOrchestrator


def test_transactional_outbox_order_creation() -> None:
    platform = PolyglotPlatform()
    platform.place_order("ord_1", "Alice", 100.0, "Mechanical Keyboard")
    platform.place_order("ord_2", "Bob", 250.0, "Noise-Cancelling Headphones")

    assert len(platform.oltp.orders) == 2
    assert len(platform.oltp.outbox_events) == 2

    e1 = platform.oltp.outbox_events[0]
    e2 = platform.oltp.outbox_events[1]
    assert e1["event_id"] == 1
    assert e1["order_id"] == "ord_1"
    assert e2["event_id"] == 2
    assert e2["order_id"] == "ord_2"


def test_cdc_event_propagation_to_all_engines() -> None:
    platform = PolyglotPlatform()
    platform.place_order("ord_100", "Alice", 450.0, "MacBook Pro Laptop")

    # Before CDC, downstream systems have no data
    assert len(platform.cache.leaderboard) == 0
    assert platform.analytics.sum_revenue() == 0.0

    # Process CDC events
    processed = platform.process_cdc_events()
    assert processed == 1
    assert len(platform.oltp.outbox_events) == 0  # Outbox queue drained

    # 1. Redis Leaderboard updated
    assert platform.cache.leaderboard["Alice"] == 450.0

    # 2. Search catalog indexed
    search_hits = platform.search_catalog("macbook laptop")
    assert len(search_hits) == 1
    assert search_hits[0]["_id"] == "ord_100"

    # 3. Columnar Analytics ingested
    assert platform.analytics.sum_revenue() == 450.0


def test_cache_aside_pattern_hit_and_miss() -> None:
    platform = PolyglotPlatform()
    platform.place_order("ord_50", "Carol", 80.0, "USB-C Hub")
    platform.process_cdc_events()

    # Cache starts empty for this key
    assert platform.cache.get("order:ord_50") is None

    # First read: Cache Miss -> Fetches from Postgres & populates Redis
    order_data = platform.get_order_cache_aside("ord_50")
    assert order_data is not None
    assert order_data["customer"] == "Carol"
    assert order_data["total"] == 80.0

    # Cache is now populated
    assert platform.cache.get("order:ord_50") == order_data

    # Second read: Cache Hit -> returns directly from cache
    cached_order = platform.get_order_cache_aside("ord_50")
    assert cached_order == order_data


def test_full_text_search_ranking() -> None:
    platform = PolyglotPlatform()
    platform.place_order("p1", "UserA", 1200.0, "High Performance Gaming Desktop PC")
    platform.place_order("p2", "UserB", 900.0, "Ultra Slim Portable Laptop")
    platform.place_order("p3", "UserC", 800.0, "Office Desktop Workstation Computer")
    platform.process_cdc_events()

    # Search for "desktop"
    results = platform.search_catalog("desktop", top_k=5)
    matched_ids = [r["_id"] for r in results]

    assert "p1" in matched_ids
    assert "p3" in matched_ids
    assert "p2" not in matched_ids


def test_columnar_analytics_revenue_and_aov() -> None:
    platform = PolyglotPlatform()
    platform.place_order("o1", "User1", 100.0, "Item 1")
    platform.place_order("o2", "User2", 200.0, "Item 2")
    platform.place_order("o3", "User3", 300.0, "Item 3")
    platform.process_cdc_events()

    summary = platform.get_analytics_summary()
    assert summary["total_revenue"] == 600.0
    assert summary["avg_order_value"] == 200.0


def test_customer_leaderboard_multi_order_spend() -> None:
    platform = PolyglotPlatform()
    platform.place_order("o1", "Alice", 150.0, "Widget A")
    platform.place_order("o2", "Alice", 350.0, "Widget B")
    platform.place_order("o3", "Bob", 300.0, "Widget C")
    platform.place_order("o4", "Carol", 75.0, "Widget D")
    platform.process_cdc_events()

    leaderboard = platform.get_customer_leaderboard(top_k=3)
    assert len(leaderboard) == 3

    assert leaderboard[0] == ("Alice", 500.0)
    assert leaderboard[1] == ("Bob", 300.0)
    assert leaderboard[2] == ("Carol", 75.0)


def test_transaction_rollback_prevents_outbox_leak() -> None:
    platform = PolyglotPlatform()
    platform.oltp.begin_transaction()
    platform.oltp.create_order("aborted_ord", "Dave", 999.0, "Expensive Watch")
    platform.oltp.rollback_transaction()

    assert platform.oltp.get_order("aborted_ord") is None
    assert len(platform.oltp.outbox_events) == 0


def test_transaction_commit_atomicity() -> None:
    platform = PolyglotPlatform()
    platform.oltp.begin_transaction()
    platform.oltp.create_order("tx_ord1", "Eve", 50.0, "Book 1")
    platform.oltp.create_order("tx_ord2", "Eve", 70.0, "Book 2")
    platform.oltp.commit_transaction()

    assert platform.oltp.get_order("tx_ord1") is not None
    assert platform.oltp.get_order("tx_ord2") is not None
    assert len(platform.oltp.outbox_events) == 2


def test_cdc_batch_chunking() -> None:
    platform = PolyglotPlatform()
    for i in range(15):
        platform.place_order(f"chunk_{i}", "CustomerX", 10.0, f"Item {i}")

    assert len(platform.oltp.outbox_events) == 15
    # Process only batch of 5
    p1 = platform.process_cdc_events(max_batch_size=5)
    assert p1 == 5
    assert len(platform.oltp.outbox_events) == 10

    # Process remaining 10
    p2 = platform.process_cdc_events(max_batch_size=20)
    assert p2 == 10
    assert len(platform.oltp.outbox_events) == 0


def test_idempotent_cdc_event_replay() -> None:
    platform = PolyglotPlatform()
    platform.place_order("idemp_1", "Grace", 200.0, "Tablet")

    # Capture raw event for replay test
    raw_event = dict(platform.oltp.outbox_events[0])

    # First dispatch
    processed = platform.process_cdc_events()
    assert processed == 1
    assert platform.cache.leaderboard["Grace"] == 200.0

    # Simulate network glitch causing re-delivery of the exact same event
    platform.oltp.outbox_events.append(raw_event)
    processed_again = platform.process_cdc_events()

    # Must be deduplicated and not re-applied
    assert processed_again == 0
    assert platform.cache.leaderboard["Grace"] == 200.0
    assert platform.analytics.sum_revenue() == 200.0


def test_poison_pill_quarantined_to_dlq() -> None:
    platform = PolyglotPlatform()
    platform.place_order("good_1", "Hank", 100.0, "Keyboard")
    platform.place_order("poison_1", "Hank", 999.0, "CRASH_PAYLOAD")
    platform.place_order("good_2", "Hank", 50.0, "Mousepad")

    def is_poison(evt: dict) -> bool:
        return "CRASH_PAYLOAD" in evt["payload"].get("description", "")

    processed = platform.process_cdc_events(poison_predicate=is_poison)
    assert processed == 2
    assert len(platform.dead_letter_queue) == 1
    assert platform.dead_letter_queue[0]["payload"]["order_id"] == "poison_1"
    assert platform.analytics.sum_revenue() == 150.0


def test_fenced_distributed_locking() -> None:
    platform = PolyglotPlatform()
    res = "customer:cust_99"

    # Worker A acquires lock
    token_a = platform.cache.acquire_lock(res, owner="worker_a", ttl_seconds=5.0)
    assert token_a is not None
    assert token_a == 1

    # Worker B attempts to acquire same resource -> Rejected
    token_b = platform.cache.acquire_lock(res, owner="worker_b", ttl_seconds=5.0)
    assert token_b is None

    # Worker B cannot release Worker A's lock
    fake_release = platform.cache.release_lock(res, owner="worker_b", fencing_token=token_a)
    assert not fake_release

    # Worker A releases lock cleanly
    released = platform.cache.release_lock(res, owner="worker_a", fencing_token=token_a)
    assert released

    # Now Worker B can acquire
    token_b2 = platform.cache.acquire_lock(res, owner="worker_b", ttl_seconds=5.0)
    assert token_b2 is not None
    assert token_b2 == 2


def test_vector_semantic_search_cosine_similarity() -> None:
    platform = PolyglotPlatform()
    platform.place_order("v1", "User1", 500.0, "Database Internal Systems Book", embedding=[1.0, 0.0, 0.0])
    platform.place_order("v2", "User2", 300.0, "SQL Optimization Performance Guide", embedding=[0.9, 0.1, 0.0])
    platform.place_order("v3", "User3", 50.0, "Gardening and Plant Care", embedding=[0.0, 0.9, 0.4])
    platform.process_cdc_events()

    results = platform.search_similar_orders(query_vector=[1.0, 0.05, 0.0], top_k=2)
    matched_ids = [r["_id"] for r in results]

    assert matched_ids == ["v1", "v2"]
    assert results[0]["_score"] > 0.95
    assert results[1]["_score"] > 0.90


def test_saga_orchestration_successful_flow() -> None:
    platform = PolyglotPlatform()
    saga = SagaOrchestrator(platform)

    success, msg = saga.execute_order_saga(
        order_id="saga_1",
        customer="Alice",
        item_id="item_1",
        quantity=5,
        total_cost=250.0,
        description="5x Widgets",
    )
    assert success
    assert msg == "SAGA_SUCCESS"
    assert saga.inventory["item_1"] == 95
    assert saga.payment_balance["Alice"] == 750.0

    platform.process_cdc_events()
    assert platform.analytics.sum_revenue() == 250.0


def test_saga_compensation_on_insufficient_inventory() -> None:
    platform = PolyglotPlatform()
    saga = SagaOrchestrator(platform)

    success, msg = saga.execute_order_saga(
        order_id="saga_fail_inv",
        customer="Alice",
        item_id="item_2",
        quantity=5,
        total_cost=100.0,
        description="Rare item",
    )
    assert not success
    assert "Insufficient inventory" in msg
    assert saga.inventory["item_2"] == 2
    assert saga.payment_balance["Alice"] == 1000.0
    assert len(platform.oltp.orders) == 0


def test_saga_compensation_on_insufficient_payment() -> None:
    platform = PolyglotPlatform()
    saga = SagaOrchestrator(platform)

    success, msg = saga.execute_order_saga(
        order_id="saga_fail_pay",
        customer="BrokeUser",
        item_id="item_1",
        quantity=1,
        total_cost=50.0,
        description="Widget",
    )
    assert not success
    assert "Insufficient funds" in msg
    assert saga.inventory["item_1"] == 100
    assert saga.payment_balance["BrokeUser"] == 5.0
    assert len(platform.oltp.orders) == 0


def test_cross_engine_reconciliation_audit() -> None:
    platform = PolyglotPlatform()
    platform.place_order("rec_1", "Alice", 100.0, "Item A")
    platform.place_order("rec_2", "Bob", 200.0, "Item B")
    platform.place_order("rec_3", "Alice", 150.0, "Item C")

    balanced_before, stats_before = platform.audit_reconciliation()
    assert not balanced_before
    assert stats_before["oltp_total"] == 450.0
    assert stats_before["olap_total"] == 0.0

    platform.process_cdc_events()

    balanced_after, stats_after = platform.audit_reconciliation()
    assert balanced_after
    assert stats_after["oltp_total"] == 450.0
    assert stats_after["olap_total"] == 450.0
    assert stats_after["redis_total"] == 450.0


def test_cache_invalidation_upon_order_mutation() -> None:
    platform = PolyglotPlatform()
    platform.place_order("mut_1", "Dave", 120.0, "SSD Disk")
    platform.process_cdc_events()

    o1 = platform.get_order_cache_aside("mut_1")
    assert o1 is not None
    assert platform.cache.get("order:mut_1") is not None

    platform.oltp.update_order_status("mut_1", "SHIPPED")

    platform.cache.invalidate("order:mut_1")
    assert platform.cache.get("order:mut_1") is None

    o2 = platform.get_order_cache_aside("mut_1")
    assert o2 is not None
    assert o2["status"] == "SHIPPED"
    assert platform.cache.get("order:mut_1")["status"] == "SHIPPED"


def test_columnar_revenue_by_customer() -> None:
    platform = PolyglotPlatform()
    platform.place_order("c1", "CustA", 10.0, "Coffee")
    platform.place_order("c2", "CustA", 20.0, "Bagel")
    platform.place_order("c3", "CustB", 35.0, "Lunch")
    platform.process_cdc_events()

    by_cust = platform.analytics.revenue_by_customer()
    assert by_cust["CustA"] == 30.0
    assert by_cust["CustB"] == 35.0


def test_cache_stampede_single_flight_mutex() -> None:
    platform = PolyglotPlatform()
    platform.place_order("stampede_1", "Zara", 88.0, "Headset")
    platform.process_cdc_events()

    platform._single_flight_in_progress.add("order:stampede_1")
    res = platform.get_order_cache_aside("stampede_1")
    assert res is not None
    assert res["customer"] == "Zara"


def test_multi_customer_concurrent_outbox_ordering() -> None:
    platform = PolyglotPlatform()
    platform.place_order("o1", "Alice", 10.0, "Book")
    platform.place_order("o2", "Bob", 20.0, "Pen")
    platform.place_order("o3", "Alice", 30.0, "Notebook")

    events = platform.oltp.outbox_events
    assert [e["event_id"] for e in events] == [1, 2, 3]
    assert [e["order_id"] for e in events] == ["o1", "o2", "o3"]


def test_outbox_event_structure_fields() -> None:
    platform = PolyglotPlatform()
    platform.place_order("o_field", "Zoe", 123.45, "Desk Lamp")
    event = platform.oltp.outbox_events[0]

    assert "event_id" in event
    assert "event_type" in event
    assert "order_id" in event
    assert "payload" in event
    assert "retry_count" in event
    assert event["payload"]["total"] == 123.45


def test_search_catalog_empty_query_handling() -> None:
    platform = PolyglotPlatform()
    platform.place_order("o_empty", "UserX", 10.0, "Valid Description")
    platform.process_cdc_events()

    assert platform.search_catalog("") == []
    assert platform.search_catalog("   ") == []


def test_search_catalog_case_insensitive_token_matching() -> None:
    platform = PolyglotPlatform()
    platform.place_order("o_caps", "UserY", 99.0, "Wireless Bluetooth KEYBOARD")
    platform.process_cdc_events()

    res = platform.search_catalog("keyboard")
    assert len(res) == 1
    assert res[0]["_id"] == "o_caps"


def test_vector_search_identical_vectors_perfect_score() -> None:
    platform = PolyglotPlatform()
    platform.place_order("vec_same", "U1", 10.0, "Identical Item", embedding=[0.6, 0.8, 0.0])
    platform.process_cdc_events()

    res = platform.search_similar_orders(query_vector=[0.6, 0.8, 0.0], top_k=1)
    assert len(res) == 1
    assert abs(res[0]["_score"] - 1.0) < 1e-4


def test_vector_search_orthogonal_vectors_zero_score() -> None:
    platform = PolyglotPlatform()
    platform.place_order("vec_ortho", "U2", 10.0, "Ortho Item", embedding=[1.0, 0.0, 0.0])
    platform.process_cdc_events()

    res = platform.search_similar_orders(query_vector=[0.0, 1.0, 0.0], top_k=1)
    assert len(res) == 1
    assert res[0]["_score"] == 0.0


def test_distributed_lock_expired_lease_allows_reacquisition() -> None:
    platform = PolyglotPlatform()
    # Acquire with very short TTL
    t1 = platform.cache.acquire_lock("exp_res", owner="w1", ttl_seconds=0.05)
    assert t1 is not None

    time.sleep(0.06)

    # w2 can now acquire because w1's lease expired
    t2 = platform.cache.acquire_lock("exp_res", owner="w2", ttl_seconds=5.0)
    assert t2 is not None
    assert t2 > t1


def test_distributed_lock_nonexistent_resource_release() -> None:
    platform = PolyglotPlatform()
    assert not platform.cache.release_lock("ghost_res", owner="w1", fencing_token=1)


def test_dlq_multiple_poison_messages() -> None:
    platform = PolyglotPlatform()
    platform.place_order("bad_1", "U", 10.0, "POISON_1")
    platform.place_order("good", "U", 20.0, "SAFE_ITEM")
    platform.place_order("bad_2", "U", 30.0, "POISON_2")

    processed = platform.process_cdc_events(poison_predicate=lambda e: "POISON" in e["payload"]["description"])
    assert processed == 1
    assert len(platform.dead_letter_queue) == 2
    assert [e["payload"]["order_id"] for e in platform.dead_letter_queue] == ["bad_1", "bad_2"]


def test_columnar_analytics_empty_warehouse() -> None:
    platform = PolyglotPlatform()
    summary = platform.get_analytics_summary()
    assert summary["total_revenue"] == 0.0
    assert summary["avg_order_value"] == 0.0
    assert platform.analytics.revenue_by_customer() == {}


def test_leaderboard_empty_top_k() -> None:
    platform = PolyglotPlatform()
    assert platform.get_customer_leaderboard(top_k=5) == []


def test_saga_zero_quantity_or_cost() -> None:
    platform = PolyglotPlatform()
    saga = SagaOrchestrator(platform)
    success, msg = saga.execute_order_saga("free_ord", "Alice", "item_1", 0, 0.0, "Free Gift")
    assert success
    assert msg == "SAGA_SUCCESS"
    assert saga.inventory["item_1"] == 100


def test_cache_aside_nonexistent_order() -> None:
    platform = PolyglotPlatform()
    res = platform.get_order_cache_aside("nonexistent_id")
    assert res is None
    assert platform.cache.get("order:nonexistent_id") is None


def test_multiple_cdc_batches_complete_drain() -> None:
    platform = PolyglotPlatform()
    for i in range(7):
        platform.place_order(f"b_{i}", "BatchUser", 10.0, f"Desc {i}")

    assert len(platform.oltp.outbox_events) == 7
    # Batch size 3
    platform.process_cdc_events(max_batch_size=3)
    assert len(platform.oltp.outbox_events) == 4
    platform.process_cdc_events(max_batch_size=3)
    assert len(platform.oltp.outbox_events) == 1
    platform.process_cdc_events(max_batch_size=3)
    assert len(platform.oltp.outbox_events) == 0


def test_order_status_update_unknown_order() -> None:
    platform = PolyglotPlatform()
    # Does not throw
    platform.oltp.update_order_status("mystery_order", "SHIPPED")


def test_reconciliation_detects_tampered_redis_score() -> None:
    platform = PolyglotPlatform()
    platform.place_order("tamper_ord", "Eve", 500.0, "Item")
    platform.process_cdc_events()

    # Tamper with Redis leaderboard
    platform.cache.leaderboard["Eve"] = 9999.0
    balanced, stats = platform.audit_reconciliation()
    assert not balanced
    assert stats["oltp_total"] == 500.0
    assert stats["redis_total"] == 9999.0
